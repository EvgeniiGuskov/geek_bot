from sqlalchemy.orm.query import Query

from src.model.tables import Users


class UsersRedactor:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def create_user(self,
                    **kwargs: dict) -> Query:
        user = Users(
            **kwargs
        )
        self.session.add(user)
        return user
