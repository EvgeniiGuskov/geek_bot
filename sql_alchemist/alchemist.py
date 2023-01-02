from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_alchemist.database_structure.declarative_base import Base
from sql_alchemist.database_structure.tables.groups_and_users import Groups, Users
from sql_alchemist.database_structure.tables.mustwatches import Watches, Mustwatches


class Alchemist:
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
