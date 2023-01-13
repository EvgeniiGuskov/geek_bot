from database_manager.database_tables.groups_and_users import Groups, Users
from database_manager.database_tables.mustwatches import UserRequests
from database_manager.command_handlers.helpers.database_updater import DatabaseUpdater


class RegisterManager(DatabaseUpdater):
    FILL_DATA = "FILL_DATA"

    def is_group_registered(self,
                            chat_id: str) -> bool:
        group = self.session.query(Groups).filter(Groups.id == chat_id).first()
        return bool(group)

    def is_user_registered(self,
                           chat_id: str,
                           user_id: str) -> bool:
        user = self.session.query(Users).filter(Users.telegram_user_id == user_id, Users.group_id == chat_id).first()
        return bool(user)

    def register_user(self,
                      chat_id: str,
                      user_id: str) -> bool:
        if self.is_user_registered(chat_id, user_id):
            return False
        else:
            if not self.is_group_registered(chat_id):
                self.insert_values(Groups, id=chat_id)
            users_record = self.insert_values(Users, telegram_user_id=user_id, group_id=chat_id)
            self.insert_values(UserRequests, users_id=users_record.id, chosen_user_id=RegisterManager.FILL_DATA,
                               title=RegisterManager.FILL_DATA)
            return True
