from typing import List

from sqlalchemy.orm.query import Query

from src.model.tables import Watches


class WatchesRedactor:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def insert_values(self,
                      **kwargs: dict) -> Query:
        record = Watches(
            **kwargs
        )
        self.session.add(record)
        return record

    def update_general_score(self,
                             title: str,
                             chat_id: str,
                             general_score: float) -> None:
        self.session.query(Watches).filter(Watches.group_id == chat_id, Watches.title == title).update(
            {Watches.general_score: general_score},
            synchronize_session='fetch'
        )

    def delete_watch(self,
                     watches_id_list: List[int]) -> None:
        self.session.query(Watches).filter(Watches.id.in_(watches_id_list)).delete(synchronize_session='fetch')
