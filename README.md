# ForeverQuest
# AI-Powered D&D-Style Multiplayer Telegram Game

Welcome to the AI-Powered D&D-Style Multiplayer Telegram Game! 
This project leverages OpenAI's capabilities to create an interactive and engaging multiplayer game on Telegram, where players can immerse themselves in a Dungeons & Dragons-like adventure.

## Project Overview

**Objective**: To provide an engaging, interactive, and multiplayer D&D-style game experience through Telegram, where an AI acts as the Dungeon Master, controlling non-player characters, describing settings, and reacting to players' actions.

**Skills Demonstrated**:
- Python programming
- API integration
- Telegram bot development
- Asynchronous programming

**Tools Used**:
- Python
- OpenAI API
- Python Telegram Bot API (`python-telegram-bot`)
- dotenv for environment variable management

How It Works

Initialize Game State:
The game initializes by loading the game state from a JSON file if it exists or creates a new game state.

Message Handling:
The bot listens for messages in the Telegram chat. When a player sends a message, it is processed, and the AI Dungeon Master (using OpenAI) responds by describing the setting, controlling non-player characters, and reacting to the player's actions.

Game Log:
The game logs all interactions to a game_log.txt file for record-keeping and potential game state restoration.

Auto-Save Feature:
The game state is auto-saved at regular intervals to prevent data loss.

Important Notes
API Costs: Using the OpenAI API incurs costs. Ensure you monitor your usage and set appropriate limits.
Environment Variables: Keep your API keys secure by using environment variables and never hard-code them in your scripts.

Example Usage
Start the Game:
Players join the Telegram group where the bot is added.

Player Interaction:
Players send messages to the bot, and the AI Dungeon Master responds, guiding them through an interactive story.

Contact
For any questions or issues, please contact me at jared.hull.dev@gmail.com or find me on GitHub.

Enjoy your adventure!
