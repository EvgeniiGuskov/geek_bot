from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alchemical_lab.database_structure.declarative_base import Base
from alchemical_lab.database_structure.tables.groups_and_users import Groups, Users
from alchemical_lab.database_structure.tables.mustwatches import UserRequests, Watches, Mustwatches

from alchemical_lab.associates_to_the_alchemist.register_associate import RegisterAssociate
from alchemical_lab.associates_to_the_alchemist.manage_mustwatch_associate import ManageMustwatchAssociate


class Alchemist(RegisterAssociate, ManageMustwatchAssociate):
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
