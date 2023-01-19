from typing import Tuple, Dict, List, Union
from config.database.tables import Users, UserRequests, Watches, Mustwatches
from sqlalchemy.orm.query import Query

from src.model.database_updater import DatabaseUpdater
from src.model.database_checker import DatabaseChecker

from telebot.types import CallbackQuery
from src.service.register_db import RegisterDb
from src.view.buttons import Button


class MustwatchDb:

    def __init__(self, alchemist, db_check, db_upd):
        self.db_check = db_check
        self.db_upd = db_upd
        self.session = alchemist.session

    def __make_watches_dict_from_watches_id_list(self,
                                                 watches_id_list: List[int]) -> Dict[int, str]:
        watches_dict_items = self.session.query(Watches.id, Watches.title).filter(Watches.id.in_(watches_id_list))
        return dict(watches_dict_items)

    def __get_watches_dict_for_add_to_one_user(self,
                                               chosen_user_tuple: Tuple[int],
                                               chat_id: str) -> Dict[int, str]:
        same_group_users_id_list = self.db_check.get_same_group_users_id_list(chat_id)
        chosen_user_watches_id_list = self.db_check.get_watches_id_list_for_add_to_one_chosen_user(chosen_user_tuple)
        watches_id_list = self.db_check.get_watches_id_list_for_add_to_one_user(same_group_users_id_list,
                                                                                chosen_user_watches_id_list)
        return self.__make_watches_dict_from_watches_id_list(watches_id_list)

    def __clear_watches_id_list_from_watches_for_all_users(self,
                                                           chosen_user_tuple: Tuple[int],
                                                           same_group_watches_id_list: List[int]) -> List[int]:
        same_group_users_amount = len(chosen_user_tuple)
        watches_id_list = []
        for watch in same_group_watches_id_list:
            if same_group_watches_id_list.count(watch) < same_group_users_amount:
                watches_id_list.append(watch)
        return list(set(watches_id_list))

    def __get_watches_dict_for_add_to_all_users(self,
                                                chosen_user_tuple: Tuple[int]) -> Dict[int, str]:
        same_group_watches_id_list = self.db_check.get_watches_id_list_with_same_group_users(chosen_user_tuple)
        watches_id_list = self.__clear_watches_id_list_from_watches_for_all_users(chosen_user_tuple,
                                                                                  same_group_watches_id_list)
        return self.__make_watches_dict_from_watches_id_list(watches_id_list)

    def __get_watches_dict_for_rating_mustwatch(self,
                                                chosen_user_tuple: Tuple[int]) -> Dict[int, str]:
        watches_id_list = self.db_check.get_watches_id_list_for_rating_mustwatch(chosen_user_tuple)
        return self.__make_watches_dict_from_watches_id_list(watches_id_list)

    def __get_watches_dict_for_delete_all(self,
                                          chosen_user_tuple: Tuple[int]) -> Dict[int, str]:
        watches_id_list = self.db_check.get_watches_id_list_with_same_group_users(chosen_user_tuple)
        return self.__make_watches_dict_from_watches_id_list(watches_id_list)

    def __get_chosen_users_id_tuple(self,
                                    chat_id: str,
                                    user_request: Query) -> Tuple[int]:
        chosen_user = user_request.chosen_user_id
        if chosen_user.isdigit():
            return (int(chosen_user),)
        elif chosen_user == Button.ME_BUTTON_CALLBACK:
            return (user_request.users_id,)
        elif chosen_user == Button.ALL_BUTTON_CALLBACK:
            return tuple(self.db_check.get_same_group_users_id_list(chat_id))

    def __add_mustwatch_to_tables(self,
                                  title: str,
                                  chosen_user_id: Tuple[int, ...],
                                  chat_id: str) -> None:
        watch_record = self.db_check.get_watch_record(title, chat_id)
        if not watch_record:
            self.db_upd.insert_values(Watches, title=title, group_id=chat_id)
            watch_record = self.db_check.get_watch_record(title, chat_id)
        users_with_chosen_mustwatch = self.db_check.get_users_id_list_with_chosen_mustwatch(watch_record,
                                                                                            chosen_user_id)
        for users_id in chosen_user_id:
            if users_id not in users_with_chosen_mustwatch:
                record = Mustwatches(watches_id=watch_record.id, users_id=users_id)
                self.session.add(record)

    def __update_watches_general_score(self,
                                       title: str,
                                       chat_id: str) -> None:
        same_group_users_id = self.db_check.get_same_group_users_id_list(chat_id)
        watch_record = self.db_check.get_watch_record(title, chat_id)
        users_score_list = self.db_check.get_users_scores_list(watch_record, same_group_users_id)
        general_score = round(sum(users_score_list) / len(users_score_list), 1)
        self.session.query(Watches).filter(Watches.group_id == chat_id, Watches.title == title).update(
            {Watches.general_score: general_score},
            synchronize_session='fetch'
        )

    def __update_user_score(self,
                            title: str,
                            chat_id: str,
                            chosen_user_id: str,
                            user_score: int) -> None:
        users_id = chosen_user_id[0]
        watch_record = self.db_check.get_watch_record(title, chat_id)
        self.session.query(Mustwatches).filter(
            Mustwatches.users_id == users_id,
            Mustwatches.watches_id == watch_record.id
        ).update({Mustwatches.user_score: user_score}, synchronize_session='fetch')

    def __delete_mustwatches_and_watches(self,
                                         title: str,
                                         chat_id: str) -> None:
        watch_id_list = self.db_check.get_watches_id_list_with_same_title(title, chat_id)
        self.session.query(Mustwatches).filter(Mustwatches.watches_id.in_(watch_id_list)).delete(
            synchronize_session='fetch')
        self.session.query(Watches).filter(Watches.id.in_(watch_id_list)).delete(synchronize_session='fetch')

    def prepare_user_request(self,
                             chat_id: str,
                             user_id: str,
                             message_id: str) -> None:
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            self.db_upd.update_user_request_message_id(user, message_id)
            self.db_upd.update_user_request_title(user, RegisterDb.FILL_DATA)
            self.db_upd.delete_user_score_from_user_request(user)
            self.session.commit()
        except:
            self.session.rollback()

    def is_callback_protected_from_intruder(self,
                                            chat_id: str,
                                            user_id: str,
                                            message_id: str) -> bool:
        user = self.db_check.get_user_record(chat_id, user_id)
        is_same_user_and_message = bool(self.session.query(UserRequests).filter(
            UserRequests.users_id == user.id,
            UserRequests.message_id == message_id
        ).first())
        return is_same_user_and_message

    def update_user_request_title_transaction(self,
                                              chat_id: str,
                                              user_id: str,
                                              title: str) -> None:
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            self.db_upd.update_user_request_title(user, title)
            self.session.commit()
        except:
            self.session.rollback()

    def is_user_registered_and_title_is_not_filled(self,
                                                   chat_id: str,
                                                   user_id: str) -> bool:
        return self.db_check.is_user_registered(chat_id, user_id) and not self.db_check.is_title_filled_at_user_request(
            chat_id, user_id)

    def update_user_request_chosen_title(self,
                                         chat_id: str,
                                         user_id: str,
                                         chosen_title_id: int) -> None:
        watch = self.session.query(Watches).get(chosen_title_id)
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            self.db_upd.update_user_request_title(user, watch.title)
            self.session.commit()
        except:
            self.session.rollback()

    def update_user_request_add_or_delete_and_chosen_user(self,
                                                          chat_id: str,
                                                          user_id: str,
                                                          user_callback: str) -> None:
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            if user_callback == Button.ADD_BUTTON_CALLBACK:
                self.db_upd.update_user_request_add_or_delete(user, True)
            else:
                self.db_upd.update_user_request_add_or_delete(user, False)
                if user_callback == Button.DELETE_BUTTON_CALLBACK:
                    self.db_upd.update_user_request_chosen_user_id(user, Button.ALL_BUTTON_CALLBACK)
                elif user_callback == Button.SHOW_MUSTWATCHES_BUTTON_CALLBACK:
                    self.db_upd.update_user_request_chosen_user_id(user, Button.ME_BUTTON_CALLBACK)
            self.session.commit()
        except:
            self.session.rollback()

    def update_user_request_chosen_user_id_transaction(self,
                                                       chat_id: str,
                                                       user_id: str,
                                                       chosen_user: str) -> None:
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            self.db_upd.update_user_request_chosen_user_id(user, chosen_user)
            self.session.commit()
        except:
            self.session.rollback()

    def update_user_request_user_score_transaction(self,
                                                   chat_id: str,
                                                   user_id: str,
                                                   user_score: str) -> None:
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            self.db_upd.update_user_request_user_score(user, int(user_score))
            self.session.commit()
        except:
            self.session.rollback()

    def get_users_dict(self,
                       chat_id: str,
                       user_id: str) -> Dict[int, str]:
        user = self.db_check.get_user_record(chat_id, user_id)
        same_group_users = self.db_check.get_same_group_users_dict_items(user)
        return dict(same_group_users)

    def delete_title_from_user_request(self,
                                       chat_id: str,
                                       user_id: str) -> None:
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            self.db_upd.update_user_request_title(user, None)
            self.session.commit()
        except:
            self.session.rollback()

    def get_user_request_values(self,
                                chat_id: str,
                                user_id: str) -> Tuple[bool, str, int, str]:
        user_request = self.db_check.get_user_request(chat_id, user_id)
        return user_request.add_or_delete, user_request.title, user_request.user_score

    def get_chosen_user_from_user_request(self,
                                          chat_id: str,
                                          user_id: str) -> str:
        user_request = self.db_check.get_user_request(chat_id, user_id)
        chosen_user_id = user_request.chosen_user_id
        if chosen_user_id.isdigit():
            chosen_user_id = self.session.query(Users).get(chosen_user_id).telegram_user_id
        return chosen_user_id

    def get_message_id_from_user_request(self,
                                         chat_id: str,
                                         user_id: str) -> int:
        user_request = self.db_check.get_user_request(chat_id, user_id)
        return int(user_request.message_id)

    def get_watches_dict(self,
                         chat_id: str,
                         user_id: str) -> Dict[int, str]:
        add_or_delete = self.db_check.get_add_or_delete(chat_id, user_id)
        user_request = self.db_check.get_user_request(chat_id, user_id)
        chosen_user_tuple = self.__get_chosen_users_id_tuple(chat_id, user_request)
        is_chosen_user_one = len(chosen_user_tuple) == 1
        if add_or_delete:
            if is_chosen_user_one:
                return self.__get_watches_dict_for_add_to_one_user(chosen_user_tuple, chat_id)
            else:
                return self.__get_watches_dict_for_add_to_all_users(chosen_user_tuple)
        else:
            if is_chosen_user_one:
                return self.__get_watches_dict_for_rating_mustwatch(chosen_user_tuple)
            else:
                return self.__get_watches_dict_for_delete_all(chosen_user_tuple)

    def execute_user_request(self,
                             call: CallbackQuery,
                             chat_id: str,
                             user_id: str) -> bool:
        user_request = self.db_check.get_user_request(chat_id, user_id)
        add_or_delete, title, user_score = user_request.add_or_delete, user_request.title, user_request.user_score
        chosen_user_id = self.__get_chosen_users_id_tuple(chat_id, user_request)
        is_user_confirmed_request = call.data == Button.CONFIRM_USER_REQUEST_BUTTON_CALLBACK
        try:
            user = self.db_check.get_user_record(chat_id, user_id)
            self.db_upd.delete_user_score_from_user_request(user)
            if add_or_delete:
                if is_user_confirmed_request:
                    self.__add_mustwatch_to_tables(title, chosen_user_id, chat_id)
            else:
                if is_user_confirmed_request:
                    if user_score == None:
                        self.__delete_mustwatches_and_watches(title, chat_id)
                    else:
                        self.__update_user_score(title, chat_id, chosen_user_id, user_score)
                        self.__update_watches_general_score(title, chat_id)
            self.session.commit()
        except:
            self.session.rollback
