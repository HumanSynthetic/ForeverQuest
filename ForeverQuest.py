import json
from pathlib import Path
from telegram import Update
from telegram.ext import Application, MessageHandler, CallbackContext, filters
import openai
import asyncio
import rackspace_email
import telegram_message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Ensure you have set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

def close_foreverquest():
    # Close the foreverquest program
    raise SystemExit

# Path to the game state file
game_state_file = Path("game_state.json")

# Function to load the game state
def load_game_state():
    if game_state_file.exists():
        with game_state_file.open() as f:
            return json.load(f)
    return {}

# Function to save the game state
def save_game_state(state):
    with game_state_file.open("w") as f:
        json.dump(state, f)

# Create an Application instance
app = Application.builder().token(telegram_token).build()

# Define starting prompt
prefix = "You are the AI Dungeon Master, your role is to describe the setting, control non-player characters, and react to the player's actions, not to control or speak for player characters. Please facilitate and cultivate interactive and exciting experiences. Be concise and clear. Do not be afraid to ask questions. You may manifest as a character in the game, but you are not a player character."
prompt = ""

# Store previous input
prev_input = ""

# Set up autosave interval (in seconds)
autosave_interval = 60

# Set up timer for autosave
global autosave_timer  # Declare the global variable
autosave_timer = asyncio.get_event_loop().time() + autosave_interval

async def handle_messages(update: Update, context: CallbackContext) -> None:
    global prev_input, prompt, autosave_timer  # Make sure to use global variables
    user_input = update.message.text
    user_name = update.message.from_user.first_name
    structured_input = f"{user_name}: {user_input}"
    chat_type = update.message.chat.type
    group_name = update.message.chat.title if chat_type in ["group", "supergroup"] else None

    if update.message.from_user.id == context.bot.id or structured_input == prev_input:
        return  # Skip processing if message is from the bot itself or is a duplicate

    prev_input = structured_input
    prompt += f"\n{update.message.from_user.first_name}: {structured_input}"

    with open("game_log.txt", "a+") as log_file:
        log_file.write(f"{update.message.from_user.first_name}: {structured_input}\n")

        # Creating a system message to inform the AI about the chat context
        chat_context_message = {
            "role": "system",
            "content": f"This is a {chat_type} chat" + (f" named {group_name}" if group_name else "")
        }

        response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are the AI Dungeon Master, your role is to describe the setting, control non-player characters, and react to the player's actions, not to control or speak for player characters. Please facilitate and cultivate interactive and exciting experiences. Be concise and clear. Do not be afraid to ask questions. You may manifest as a character in the game, but you are not a player character."
            },
            chat_context_message,
            {
                "role": "user",
                "content": structured_input
            }
        ],
        temperature=0.5,
        max_tokens=1000,
        top_p=0.8,
        frequency_penalty=0.2,
        presence_penalty=0
        )

        # print("This is the response: " + str(response))  # Debugging line to check the entire response

        story = response.choices[0].message['content'].strip()
        if not story:
            await update.message.reply_text("Add More!")
        else:
            await update.message.reply_text(story)
            log_file.write(f"AI: {story}\n")

        if asyncio.get_event_loop().time() >= autosave_timer:
            log_file.flush()  # Save the log file
            autosave_timer = asyncio.get_event_loop().time() + autosave_interval  # Update the global autosave timer

def main():
    # Add the message handler to the application
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))  # Changed line
    app.run_polling()
    app.idle()

if __name__ == '__main__':
    main()