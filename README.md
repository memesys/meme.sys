# Meme.Sys – Memes systems.

Mimesis: [wiki](https://en.wikipedia.org/wiki/Mimesis)

(OpenAI, LLM, OCR)-powered telegram bot for semantic memes search.

Search your memes library, always have any meme you need at the tips of the fingers.

1. Repost you memes to the chat
2. Get search terms
3. Search telegram for search terms when you need to find your meme
4. Arificial memeory profit

# Setup
0. Install python3.11 or higher.
1. Clone [memesys repo](https://github.com/memesys/meme.sys) and navigate to repo dir
2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Setup environment variables:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` file and set:
   - `TG_BOT_TOKEN`: Get from [@BotFather](https://t.me/BotFather)
   - `OPENAI_API_KEY`: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - `DATABASE_URI`: (Optional) Database connection string

4. Choose one of the installation methods:

## Option A: Install with pip (standard)
```bash
pip install .  # Install package from current directory
```

## Option B: Install with uv (faster)
1. Install uv first:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2. Install package:
    ```bash
    uv pip install .
    ```

## Option C: Editable install (for development)
For development installation (with either pip or uv):
```bash
# Using pip
pip install -r requirements.txt -e .

# OR using uv
uv pip install -r requirements.txt -e .
```

# Usage
After installation, you can run the bot using:

```bash
python -m memesys.bot
```

# Database Configuration
By default, the bot uses SQLite database stored in `memes.db` file. To use PostgreSQL:

1. Install PostgreSQL and create a database
2. Set `DATABASE_URI` in `.env`:
   ```
   DATABASE_URI=postgresql+asyncpg://user:password@host:port/dbname
   ```

# Bot Commands
- `/start` - Start the bot and get welcome message
- `/search_all <terms>` - Search for memes by description
- Send any image to save it with searchable description

# Troubleshooting
1. If you get "TG_BOT_TOKEN environment variable is not set" error:
   - Make sure you copied `.env.template` to `.env`
   - Make sure you set valid Telegram bot token in `.env`

2. If you get OpenAI API errors:
   - Check if your OpenAI API key is valid
   - Make sure you have enough credits

3. For database errors:
   - Check if DATABASE_URI is correct
   - For PostgreSQL, make sure the database exists and is accessible
