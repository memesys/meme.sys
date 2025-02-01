from dotenv import load_dotenv
load_dotenv()

import base64
import os
from io import BytesIO
from typing import Final

from loguru import logger
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from openai import OpenAI

from memesys.db import create_tables, save_image, search_image

TG_BOT_TOKEN: Final[str] = os.getenv("TG_BOT_TOKEN")
if not TG_BOT_TOKEN:
    raise ValueError("TG_BOT_TOKEN environment variable is not set")

OPENAI_CLIENT = OpenAI()


def encode_image(image_data: BytesIO) -> str:
    """Convert image data to base64 string."""
    return base64.b64encode(image_data.getvalue()).decode('utf-8')


def get_image_description(image_data: BytesIO) -> str:
    """Get image description from GPT-4 Vision."""
    base64_image = encode_image(image_data)

    response = OPENAI_CLIENT.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "What's in this image? "
                            "Produce only semantic search terms which can be used to look for this image. "
                            "Mention the objects, people, places, actions, activities, "
                            "colors and text in the image. "
                            "Create terms in english and then in russian language."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            },
        ],
        max_tokens=300,
    )

    return str(response.choices[0].message.content)


def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hi! Send me a picture to save it for searching, or use /search_all to find memes.'
    )


def process_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save photo with its description for future search."""
    try:
        photo_file = update.message.photo[-1].get_file()
        image_data = BytesIO()
        photo_file.download_to_memory(image_data)

        description = get_image_description(image_data)
        link = f'https://t.me/c/{update.message.chat.id}/{update.message.id}'

        save_image(
            data=image_data.getvalue(),
            text=description,
            link=link,
        )

        update.message.reply_text(
            "✅ Meme saved with description:\n\n" + description
        )
    except Exception as e:
        logger.exception("Error processing photo")
        update.message.reply_text(
            "❌ An error occurred while processing your image."
        )


def search_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search for memes by description."""
    search_query = update.message.text.removeprefix("/search_all").strip()
    if not search_query:
        update.message.reply_text(
            "Please provide search terms after /search_all command"
        )
        return

    try:
        results = search_image(search_query)
        if not results:
            update.message.reply_text("No memes found matching your search terms")
            return

        response = "Found memes:\n\n" + "\n\n".join(
            f"🔗 {result.telegram_image_link}\n📝 {result.recognized_search_terms}"
            for result in results
        )
        update.message.reply_text(response)
    except Exception as e:
        logger.exception("Error searching memes")
        update.message.reply_text(
            "❌ An error occurred while searching. Please try again later."
        )


def main():
    """Start the bot."""
    # Initialize database
    create_tables()

    # Create application
    application = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search_all", search_meme))
    application.add_handler(MessageHandler(filters.PHOTO, process_photo))

    # Start polling
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
