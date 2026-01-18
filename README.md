# Basketball Telegram Bot

A Telegram bot that sends motivational basketball messages.

## Features

- Sends a welcome message with inline keyboard when user sends `/start`
- Responds to inline button press by sending a new message (preserving chat history)

## Requirements

- Python 3.8+
- python-telegram-bot library

## Installation and Setup

### Local Development

1. Clone or download the project
2. Create a virtual environment:
   ```bash
   python -m venv bot_env
   ```
3. Activate the virtual environment:
   ```bash
   # On Windows
   bot_env\Scripts\Activate.ps1
   
   # On Linux/Mac
   source bot_env/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the bot:
   ```bash
   python bot.py
   ```

### Server Deployment with systemd

1. Copy the project to your server (e.g., to `/opt/basket-bot/`)

2. Install Python and pip if not already installed:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

3. Create a dedicated user for the bot:
   ```bash
   sudo useradd -r -s /bin/false botuser
   sudo chown -R botuser:botuser /opt/basket-bot/
   ```

4. Create a virtual environment and install dependencies:
   ```bash
   cd /opt/basket-bot/
   sudo -u botuser python3 -m venv venv
   sudo -u botuser venv/bin/pip install -r requirements.txt
   ```

5. Create a systemd service file at `/etc/systemd/system/basket-bot.service`:
   ```ini
   [Unit]
   Description=Basketball Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=botuser
   WorkingDirectory=/opt/basket-bot
   Environment=PATH=/opt/basket-bot/venv/bin
   ExecStart=/opt/basket-bot/venv/bin/python bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

6. Reload systemd and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start basket-bot
   sudo systemctl enable basket-bot
   ```

7. Check the service status:
   ```bash
   sudo systemctl status basket-bot
   ```

8. View logs:
   ```bash
   sudo journalctl -u basket-bot -f
   ```

## Bot Commands

- `/start` - Start the bot and receive welcome message with inline keyboard

## Files Structure

- `bot.py` - Main bot logic
- `requirements.txt` - Python dependencies

Note: The bot uses environment variables for configuration. Set `BOT_TOKEN` before running.