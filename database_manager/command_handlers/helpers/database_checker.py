from sqlalchemy.orm.query import Query

from database_manager.database_tables.groups_and_users import Users
from database_manager.database_tables.mustwatches import UserRequests, Watches, Mustwatches

from telebot_controller.command_handlers.helpers.buttons import Button as btn


class DatabaseChecker:

    def get_list_from_raw_list(self,
                               raw_list: list) -> list:
        return [raw_list[i][0] for i in range(len(raw_list))]

    def get_user_record(self,
                        chat_id: str,
                        user_id: str) -> Query:
        return self.session.query(Users).filter(Users.telegram_user_id == user_id, Users.group_id == chat_id).first()

    def get_user_request(self,
                         chat_id: str,
                         user_id: str) -> Query:
        user = self.get_user_record(chat_id, user_id)
        return self.session.query(UserRequests).filter(UserRequests.users_id == user.id).first()

    def get_same_group_users_id_list(self,
                                     chat_id: str) -> list:
        raw_same_users_list = self.session.query(Users.id).filter(Users.group_id == chat_id).all()
        return self.get_list_from_raw_list(raw_same_users_list)

    def get_chosen_users_id_tuple(self,
                                  chat_id: str,
                                  user_request: Query) -> list:
        chosen_user = user_request.chosen_user_id
        if chosen_user.isdigit():
            return (int(chosen_user),)
        elif chosen_user == btn.ME_BUTTON_CALLBACK:
            return (user_request.users_id,)
        elif chosen_user == btn.ALL_BUTTON_CALLBACK:
            return self.get_same_group_users_id_list(chat_id)

    def get_watch_record(self,
                         title: str,
                         chat_id: str) -> Query:
        return self.session.query(Watches).filter(Watches.title == title, Watches.group_id == chat_id).first()

    def get_watches_id_list_with_same_title(self, title, chat_id):
        raw_watches_id_list = self.session.query(Watches.id).filter(Watches.title == title,
                                                                    Watches.group_id == chat_id).all()
        return self.get_list_from_raw_list(raw_watches_id_list)

    def get_watches_id_list_for_add_to_one_chosen_user(self,
                                                       chosen_user_tuple: tuple) -> list:
        chosen_user_id = chosen_user_tuple[0]
        raw_chosen_user_watches_id = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id == chosen_user_id
        ).all()
        return self.get_list_from_raw_list(raw_chosen_user_watches_id)

    def make_watches_dict_from_watches_id_list(self,
                                               watches_id_list: list) -> dict:
        watches_dict_items = self.session.query(Watches.id, Watches.title).filter(Watches.id.in_(watches_id_list))
        return dict(watches_dict_items)

    def get_watches_dict_for_add_to_one_user(self,
                                             chosen_user_tuple: tuple,
                                             chat_id: str) -> dict:
        same_group_users_id_list = self.get_same_group_users_id_list(chat_id)
        chosen_user_watches_id_list = self.get_watches_id_list_for_add_to_one_chosen_user(chosen_user_tuple)
        raw_watches_id_list = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id.in_(same_group_users_id_list),
            Mustwatches.watches_id.not_in(chosen_user_watches_id_list)
        ).all()
        watches_id_list = self.get_list_from_raw_list(raw_watches_id_list)
        return self.make_watches_dict_from_watches_id_list(watches_id_list)

    def clear_watches_id_list_from_watches_for_all_users(self,
                                                         chosen_user_tuple: tuple,
                                                         same_group_watches_id_list: list) -> list:
        same_group_users_amount = len(chosen_user_tuple)
        watches_id_list = []
        for watch in same_group_watches_id_list:
            if same_group_watches_id_list.count(watch) < same_group_users_amount:
                watches_id_list.append(watch)
        return list(set(watches_id_list))

    def get_watches_id_list_with_same_group_users(self,
                                                  chosen_user_tuple: tuple) -> list:
        raw_same_group_watches_id_list = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id.in_(chosen_user_tuple)
        ).all()
        return self.get_list_from_raw_list(raw_same_group_watches_id_list)

    def get_watches_dict_for_add_to_all_users(self,
                                              chosen_user_tuple: tuple) -> dict:
        same_group_watches_id_list = self.get_watches_id_list_with_same_group_users(chosen_user_tuple)
        watches_id_list = self.clear_watches_id_list_from_watches_for_all_users(chosen_user_tuple,
                                                                                same_group_watches_id_list)
        return self.make_watches_dict_from_watches_id_list(watches_id_list)

    def get_watches_id_list_for_rating_mustwatch(self,
                                                 chosen_user_tuple: tuple) -> list:
        chosen_user_id = chosen_user_tuple[0]
        raw_chosen_user_watches_id = self.session.query(Mustwatches.watches_id).filter(
            Mustwatches.users_id == chosen_user_id,
            Mustwatches.user_score == None
        ).all()
        return self.get_list_from_raw_list(raw_chosen_user_watches_id)

    def get_watches_dict_for_rating_mustwatch(self,
                                              chosen_user_tuple: tuple) -> dict:
        watches_id_list = self.get_watches_id_list_for_rating_mustwatch(chosen_user_tuple)
        return self.make_watches_dict_from_watches_id_list(watches_id_list)

    def get_watches_dict_for_delete_all(self,
                                        chosen_user_tuple: tuple) -> dict:
        watches_id_list = self.get_watches_id_list_with_same_group_users(chosen_user_tuple)
        return self.make_watches_dict_from_watches_id_list(watches_id_list)
