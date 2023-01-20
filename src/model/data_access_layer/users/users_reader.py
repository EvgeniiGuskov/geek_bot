from typing import List, Tuple

from sqlalchemy.orm.query import Query

from src.model.tables import Users


class UsersReader:

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

    def get_record(self,
                   chat_id: str,
                   user_id: str) -> Query:
        return self.session.query(Users).filter(Users.telegram_user_id == user_id, Users.group_id == chat_id).first()

    def get_same_group_users_id_list(self,
                                     chat_id: str) -> List[int]:
        raw_same_users_list = self.session.query(Users.id).filter(Users.group_id == chat_id).all()
        return self.__get_list_from_raw_list(raw_same_users_list)

    def get_same_group_users_dict_items(self,
                                        user: Query) -> List[Tuple[int, str]]:
        return self.session.query(Users.id, Users.telegram_user_id).filter(
            Users.group_id == user.group_id,
            Users.telegram_user_id != user.telegram_user_id)

    def get_record_by_id(self,
                         chosen_user_id: int) -> Query:
        return self.session.query(Users).get(chosen_user_id)
