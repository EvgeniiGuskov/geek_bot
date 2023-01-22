from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.tables import Base


class Alchemist:

    def __init__(self):
        load_dotenv()
        self.__engine = create_engine(
            f"{getenv('DB_SPEC')}://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
            f"@{getenv('DB_HOST_PORT')}/{getenv('POSTGRES_DB')}"
        )
        Base.metadata.create_all(self.__engine)

        self.__Session = sessionmaker(self.__engine)
        self.session = self.__Session()
