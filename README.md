# TwitchBot

## Overview

This is a Twitch Bot developed to enhance user interaction and engagement on Twitch channels. The bot includes a wide range of features such as mini-games, chat commands, watchtime tracking, interval messages, and much more. It is designed with modularity and scalability in mind, making it adaptable for various use cases.

## Features

- **Chat Interaction Commands**:
  - Randomized responses (e.g. 8ball).
  - Adding, removing, and displaying quotes.
  - Watchtime tracking and leaderboard display.
  - Hug, random number generation, and custom commands.

- **Mini-Games**:
  - Duel system with bets.
  - Gambling and currency system.
  - Stats-based gameplay with upgrade options like `rizz`, `sigma` and `aura`.

- **Moderation Tools**:
  - Commands to update stream title and game.
  - Interval messages with customizable content.
  - Error logging and recovery mechanisms.

- **Stream Tracking**:
  - Track uptime, followage, and watchtime.
  - Save game history played on the stream.

- **Miscellaneous**:
  - Discord, Steam, and social media integration.
  - Command aliases for convenience.
  - Debug commands (`ping`, `pong`, `peng`, `pow`) for testing bot responsiveness.

## File Structure

```plaintext
Twitchbot
├── app
│   ├── style
│   │   ├── __init__.py
│   │   └── better_print.py
│   ├── twitch
│   │   ├── __init__.py
│   │   ├── minigame.py
│   │   ├── oauth_2.py
│   │   ├── quotes.py
│   │   ├── request.py
│   │   ├── tts.py
│   │   ├── twitch_chatbot.py
│   │   ├── twitch_rewards.py
│   │   └── watchtime.py
│   ├── __init__.py
│   └── logging.py
├── json
│   ├── shared
│   │   ├── crash_count.json
│   │   └── quotes.json
│   ├── twitch
│   │   ├── clips.json
│   │   ├── count.json
│   │   ├── minigame.json
│   │   ├── oauth.json
│   │   ├── pick_game.json
│   │   └── watchtime.json
├── .env
├── README.md
├── requirements.txt
├── run_twitch.py
├── start.bat
└── start.sh
```

## Note

- The TTS Function is currently disabled due to TTS installing issues through pip.

- Before you start the bot, replace the placeholder in the `.env` file.

##

### For Windows user

You need to execute `start.bat`

### For the Linux user

 You have to do a few steps:

- **First**
You need to install `dos2unix`:
```
sudo apt install dos2unix -y
```

- **Second**
Go to the directory of the bot and do as follow:
```
dos2unix start.sh
```

- **Third**
Give the `start.sh` execute permission:
```
chmod +x start.sh
```

- **Last**
You can start the bot with:
```
./start.sh
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
By using this project, you agree to comply with the licenses of all third-party dependencies. Additionally, if you use this bot to interact with services like Twitch, you must ensure compliance with their terms of service and developer policies.
