from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.tables import Base
from config.database.db_config import AlchemistConfig


class Alchemist:

    def __init__(self):
        self.__engine = create_engine(
            f"{AlchemistConfig.DATABASE}://{AlchemistConfig.USERNAME}:{AlchemistConfig.PASSWORD}"
            f"@{AlchemistConfig.HOST}/{AlchemistConfig.DATABASE_NAME}"
        )
        Base.metadata.create_all(self.__engine)

        self.__Session = sessionmaker(self.__engine)
        self.session = self.__Session()
