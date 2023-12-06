# ChatKNML Discord Bot

## Setup

```bash
# Create virtual env
python3 -m venv .venv
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# Create env variables
touch .env

# Insert Bot token here
echo "[BOT TOKEN]" > .env

# Set variables
source .env
set -a

# Run a bot!
python3 Bot.py
```
