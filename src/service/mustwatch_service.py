from typing import Tuple, Dict, List

from sqlalchemy.orm.query import Query
from telebot.types import CallbackQuery

from src.service.register_service import RegisterService
from src.view.buttons import Button


class MustwatchService:

    def __init__(self, alchemist, users_read, user_requests_read, watches_read, mustwatches_read, watches_redact,
                 user_requests_redact, mustwatches_redact):
        self.users_read = users_read
        self.user_requests_read = user_requests_read
        self.watches_read = watches_read
        self.mustwatches_read = mustwatches_read
        self.watches_redact = watches_redact
        self.user_requests_redact = user_requests_redact
        self.mustwatches_redact = mustwatches_redact
        self.session = alchemist.session

    def prepare_user_request(self,
                             chat_id: str,
                             user_id: str,
                             message_id: str) -> None:
        try:
            user = self.users_read.get_user(chat_id, user_id)
            self.user_requests_redact.update_message_id(user, message_id)
            self.user_requests_redact.update_title(user, RegisterService.FILL_DATA)
            self.user_requests_redact.delete_user_score(user)
            self.session.commit()
        except:
            self.session.rollback()

    def is_callback_protected_from_intruder(self,
                                            chat_id: str,
                                            user_id: str,
                                            message_id: str) -> bool:
        user = self.users_read.get_user(chat_id, user_id)
        is_same_user_and_message = bool(self.user_requests_read.get_record_by_users_and_message_ids(user, message_id))
        return is_same_user_and_message

    def update_user_request_title_transaction(self,
                                              chat_id: str,
                                              user_id: str,
                                              title: str) -> None:
        try:
            user = self.users_read.get_user(chat_id, user_id)
            self.user_requests_redact.update_title(user, title)
            self.session.commit()
        except:
            self.session.rollback()

    def is_user_registered_and_title_is_not_filled(self,
                                                   chat_id: str,
                                                   user_id: str) -> bool:
        return self.users_read.is_user_registered(chat_id, user_id) and not self.__is_title_filled_at_user_request(
            chat_id, user_id)

    def update_user_request_chosen_title(self,
                                         chat_id: str,
                                         user_id: str,
                                         chosen_title_id: int) -> None:
        watch = self.watches_read.get_watch_by_id(chosen_title_id)
        try:
            user = self.users_read.get_user(chat_id, user_id)
            self.user_requests_redact.update_title(user, watch.title)
            self.session.commit()
        except:
            self.session.rollback()

    def update_user_request_add_or_delete_and_chosen_user(self,
                                                          chat_id: str,
                                                          user_id: str,
                                                          user_callback: str) -> None:
        try:
            user = self.users_read.get_user(chat_id, user_id)
            if user_callback == Button.ADD_BUTTON_CALLBACK:
                self.user_requests_redact.update_add_or_delete(user, True)
            else:
                self.user_requests_redact.update_add_or_delete(user, False)
                if user_callback == Button.DELETE_BUTTON_CALLBACK:
                    self.user_requests_redact.update_chosen_user_id(user, Button.ALL_BUTTON_CALLBACK)
                elif user_callback == Button.SHOW_MUSTWATCHES_BUTTON_CALLBACK:
                    self.user_requests_redact.update_chosen_user_id(user, Button.ME_BUTTON_CALLBACK)
            self.session.commit()
        except:
            self.session.rollback()

    def update_user_request_chosen_user_id_transaction(self,
                                                       chat_id: str,
                                                       user_id: str,
                                                       chosen_user: str) -> None:
        try:
            user = self.users_read.get_user(chat_id, user_id)
            self.user_requests_redact.update_chosen_user_id(user, chosen_user)
            self.session.commit()
        except:
            self.session.rollback()

    def update_user_request_user_score_transaction(self,
                                                   chat_id: str,
                                                   user_id: str,
                                                   user_score: str) -> None:
        try:
            user = self.users_read.get_user(chat_id, user_id)
            self.user_requests_redact.update_user_score(user, int(user_score))
            self.session.commit()
        except:
            self.session.rollback()

    def get_users_dict(self,
                       chat_id: str,
                       user_id: str) -> Dict[int, str]:
        user = self.users_read.get_user(chat_id, user_id)
        same_group_users = self.users_read.get_same_group_users_dict_items(user)
        return dict(same_group_users)

    def delete_title_from_user_request(self,
                                       chat_id: str,
                                       user_id: str) -> None:
        try:
            user = self.users_read.get_user(chat_id, user_id)
            self.user_requests_redact.update_title(user, None)
            self.session.commit()
        except:
            self.session.rollback()

    def get_user_request_values(self,
                                chat_id: str,
                                user_id: str) -> Tuple[bool, str, int]:
        user_request = self.__get_user_request(chat_id, user_id)
        return user_request.add_or_delete, user_request.title, user_request.user_score

    def get_chosen_user_from_user_request(self,
                                          chat_id: str,
                                          user_id: str) -> str:
        user_request = self.__get_user_request(chat_id, user_id)
        chosen_user_id = user_request.chosen_user_id
        if chosen_user_id.isdigit():
            chosen_user_id = int(chosen_user_id)
            user = self.users_read.get_user_by_id(chosen_user_id)
            chosen_user_id = user.telegram_user_id
        return chosen_user_id

    def get_message_id_from_user_request(self,
                                         chat_id: str,
                                         user_id: str) -> int:
        user_request = self.__get_user_request(chat_id, user_id)
        return int(user_request.message_id)

    def get_watches_dict(self,
                         chat_id: str,
                         user_id: str) -> Dict[int, str]:
        add_or_delete = self.__get_add_or_delete(chat_id, user_id)
        user_request = self.__get_user_request(chat_id, user_id)
        chosen_user_tuple = self.__get_chosen_users_id_tuple(chat_id, user_request)
        chosen_user_tuple_len = len(chosen_user_tuple)
        if add_or_delete:
            if chosen_user_tuple_len == 1:
                return self.__get_watches_dict_for_add_to_one_user(chosen_user_tuple, chat_id)
            elif chosen_user_tuple_len > 1:
                return self.__get_watches_dict_for_add_to_all_users(chosen_user_tuple)
        else:
            if chosen_user_tuple_len == 1:
                return self.__get_watches_dict_for_rating_mustwatch(chosen_user_tuple)
            elif chosen_user_tuple_len > 1:
                return self.__get_watches_dict_for_delete_all(chosen_user_tuple)
        return dict()

    def execute_user_request(self,
                             call: CallbackQuery,
                             chat_id: str,
                             user_id: str) -> bool:
        user_request = self.__get_user_request(chat_id, user_id)
        add_or_delete, title, user_score = user_request.add_or_delete, user_request.title, user_request.user_score
        chosen_user_id = self.__get_chosen_users_id_tuple(chat_id, user_request)
        is_user_confirmed_request = call.data == Button.CONFIRM_USER_REQUEST_BUTTON_CALLBACK
        try:
            user = self.users_read.get_user(chat_id, user_id)
            self.user_requests_redact.delete_user_score(user)
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

    def __clear_watches_id_list_from_watches_for_all_users(self,
                                                           chosen_user_tuple: Tuple[int],
                                                           same_group_watches_id_list: List[int]) -> List[int]:
        same_group_users_amount = len(chosen_user_tuple)
        watches_id_list = []
        for watch in same_group_watches_id_list:
            if same_group_watches_id_list.count(watch) < same_group_users_amount:
                watches_id_list.append(watch)
        return list(set(watches_id_list))

    def __make_watches_dict_from_watches_id_list(self,
                                                 watches_id_list: List[int]) -> Dict[int, str]:
        watches_dict_items = self.watches_read.get_id_and_title_dict_items(watches_id_list)
        return dict(watches_dict_items)

    def __get_watches_dict_for_add_to_one_user(self,
                                               chosen_user_tuple: Tuple[int],
                                               chat_id: str) -> Dict[int, str]:
        same_group_users_id_list = self.users_read.get_same_group_users_id_list(chat_id)
        chosen_user_watches_id_list = self.mustwatches_read.get_watches_id_list_for_chosen_user(chosen_user_tuple)
        watches_id_list = self.mustwatches_read.get_watches_id_list_from_other_group_members(same_group_users_id_list,
                                                                                             chosen_user_watches_id_list)
        return self.__make_watches_dict_from_watches_id_list(watches_id_list)

    def __get_watches_dict_for_add_to_all_users(self,
                                                chosen_user_tuple: Tuple[int]) -> Dict[int, str]:
        same_group_watches_id_list = self.mustwatches_read.get_watches_id_list_with_same_group_users(chosen_user_tuple)
        watches_id_list = self.__clear_watches_id_list_from_watches_for_all_users(chosen_user_tuple,
                                                                                  same_group_watches_id_list)
        return self.__make_watches_dict_from_watches_id_list(watches_id_list)

    def __get_watches_dict_for_rating_mustwatch(self,
                                                chosen_user_tuple: Tuple[int]) -> Dict[int, str]:
        watches_id_list = self.mustwatches_read.get_watches_id_list_unrated_mustwatches(chosen_user_tuple)
        return self.__make_watches_dict_from_watches_id_list(watches_id_list)

    def __get_watches_dict_for_delete_all(self,
                                          chosen_user_tuple: Tuple[int]) -> Dict[int, str]:
        watches_id_list = self.mustwatches_read.get_watches_id_list_with_same_group_users(chosen_user_tuple)
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
            return tuple(self.users_read.get_same_group_users_id_list(chat_id))
        else:
            return tuple()

    def __add_mustwatch_to_tables(self,
                                  title: str,
                                  chosen_user_id: Tuple[int, ...],
                                  chat_id: str) -> None:
        watch_record = self.watches_read.get_watch_by_title_and_chat_id(title, chat_id)
        if not watch_record:
            self.watches_redact.create_watch(title=title, group_id=chat_id)
            watch_record = self.watches_read.get_watch_by_title_and_chat_id(title, chat_id)
        users_with_chosen_mustwatch = self.mustwatches_read.get_users_id_list_with_chosen_mustwatch(watch_record,
                                                                                                    chosen_user_id)
        for users_id in chosen_user_id:
            if users_id not in users_with_chosen_mustwatch:
                self.mustwatches_redact.create_mustwatch(watches_id=watch_record.id, users_id=users_id)

    def __update_watches_general_score(self,
                                       title: str,
                                       chat_id: str) -> None:
        same_group_users_id = self.users_read.get_same_group_users_id_list(chat_id)
        watch_record = self.watches_read.get_watch_by_title_and_chat_id(title, chat_id)
        users_score_list = self.mustwatches_read.get_users_scores_list(watch_record, same_group_users_id)
        general_score = round(sum(users_score_list) / len(users_score_list), 1)
        self.watches_redact.update_general_score(title, chat_id, general_score)

    def __update_user_score(self,
                            title: str,
                            chat_id: str,
                            chosen_user_id: str,
                            user_score: int) -> None:
        users_id = chosen_user_id[0]
        watch_record = self.watches_read.get_watch_by_title_and_chat_id(title, chat_id)
        self.mustwatches_redact.update_user_score(users_id, watch_record, user_score)

    def __delete_mustwatches_and_watches(self,
                                         title: str,
                                         chat_id: str) -> None:
        watches_id_list = self.watches_read.get_watches_id_list_with_same_title(title, chat_id)
        self.mustwatches_redact.delete_mustwatch(watches_id_list)
        self.watches_redact.delete_watch(watches_id_list)

    def __get_user_request(self,
                           chat_id: str,
                           user_id: str) -> Query:
        user = self.users_read.get_user(chat_id, user_id)
        return self.user_requests_read.get_user_request(user)

    def __is_title_filled_at_user_request(self,
                                          chat_id: str,
                                          user_id: str) -> bool:
        user_request = self.__get_user_request(chat_id, user_id)
        return bool(user_request.title)

    def __get_add_or_delete(self,
                            chat_id: str,
                            user_id: str) -> bool:
        user_request = self.__get_user_request(chat_id, user_id)
        return user_request.add_or_delete
