import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

dotenv.load_dotenv()

class DatabaseConfig:
    DATABASE_URL = os.getenv("DATABASE_URL")  # Для Render
    DATABASE_NAME = os.getenv("DATABASE_NAME", "db_auth")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    ROOT_DB_USER = os.getenv("ROOT_DB_USER")
    ROOT_DB_PASSWORD = os.getenv("ROOT_DB_PASSWORD")
    SECRET_KEY = os.getenv("SECRET_KEY")
    IMAGES_DIR = "static/images_menu"

    def uri_postgres(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5432/{self.DATABASE_NAME}"

    def uri_sqlite(self):
        return f"sqlite:///{self.DATABASE_NAME}.db"

config = DatabaseConfig()
engine = create_engine(
    config.uri_postgres(), 
    echo=True,
    connect_args={'client_encoding': 'utf8'}
)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    def create_db(self):
        self.metadata.create_all(engine)

    def drop_db(self):
        self.metadata.drop_all(engine) 
