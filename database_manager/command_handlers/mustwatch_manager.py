from database_manager.database_tables.groups_and_users import Users
from database_manager.database_tables.mustwatches import UserRequests, Watches, Mustwatches

from database_manager.command_handlers.helpers.database_updater import DatabaseUpdater

from telebot_controller.command_handlers.helpers.buttons import Button as btn


class MustwatchManager(DatabaseUpdater):
    def __get_user_record(self, chat_id, user_id):
        return self.session.query(Users).filter(Users.telegram_user_id == user_id, Users.group_id == chat_id).first()

    def __get_user_request(self, chat_id, user_id):
        user = self.__get_user_record(chat_id, user_id)
        return self.session.query(UserRequests).filter(UserRequests.users_id == user.id).first()

    def __update_user_request_attribute(self, user, user_requests_attribute, new_value):
        self.session.query(UserRequests).filter(UserRequests.users_id == user.id).update(
            {user_requests_attribute: new_value},
            synchronize_session='fetch'
        )

    def __update_user_request(self, user_requests_attribute, chat_id, user_id, new_value):
        user = self.__get_user_record(chat_id, user_id)
        self.__update_user_request_attribute(user, user_requests_attribute, new_value)
        self.session.commit()

    def is_callback_protected_from_intruder(self, chat_id, user_id, message_id):
        user = self.__get_user_record(chat_id, user_id)
        is_same_user_and_message = bool(self.session.query(UserRequests).filter(
            UserRequests.users_id == user.id,
            UserRequests.message_id == message_id
        ).first())
        return is_same_user_and_message

    def get_add_or_delete(self, chat_id, user_id):
        user_request = self.__get_user_request(chat_id, user_id)
        return user_request.add_or_delete

    def is_title_filled_at_user_request(self, chat_id, user_id):
        user_request = self.__get_user_request(chat_id, user_id)
        return bool(user_request.title)

    def update_user_request_message_id(self, chat_id, user_id, message_id):
        self.__update_user_request(UserRequests.message_id, chat_id, user_id, message_id)

    def __update_user_request_add_or_delete(self, chat_id, user_id, chosen_action_on_mustwatch):
        if chosen_action_on_mustwatch == btn.ADD_BUTTON_CALLBACK:
            self.__update_user_request(UserRequests.add_or_delete, chat_id, user_id, True)
        else:
            self.__update_user_request(UserRequests.add_or_delete, chat_id, user_id, False)

    def __update_user_request_chosen_user(self, chat_id, user_id, chosen_action_on_mustwatch):
        if chosen_action_on_mustwatch == btn.DELETE_BUTTON_CALLBACK:
            self.__update_user_request(UserRequests.chosen_user_id, chat_id, user_id, btn.ALL_BUTTON_CALLBACK)
        elif chosen_action_on_mustwatch == btn.HAS_WATCHED_BUTTON_CALLBACK:
            self.__update_user_request(UserRequests.chosen_user_id, chat_id, user_id, btn.ME_BUTTON_CALLBACK)

    def update_user_request_add_or_delete_and_chosen_user(self, chat_id, user_id, chosen_action_on_mustwatch):
        self.__update_user_request_add_or_delete(chat_id, user_id, chosen_action_on_mustwatch)
        self.__update_user_request_chosen_user(chat_id, user_id, chosen_action_on_mustwatch)

    def update_user_request_chosen_user(self, chat_id, user_id, chosen_user):
        self.__update_user_request(UserRequests.chosen_user_id, chat_id, user_id, chosen_user)

    def get_users_dict(self, chat_id, user_id):
        user = self.__get_user_record(chat_id, user_id)
        same_group_users = self.session.query(Users.id, Users.telegram_user_id).filter(
            Users.group_id == user.group_id,
            Users.telegram_user_id != user.telegram_user_id
        )
        return dict(same_group_users)

    def delete_title_from_user_request(self, chat_id, user_id):
        self.__update_user_request(UserRequests.title, chat_id, user_id, None)

    def delete_user_score_from_user_request(self, chat_id, user_id):
        self.__update_user_request(UserRequests.user_score, chat_id, user_id, None)

    def update_user_request_title(self, chat_id, user_id, title):
        self.__update_user_request(UserRequests.title, chat_id, user_id, title)

    def get_user_request_values(self, chat_id, user_id):
        user_request = self.__get_user_request(chat_id, user_id)
        raw_chosen_user = user_request.chosen_user_id
        if raw_chosen_user.isalpha():
            chosen_user = raw_chosen_user
        else:
            chosen_user = self.session.query(Users).get(int(raw_chosen_user)).telegram_user_id
        return user_request.add_or_delete, user_request.title, chosen_user

    def get_message_id_from_user_request(self, chat_id, user_id):
        user_request = self.__get_user_request(chat_id, user_id)
        return int(user_request.message_id)

    def __get_same_users_id_tuple(self, chat_id):
        return self.session.query(Users.id).filter(Users.group_id == chat_id).all()

    def __get_chosen_users_id_tuple(self, chat_id, user_request):
        chosen_user = user_request.chosen_user_id
        if chosen_user.isdigit():
            return (int(chosen_user),)
        elif chosen_user == btn.ME_BUTTON_CALLBACK:
            return (user_request.users_id,)
        elif chosen_user == btn.ALL_BUTTON_CALLBACK:
            return self.__get_same_users_id_tuple(chat_id)

    def __get_watch_record(self, title, chat_id):
        return self.session.query(Watches).filter(Watches.title == title, Watches.group_id == chat_id).first()

    def __add_mustwatch_to_tables(self, title, chosen_user_id, chat_id):
        watch_record = self.__get_watch_record(title, chat_id)
        if not watch_record:
            self.insert_values(Watches, title=title, group_id=chat_id)
            watch_record = self.__get_watch_record(title, chat_id)
        for users_id in chosen_user_id:
            is_mustwatch_present = bool(
                self.session.query(Mustwatches).filter(Mustwatches.watches_id == watch_record.id,
                                                       Mustwatches.users_id == users_id).first())
            if not is_mustwatch_present:
                self.insert_values(Mustwatches, watches_id=watch_record.id, users_id=users_id)

    def __update_watches_general_score(self, title, chat_id):
        same_group_users_id = self.__get_same_users_id_tuple(chat_id)
        watch_record = self.__get_watch_record(title, chat_id)
        same_title_mustwatches = self.session.query(Mustwatches).filter(
            Mustwatches.watches_id == watch_record.id,
            Mustwatches.users_id in same_group_users_id
        )
        users_score_list = [mustwatch.user_score for mustwatch in same_title_mustwatches]
        general_score = sum(users_score_list) / len(users_score_list)
        self.session.query(Watches).filter(Watches.group_id == chat_id, Watches.title == title).update(
            {Watches.general_score: general_score},
            synchronize_session='fetch'
        )
        self.session.commit()

    def __update_user_score(self, title, chat_id, chosen_user_id, user_score):
        users_id = chosen_user_id[0]
        watch_record = self.__get_watch_record(title, chat_id)
        self.session.query(Mustwatches).filter(
            Mustwatches.users_id == users_id,
            Mustwatches.watches_id == watch_record.id
        ).update({Mustwatches.user_score: user_score}, synchronize_session='fetch')
        self.session.commit()

    def __get_watches_id_list(self, title, chat_id):
        return self.session.query(Watches).filter(Watches.title == title, Watches.group_id == chat_id).all()

    def __delete_mustwatches_and_watches(self, title, chat_id):
        watch_id_list = self.__get_watches_id_list(title, chat_id)
        self.session.query(Mustwatches).filter(Mustwatches.watches_id in watch_id_list).delete(
            synchronize_session='fetch')
        self.session.commit()
        self.session.query(Watches).filter(Watches.id in watch_id_list).delete(synchronize_session='fetch')
        self.session.commit()

    def execute_user_request(self, call, chat_id, user_id):
        user_request = self.__get_user_request(chat_id, user_id)
        add_or_delete, title, user_score = user_request.add_or_delete, user_request.title, user_request.user_score
        chosen_user_id = self.__get_chosen_users_id_tuple(chat_id, user_request)
        is_user_confirmed_request = call.data == btn.CONFIRM_USER_REQUEST_BUTTON_CALLBACK
        self.delete_user_score_from_user_request(chat_id, user_id)
        if add_or_delete:
            if is_user_confirmed_request:
                self.__add_mustwatch_to_tables(title, chosen_user_id, chat_id)
        else:
            if is_user_confirmed_request:
                if user_score is None:
                    self.__delete_mustwatches_and_watches(title, chat_id)
                else:
                    self.__update_user_score(title, chat_id, chosen_user_id, user_score)
                    self.__update_watches_general_score(title, chat_id)
        return True
