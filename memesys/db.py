import hashlib
import os
from typing import Final, List

from loguru import logger
from sqlalchemy import Column, String, JSON, create_engine, cast, select, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# Make sure we're using the standard SQLite dialect
if os.environ.get("DATABASE_URI"):
    DATABASE_URI: Final[str] = os.environ["DATABASE_URI"]
else:
    # Use standard sqlite:// instead of sqlite+aiosqlite://
    DATABASE_URI: Final[str] = "sqlite:///memes.db"

engine = create_engine(
    DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    # Enable SQLite foreign key support
    creator=lambda: __import__('sqlite3').connect('memes.db', isolation_level=None)
)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class RecognisedImage(Base):
    """Model for storing recognized images and their metadata."""
    __tablename__ = 'recognised_images'

    image_hash = Column(String, primary_key=True, unique=True)
    telegram_image_link = Column(String, nullable=False)
    recognized_search_terms = Column(JSON, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<RecognisedImage("
            f"link={self.telegram_image_link}, "
            f"terms={self.recognized_search_terms})>"
        )


def create_tables() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(engine)
    logger.info("Database tables created")


def save_image(data: bytes, text: str, link: str) -> None:
    """Save image data and metadata to database."""
    image_hash = hashlib.sha256(data).hexdigest()

    with Session() as session:
        try:
            image = RecognisedImage(
                image_hash=image_hash,
                telegram_image_link=link,
                recognized_search_terms=text
            )
            session.add(image)
            session.commit()
            logger.debug(f"Saved image {image_hash}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving image: {e}")
            raise


def search_image(search_text: str) -> List[RecognisedImage]:
    """Search for images by text in their recognized terms."""
    with Session() as session:
        try:
            query = select(RecognisedImage).where(
                cast(RecognisedImage.recognized_search_terms, String).contains(search_text)
            )
            return session.execute(query).scalars().all()
        except Exception as e:
            logger.error(f"Error searching images: {e}")
            raise