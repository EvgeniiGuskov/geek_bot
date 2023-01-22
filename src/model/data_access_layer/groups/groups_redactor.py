from sqlalchemy.orm.query import Query

from src.model.tables import Groups


class GroupsRedactor:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def create_group(self,
                     **kwargs: dict) -> Query:
        group = Groups(
            **kwargs
        )
        self.session.add(group)
        return group
