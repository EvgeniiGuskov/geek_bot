from alchemical_lab.database_structure.tables.groups_and_users import Groups, Users
from alchemical_lab.associates_to_the_alchemist.assistants_to_associates.update_database_assistant import \
    UpdateDatabaseAssistant


class RegisterAssociate(UpdateDatabaseAssistant):
    def is_group_registered(self, chat_id):
        group = self.session.query(Groups).filter(Groups.id == chat_id).first()
        return group

    def is_user_registered(self, chat_id, user_id):
        user = self.session.query(Users).filter(Users.user_id == user_id, Users.group_id == chat_id).first()
        return user

    def register_user(self, chat_id, user_id):
        if self.is_user_registered(chat_id, user_id):
            return False
        else:
            if not self.is_group_registered(chat_id):
                self.insert_values(Groups, id=chat_id)
            self.insert_values(Users, user_id=user_id, group_id=chat_id)
            return True
