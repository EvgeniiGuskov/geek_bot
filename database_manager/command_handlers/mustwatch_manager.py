from sqlalchemy import desc
from database_manager.database_tables.groups_and_users import Users
from database_manager.database_tables.mustwatches import UserRequests, Watches, Mustwatches

from database_manager.command_handlers.helpers.database_updater import DatabaseUpdater
from database_manager.command_handlers.helpers.database_checker import DatabaseChecker

from telebot.types import CallbackQuery
from telebot_controller.command_handlers.helpers.buttons import Button as btn
from database_manager.command_handlers.register_manager import RegisterManager


class MustwatchManager(DatabaseUpdater, DatabaseChecker):

    def is_callback_protected_from_intruder(self,
                                            chat_id: str,
                                            user_id: str,
                                            message_id: str) -> bool:
        user = self.get_user_record(chat_id, user_id)
        is_same_user_and_message = bool(self.session.query(UserRequests).filter(
            UserRequests.users_id == user.id,
            UserRequests.message_id == message_id
        ).first())
        return is_same_user_and_message

    def get_add_or_delete(self,
                          chat_id: str,
                          user_id: str) -> bool:
        user_request = self.get_user_request(chat_id, user_id)
        return user_request.add_or_delete

    def is_title_filled_at_user_request(self,
                                        chat_id: str,
                                        user_id: str) -> bool:
        user_request = self.get_user_request(chat_id, user_id)
        return bool(user_request.title)

    def update_user_request_title(self,
                                  chat_id: str,
                                  user_id: str,
                                  title: str) -> None:
        self.update_user_request(UserRequests.title, chat_id, user_id, title)

    def update_user_request_chosen_title(self,
                                         chat_id: str,
                                         user_id: str,
                                         chosen_title_id: int) -> None:
        watch = self.session.query(Watches).get(chosen_title_id)
        self.update_user_request_title(chat_id, user_id, watch.title)

    def prepare_user_request(self,
                             chat_id: str,
                             user_id: str,
                             message_id: str) -> None:
        self.update_user_request_message_id(chat_id, user_id, message_id)
        self.update_user_request_title(chat_id, user_id, RegisterManager.FILL_DATA)
        self.delete_user_score_from_user_request(chat_id, user_id)

    def update_user_request_add_or_delete_and_chosen_user(self,
                                                          chat_id: str,
                                                          user_id: str,
                                                          chosen_action_on_mustwatch: str) -> None:
        self.update_user_request_add_or_delete(chat_id, user_id, chosen_action_on_mustwatch)
        self.update_user_request_chosen_user_from_chosen_action(chat_id, user_id, chosen_action_on_mustwatch)

    def update_user_request_chosen_user(self,
                                        chat_id: str,
                                        user_id: str,
                                        chosen_user: str) -> None:
        self.update_user_request(UserRequests.chosen_user_id, chat_id, user_id, chosen_user)

    def update_user_request_user_score(self,
                                       chat_id: str,
                                       user_id: str,
                                       user_score: str) -> None:
        self.update_user_request(UserRequests.user_score, chat_id, user_id, int(user_score))

    def get_users_dict(self,
                       chat_id: str,
                       user_id: str) -> dict:
        user = self.get_user_record(chat_id, user_id)
        same_group_users = self.session.query(Users.id, Users.telegram_user_id).filter(
            Users.group_id == user.group_id,
            Users.telegram_user_id != user.telegram_user_id
        )
        return dict(same_group_users)

    def delete_title_from_user_request(self,
                                       chat_id: str,
                                       user_id: str) -> None:
        self.update_user_request(UserRequests.title, chat_id, user_id, None)

    def get_user_request_values(self,
                                chat_id: str,
                                user_id: str) -> tuple:
        user_request = self.get_user_request(chat_id, user_id)
        raw_chosen_user = user_request.chosen_user_id
        if raw_chosen_user.isalpha():
            chosen_user = raw_chosen_user
        else:
            chosen_user = self.session.query(Users).get(int(raw_chosen_user)).telegram_user_id
        return user_request.add_or_delete, user_request.title, chosen_user, user_request.user_score

    def get_chosen_user_from_user_request(self,
                                          chat_id: str,
                                          user_id: str) -> str:
        user_request = self.get_user_request(chat_id, user_id)
        return user_request.chosen_user_id

    def get_message_id_from_user_request(self,
                                         chat_id: str,
                                         user_id: str) -> int:
        user_request = self.get_user_request(chat_id, user_id)
        return int(user_request.message_id)

    def get_watches_dict(self,
                         chat_id: str,
                         user_id: str) -> dict:
        add_or_delete = self.get_add_or_delete(chat_id, user_id)
        user_request = self.get_user_request(chat_id, user_id)
        chosen_user_tuple = self.get_chosen_users_id_tuple(chat_id, user_request)
        is_chosen_user_one = len(chosen_user_tuple) == 1
        if add_or_delete:
            if is_chosen_user_one:
                return self.get_watches_dict_for_add_to_one_user(chosen_user_tuple, chat_id)
            else:
                return self.get_watches_dict_for_add_to_all_users(chosen_user_tuple)
        else:
            if is_chosen_user_one:
                return self.get_watches_dict_for_rating_mustwatch(chosen_user_tuple)
            else:
                return self.get_watches_dict_for_delete_all(chosen_user_tuple)

    def execute_user_request(self,
                             call: CallbackQuery,
                             chat_id: str,
                             user_id: str) -> bool:
        user_request = self.get_user_request(chat_id, user_id)
        add_or_delete, title, user_score = user_request.add_or_delete, user_request.title, user_request.user_score
        chosen_user_id = self.get_chosen_users_id_tuple(chat_id, user_request)
        is_user_confirmed_request = call.data == btn.CONFIRM_USER_REQUEST_BUTTON_CALLBACK
        self.delete_user_score_from_user_request(chat_id, user_id)
        if add_or_delete:
            if is_user_confirmed_request:
                self.add_mustwatch_to_tables(title, chosen_user_id, chat_id)
        else:
            if is_user_confirmed_request:
                if user_score == None:
                    self.delete_mustwatches_and_watches(title, chat_id)
                else:
                    self.update_user_score(title, chat_id, chosen_user_id, user_score)
                    self.update_watches_general_score(title, chat_id)
        return True

    def get_rated_watches_dict(self,
                               chat_id: str) -> dict:

        watches_dict_items = self.session.query(Watches.title, Watches.general_score).filter(
            Watches.group_id == chat_id,
            Watches.general_score != None
        ).order_by(desc(Watches.general_score))
        return dict(watches_dict_items)
