from typing import Union

from sqlalchemy.orm.query import Query

from src.model.tables import UserRequests


class UserRequestsRedactor:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def insert_values(self,
                      **kwargs: dict) -> Query:
        record = UserRequests(
            **kwargs
        )
        self.session.add(record)
        return record

    def __update_attribute(self,
                           user: Query,
                           user_requests_attribute: UserRequests,
                           new_value: Union[bool, str, int]) -> None:
        self.session.query(UserRequests).filter(UserRequests.users_id == user.id).update(
            {user_requests_attribute: new_value},
            synchronize_session='fetch'
        )

    def update_add_or_delete(self,
                             user: Query,
                             add_or_delete: bool) -> None:
        self.__update_attribute(user, UserRequests.add_or_delete, add_or_delete)

    def update_message_id(self,
                          user: Query,
                          message_id: str) -> None:
        self.__update_attribute(user, UserRequests.message_id, message_id)

    def update_chosen_user_id(self,
                              user: Query,
                              chosen_user: str) -> None:
        self.__update_attribute(user, UserRequests.chosen_user_id, chosen_user)

    def delete_user_score(self,
                          user: Query) -> None:
        self.__update_attribute(user, UserRequests.user_score, None)

    def update_title(self,
                     user: Query,
                     title: str) -> None:
        self.__update_attribute(user, UserRequests.title, title)

    def update_user_score(self,
                          user: Query,
                          user_score: int) -> None:
        self.__update_attribute(user, UserRequests.user_score, user_score)
