import base64
import os
from io import BytesIO
from typing import Final

from loguru import logger
from openai import AsyncOpenAI, OpenAIError


API_KEY: Final[str] = os.getenv("OPENAI_API_KEY")
OPEN_AI_CLIENT: Final[AsyncOpenAI] = AsyncOpenAI(api_key=API_KEY)


def encode_image(image_data: BytesIO) -> str:
    """Convert image data to base64 string."""
    return base64.b64encode(image_data.getvalue()).decode('utf-8')


async def chat_gpt_description(image_data: BytesIO) -> str:
    """Get image description from GPT-4 Vision.

    Args:
        image_data: BytesIO object containing the image

    Returns:
        str: Description of the image with search terms in English and Russian

    Raises:
        OpenAIError: If there's an error communicating with OpenAI API
    """
    try:
        base64_image = encode_image(image_data)

        response = await OPEN_AI_CLIENT.chat.completions.create(
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
    except OpenAIError as e:
        logger.error(f"Error getting image description: {e}")
        raise
