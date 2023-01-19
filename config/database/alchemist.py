from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database.tables import Base

from src.service.register_db import RegisterDb
from src.view.commands_handlers.register_handler.register_response import RegisterResponse
from src.service.mustwatch_db import MustwatchDb
from src.view.commands_handlers.mustwatch_handler.mustwatch_response import MustwatchResponse
from src.service.mustwatch_rating_db import MustwatchRatingDb
from src.view.commands_handlers.mustwatch_rating_handler.mustwatch_rating_response import MustwatchRatingResponse


class Alchemist(RegisterDb, MustwatchDb, MustwatchRatingDb):
    __USERNAME = "postgres"
    __PASSWORD = "password"
    __HOST = "localhost"
    __DATABASE = "geek_bot"

    def __init__(self):
        self.__engine = create_engine(
            f"postgresql+psycopg2://{Alchemist.__USERNAME}:{Alchemist.__PASSWORD}"
            f"@{Alchemist.__HOST}/{Alchemist.__DATABASE}"
        )
        Base.metadata.create_all(self.__engine)

        self.__Session = sessionmaker(self.__engine)
        self.session = self.__Session()
