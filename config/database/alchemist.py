from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database.tables import Base
from config.database.db_config import AlchemistConfig
from src.service.register_db import RegisterDb
from src.service.mustwatch_db import MustwatchDb
from src.service.mustwatch_rating_db import MustwatchRatingDb


class Alchemist(RegisterDb, MustwatchDb, MustwatchRatingDb):

    def __init__(self):
        self.__engine = create_engine(
            f"{AlchemistConfig.DATABASE}://{AlchemistConfig.USERNAME}:{AlchemistConfig.PASSWORD}"
            f"@{AlchemistConfig.HOST}/{AlchemistConfig.DATABASE_NAME}"
        )
        Base.metadata.create_all(self.__engine)

        self.__Session = sessionmaker(self.__engine)
        self.session = self.__Session()
