from typing import Union, Tuple, List, Dict
from sqlalchemy.orm.query import Query

from config.database.tables import Users, UserRequests, Watches, Mustwatches

from src.view.buttons import Button as btn


class DatabaseUpdater:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def insert_values(self,
                      table: Union[Users, UserRequests, Watches, Mustwatches],
                      **kwargs: dict) -> Query:
        record = table(
            **kwargs
        )
        self.session.add(record)
        return record

    def __update_user_request_attribute(self,
                                        user: Query,
                                        user_requests_attribute: UserRequests,
                                        new_value: Union[bool, str, int]) -> None:
        self.session.query(UserRequests).filter(UserRequests.users_id == user.id).update(
            {user_requests_attribute: new_value},
            synchronize_session='fetch'
        )

    def __update_user_request(self,
                              user: Query,
                              user_requests_attribute: UserRequests,
                              new_value: Union[bool, str, int]) -> None:
        self.__update_user_request_attribute(user, user_requests_attribute, new_value)

    def update_user_request_add_or_delete(self,
                                          user: Query,
                                          add_or_delete: bool) -> None:
        self.__update_user_request(user, UserRequests.add_or_delete, add_or_delete)

    def update_user_request_message_id(self,
                                       user: Query,
                                       message_id: str) -> None:
        self.__update_user_request(user, UserRequests.message_id, message_id)

    def update_user_request_chosen_user_id(self,
                                           user: Query,
                                           chosen_user: str) -> None:
        self.__update_user_request(user, UserRequests.chosen_user_id, chosen_user)

    def delete_user_score_from_user_request(self,
                                            user: Query) -> None:
        self.__update_user_request(user, UserRequests.user_score, None)

    def update_user_request_title(self,
                                  user: Query,
                                  title: str) -> None:
        self.__update_user_request(user, UserRequests.title, title)

    def update_user_request_user_score(self,
                                       user: Query,
                                       user_score: int) -> None:
        self.__update_user_request(user, UserRequests.user_score, user_score)