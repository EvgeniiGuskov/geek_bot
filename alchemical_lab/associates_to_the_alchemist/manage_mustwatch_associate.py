from sqlalchemy import update

from alchemical_lab.database_structure.tables.groups_and_users import Groups, Users
from alchemical_lab.database_structure.tables.mustwatches import UserRequests

from alchemical_lab.associates_to_the_alchemist.assistants_to_associates.update_database_assistant import \
    UpdateDatabaseAssistant


class ManageMustwatchAssociate(UpdateDatabaseAssistant):
    def update_user_request_with_message_id_and_add_or_delete(self, chat_id, user_id, message_id, add_or_delete):
        user = self.session.query(Users).filter(Users.telegram_user_id == user_id, Users.group_id == chat_id).first()

        self.session.query(UserRequests).filter(UserRequests.users_id == user.id).update(
            {UserRequests.message_id: message_id, UserRequests.add_or_delete: add_or_delete},
            synchronize_session='fetch'
        )

        self.session.commit()
        # добавить take если delete
