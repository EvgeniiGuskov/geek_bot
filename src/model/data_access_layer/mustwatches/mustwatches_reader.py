from typing import List, Tuple

from sqlalchemy.orm.query import Query

from src.model.tables import Mustwatches


class MustwatchesReader:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def get_watches_id_list_for_chosen_user(self,
                                            chosen_user_tuple: Tuple[int]) -> List[int]:
        chosen_user_id = chosen_user_tuple[0]
        raw_chosen_user_watches_id = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id == chosen_user_id
        ).all()
        return self.__get_list_from_raw_list(raw_chosen_user_watches_id)

    def get_watches_id_list_from_other_group_members(self,
                                                     same_group_users_id_list: List[int],
                                                     chosen_user_watches_id_list: List[int]) -> List[Tuple[int]]:
        raw_list = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id.in_(same_group_users_id_list),
            Mustwatches.watches_id.not_in(chosen_user_watches_id_list)
        ).all()
        return self.__get_list_from_raw_list(raw_list)

    def get_users_id_list_with_chosen_mustwatch(self,
                                                watch_record: Query,
                                                chosen_user_id: Tuple[int, ...]) -> None:
        raw_users_with_chosen_mustwatch = self.session.query(Mustwatches.users_id).filter(
            Mustwatches.watches_id == watch_record.id,
            Mustwatches.users_id.in_(chosen_user_id)).all()
        return self.__get_list_from_raw_list(raw_users_with_chosen_mustwatch)

    def get_watches_id_list_with_same_group_users(self,
                                                  chosen_user_tuple: Tuple[int]) -> List[int]:
        raw_same_group_watches_id_list = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id.in_(chosen_user_tuple)
        ).all()
        return self.__get_list_from_raw_list(raw_same_group_watches_id_list)

    def get_watches_id_list_unrated_mustwatches(self,
                                                chosen_user_tuple: Tuple[int]) -> List[int]:
        chosen_user_id = chosen_user_tuple[0]
        raw_chosen_user_watches_id = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id == chosen_user_id,
            Mustwatches.user_score == None
        ).all()
        return self.__get_list_from_raw_list(raw_chosen_user_watches_id)

    def get_users_scores_list(self,
                              watch_record: Query,
                              same_group_users_id: List[int],
                              ) -> None:
        raw_user_score_list = self.session.query(Mustwatches.user_score).filter(
            Mustwatches.watches_id == watch_record.id,
            Mustwatches.users_id.in_(same_group_users_id),
            Mustwatches.user_score != None
        ).all()
        return self.__get_list_from_raw_list(raw_user_score_list)

    def __get_list_from_raw_list(self,
                                 raw_list: List[Tuple[int]]) -> List[int]:
        return [raw_list[i][0] for i in range(len(raw_list))]
