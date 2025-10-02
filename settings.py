import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

dotenv.load_dotenv()

class DatabaseConfig:
    DATABASE_URL = os.getenv("DATABASE_URL")  # Render выдаёт эту переменную
    DATABASE_NAME = os.getenv("DATABASE_NAME", "db_auth")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    SECRET_KEY = os.getenv("SECRET_KEY")
    IMAGES_DIR = "static/images_menu"

    def uri_postgres(self):
        if self.DATABASE_URL:
            # Render иногда даёт postgres:// вместо postgresql://
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        # fallback для локалки
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5432/{self.DATABASE_NAME}"

    def uri_sqlite(self):
        return f"sqlite:///{self.DATABASE_NAME}.db"


config = DatabaseConfig()

engine = create_engine(
    config.uri_postgres(),
    echo=True,
    pool_pre_ping=True  # авто-проверка соединения (иначе может отваливаться)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    @classmethod
    def create_db(cls):
        cls.metadata.create_all(engine)

    @classmethod
    def drop_db(cls):
        cls.metadata.drop_all(engine)
