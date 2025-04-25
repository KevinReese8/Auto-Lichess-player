Here is the English translation of the README file:

---

# Lichess Auto Chess Bot

This project is an automated chess bot that connects to lichess.org and plays games automatically. It can analyze the board state, compute the best moves using a chess engine, and make moves on the platform.

## Features

- Automatically connects to the lichess.org API
- Reads the current board state
- Computes the best moves using a chess engine (e.g., Stockfish)
- Makes moves on lichess.org automatically
- Starts a new game after the current game ends

## Requirements

- Python 3.6 or higher
- Chess engine (Stockfish is recommended)
- Lichess API token

## Installation Steps

1. Clone or download this repository.

2. Install the required Python packages:

   ```bash
   pip install python-chess berserk
   ```

3. Download and install the Stockfish chess engine:
   - Download the appropriate version for your operating system from the [Stockfish official website](https://stockfishchess.org/download/).
   - Place the downloaded engine file in the project's `stockfish` directory.
   - Ensure the engine file has execution permissions (use `chmod +x stockfish-xxx` on macOS/Linux).

4. Obtain a Lichess API token:
   - Log in to your Lichess account.
   - Visit [Lichess OAuth Token page](https://lichess.org/account/oauth/token).
   - Create a new access token with the following permissions:
     - Read preferences
     - Read email address
     - Play games on the website
     - Challenge AI and human players

5. Configure your API token:
   - Open the `config.py` file.
   - **Replace the value of the `LICHESS_API_TOKEN` variable with your Lichess API token.**
   - If necessary, set the `ENGINE_PATH` variable to the path of your chess engine.

## Usage Instructions

1. Ensure all installation steps are completed.

2. Run the bot:

   ```bash
   python lichess_bot.py
   ```

3. The bot will automatically connect to Lichess, create a new game or accept existing challenges, and start playing.

4. To stop the bot, press `Ctrl+C`.

## Custom Settings

You can modify the following settings in the `config.py` file:

- `ENGINE_PATH`: Path to the chess engine.
- `ENGINE_THINK_TIME`: Engine thinking time (in seconds).
- `GAME_SETTINGS`: Game settings, including clock settings, game variants, and color preferences.

## Notes

- Please adhere to Lichess's terms of service and API usage policies.
- Avoid excessively creating and abandoning games, as this may result in account restrictions.
- Ensure the chess engine path is set correctly.

## Troubleshooting

- If you encounter a "Chess engine not found" error, check if your engine path is correct.
- If you face API connection issues, ensure your API token is valid and has the correct permissions.
- If the bot cannot create new games, check your network connection and Lichess service status.

---
