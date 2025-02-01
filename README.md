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
3. Setup .env file:
   ```bash
   cp .env.template .env
   ```
   Fill in the .env file with your api keys.

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
pip install -e .

# OR using uv
uv pip install -e .
```

# Usage
After installation, you can run the bot using:
```bash
memesys
```

Or using Python directly:
```bash
python -m memesys.bot
```
