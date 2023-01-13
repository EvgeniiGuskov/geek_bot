from typing import Union
from sqlalchemy.orm.query import Query

from database_manager.database_tables.groups_and_users import Users
from database_manager.database_tables.mustwatches import UserRequests, Watches, Mustwatches

from telebot_controller.command_handlers.helpers.buttons import Button as btn


class DatabaseUpdater:

    def update_user_request_attribute(self,
                                      user: Query,
                                      user_requests_attribute: UserRequests,
                                      new_value: Union[bool, str, int]) -> None:
        self.session.query(UserRequests).filter(UserRequests.users_id == user.id).update(
            {user_requests_attribute: new_value},
            synchronize_session='fetch'
        )

    def insert_values(self,
                      table: Union[Users, UserRequests, Watches, Mustwatches],
                      **kwargs: dict) -> Query:
        record = table(
            **kwargs
        )
        self.session.add(record)
        self.session.commit()
        return record

    def update_user_request(self,
                            user_requests_attribute: UserRequests,
                            chat_id: str,
                            user_id: str,
                            new_value: Union[bool, str, int]) -> None:
        user = self.get_user_record(chat_id, user_id)
        self.update_user_request_attribute(user, user_requests_attribute, new_value)
        self.session.commit()

    def update_user_request_message_id(self,
                                       chat_id: str,
                                       user_id: str,
                                       message_id: str) -> None:
        self.update_user_request(UserRequests.message_id, chat_id, user_id, message_id)

    def delete_user_score_from_user_request(self,
                                            chat_id: str,
                                            user_id: str) -> None:
        self.update_user_request(UserRequests.user_score, chat_id, user_id, None)

    def update_user_request_add_or_delete(self,
                                          chat_id: str,
                                          user_id: str,
                                          chosen_action_on_mustwatch: str) -> None:
        if chosen_action_on_mustwatch == btn.ADD_BUTTON_CALLBACK:
            self.update_user_request(UserRequests.add_or_delete, chat_id, user_id, True)
        else:
            self.update_user_request(UserRequests.add_or_delete, chat_id, user_id, False)

    def update_user_request_chosen_user_from_chosen_action(self,
                                                           chat_id: str,
                                                           user_id: str,
                                                           chosen_action_on_mustwatch: str) -> None:
        if chosen_action_on_mustwatch == btn.DELETE_BUTTON_CALLBACK:
            self.update_user_request(UserRequests.chosen_user_id, chat_id, user_id, btn.ALL_BUTTON_CALLBACK)
        elif chosen_action_on_mustwatch == btn.SHOW_MUSTWATCHES_BUTTON_CALLBACK:
            self.update_user_request(UserRequests.chosen_user_id, chat_id, user_id, btn.ME_BUTTON_CALLBACK)

    def add_mustwatch_to_tables(self,
                                title: str,
                                chosen_user_id: str,
                                chat_id: str) -> None:
        watch_record = self.get_watch_record(title, chat_id)
        if not watch_record:
            self.insert_values(Watches, title=title, group_id=chat_id)
            watch_record = self.get_watch_record(title, chat_id)
        for users_id in chosen_user_id:
            is_mustwatch_present = bool(
                self.session.query(Mustwatches).filter(Mustwatches.watches_id == watch_record.id,
                                                       Mustwatches.users_id == users_id).first())
            if not is_mustwatch_present:
                self.insert_values(Mustwatches, watches_id=watch_record.id, users_id=users_id)

    def update_watches_general_score(self,
                                     title: str,
                                     chat_id: str) -> None:
        same_group_users_id = self.get_same_group_users_id_list(chat_id)
        watch_record = self.get_watch_record(title, chat_id)
        raw_user_score_list = self.session.query(Mustwatches.user_score).filter(
            Mustwatches.watches_id == watch_record.id,
            Mustwatches.users_id.in_(same_group_users_id),
            Mustwatches.user_score != None
        ).all()
        users_score_list = self.get_list_from_raw_list(raw_user_score_list)
        general_score = round(sum(users_score_list) / len(users_score_list), 1)
        self.session.query(Watches).filter(Watches.group_id == chat_id, Watches.title == title).update(
            {Watches.general_score: general_score},
            synchronize_session='fetch'
        )
        self.session.commit()

    def update_user_score(self,
                          title: str,
                          chat_id: str,
                          chosen_user_id: str,
                          user_score: int) -> None:
        users_id = chosen_user_id[0]
        watch_record = self.get_watch_record(title, chat_id)
        self.session.query(Mustwatches).filter(
            Mustwatches.users_id == users_id,
            Mustwatches.watches_id == watch_record.id
        ).update({Mustwatches.user_score: user_score}, synchronize_session='fetch')
        self.session.commit()

    def delete_mustwatches_and_watches(self,
                                       title: str,
                                       chat_id: str) -> None:
        watch_id_list = self.get_watches_id_list_with_same_title(title, chat_id)
        self.session.query(Mustwatches).filter(Mustwatches.watches_id.in_(watch_id_list)).delete(
            synchronize_session='fetch')
        self.session.commit()
        self.session.query(Watches).filter(Watches.id.in_(watch_id_list)).delete(synchronize_session='fetch')
        self.session.commit()
