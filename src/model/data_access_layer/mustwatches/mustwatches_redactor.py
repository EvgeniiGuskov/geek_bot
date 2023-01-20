from typing import List

from sqlalchemy.orm.query import Query

from src.model.tables import Mustwatches


class MustwatchesRedactor:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def insert_values(self,
                      **kwargs: dict) -> Query:
        record = Mustwatches(
            **kwargs
        )
        self.session.add(record)
        return record

    def update_user_score(self,
                          users_id: int,
                          watch_record: Query,
                          user_score: int) -> None:
        self.session.query(Mustwatches).filter(
            Mustwatches.users_id == users_id,
            Mustwatches.watches_id == watch_record.id
        ).update({Mustwatches.user_score: user_score}, synchronize_session='fetch')

    def delete_mustwatch(self,
                         watches_id_list: List[int]) -> None:
        self.session.query(Mustwatches).filter(Mustwatches.watches_id.in_(watches_id_list)).delete(
            synchronize_session='fetch')
