from sqlalchemy.orm.query import Query

from src.model.tables import Users


class UsersRedactor:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def insert_values(self,
                      **kwargs: dict) -> Query:
        record = Users(
            **kwargs
        )
        self.session.add(record)
        return record
