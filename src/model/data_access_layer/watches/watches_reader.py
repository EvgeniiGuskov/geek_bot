from typing import List, Tuple

from sqlalchemy import desc
from sqlalchemy.orm.query import Query

from src.model.tables import Watches


class WatchesReader:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def get_watch_by_title_and_chat_id(self,
                                       title: str,
                                       chat_id: str) -> Query:
        return self.session.query(Watches).filter(Watches.title == title, Watches.group_id == chat_id).first()

    def get_watches_id_list_with_same_title(self,
                                            title: str,
                                            chat_id: str) -> List[int]:
        raw_watches_id_list = self.session.query(Watches.id).filter(Watches.title == title,
                                                                    Watches.group_id == chat_id).all()
        return self.__get_list_from_raw_list(raw_watches_id_list)

    def get_watches_title_and_score_dict_items(self,
                                               chat_id: str) -> List[Tuple[str, float]]:
        return self.session.query(Watches.title, Watches.general_score).filter(
            Watches.group_id == chat_id,
            Watches.general_score != None
        ).order_by(desc(Watches.general_score))

    def get_id_and_title_dict_items(self,
                                    watches_id_list: List[int]):
        return self.session.query(Watches.id, Watches.title).filter(Watches.id.in_(watches_id_list))

    def get_watch_by_id(self,
                        chosen_title_id: int) -> Query:
        return self.session.query(Watches).get(chosen_title_id)

    def __get_list_from_raw_list(self,
                                 raw_list: List[Tuple[int]]) -> List[int]:
        return [raw_list[i][0] for i in range(len(raw_list))]
