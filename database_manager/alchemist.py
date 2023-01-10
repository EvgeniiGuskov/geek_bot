from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_manager.database_tables.base.declarative_base import Base

from database_manager.command_handlers.register_manager import RegisterManager
from database_manager.command_handlers.mustwatch_manager import MustwatchManager


class Alchemist(RegisterManager, MustwatchManager):
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
