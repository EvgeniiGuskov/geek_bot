from sqlalchemy.orm.query import Query

from config.database.tables import Groups, Users, UserRequests, Watches, Mustwatches
from typing import List, Tuple, Dict

from src.view.buttons import Button as btn


class DatabaseChecker:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def __get_list_from_raw_list(self,
                                 raw_list: List[Tuple[int]]) -> List[int]:
        return [raw_list[i][0] for i in range(len(raw_list))]

    def is_user_registered(self,
                           chat_id: str,
                           user_id: str) -> bool:
        user = self.session.query(Users).filter(Users.telegram_user_id == user_id, Users.group_id == chat_id).first()
        return bool(user)

    def is_group_registered(self,
                            chat_id: str) -> bool:
        group = self.session.query(Groups).filter(Groups.id == chat_id).first()
        return bool(group)

    def get_user_record(self,
                        chat_id: str,
                        user_id: str) -> Query:
        return self.session.query(Users).filter(Users.telegram_user_id == user_id, Users.group_id == chat_id).first()

    def get_user_request(self,
                         chat_id: str,
                         user_id: str) -> Query:
        user = self.get_user_record(chat_id, user_id)
        return self.session.query(UserRequests).filter(UserRequests.users_id == user.id).first()

    def is_title_filled_at_user_request(self,
                                        chat_id: str,
                                        user_id: str) -> bool:
        user_request = self.get_user_request(chat_id, user_id)
        return bool(user_request.title)

    def get_add_or_delete(self,
                          chat_id: str,
                          user_id: str) -> bool:
        user_request = self.get_user_request(chat_id, user_id)
        return user_request.add_or_delete

    def get_title_from_user_request(self,
                                    chat_id: str,
                                    user_id: str) -> str:
        user_request = self.get_user_request(chat_id, user_id)
        return user_request.title

    def get_user_score_from_user_request(self,
                                         chat_id: str,
                                         user_id: str) -> int:
        user_request = self.get_user_request(chat_id, user_id)
        return user_request.user_score

    def get_same_group_users_id_list(self,
                                     chat_id: str) -> List[int]:
        raw_same_users_list = self.session.query(Users.id).filter(Users.group_id == chat_id).all()
        return self.__get_list_from_raw_list(raw_same_users_list)

    def get_same_group_users_dict_items(self,
                                        user: Query) -> List[Tuple[int, str]]:
        return self.session.query(Users.id, Users.telegram_user_id).filter(
            Users.group_id == user.group_id,
            Users.telegram_user_id != user.telegram_user_id)

    def get_watch_record(self,
                         title: str,
                         chat_id: str) -> Query:
        return self.session.query(Watches).filter(Watches.title == title, Watches.group_id == chat_id).first()

    def get_watches_id_list_with_same_title(self,
                                            title: str,
                                            chat_id: str) -> List[int]:
        raw_watches_id_list = self.session.query(Watches.id).filter(Watches.title == title,
                                                                    Watches.group_id == chat_id).all()
        return self.__get_list_from_raw_list(raw_watches_id_list)

    def get_watches_id_list_for_add_to_one_chosen_user(self,
                                                       chosen_user_tuple: Tuple[int]) -> List[int]:
        chosen_user_id = chosen_user_tuple[0]
        raw_chosen_user_watches_id = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id == chosen_user_id
        ).all()
        return self.__get_list_from_raw_list(raw_chosen_user_watches_id)

    def get_watches_id_list_for_add_to_one_user(self,
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

    def get_watches_id_list_for_rating_mustwatch(self,
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
