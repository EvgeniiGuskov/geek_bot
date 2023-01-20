from sqlalchemy.orm.query import Query

from src.model.tables import UserRequests


class UserRequestsReader:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def get_record(self,
                   user: Query) -> Query:
        return self.session.query(UserRequests).filter(UserRequests.users_id == user.id).first()

    def get_record_by_users_and_message_ids(self,
                                            user: Query,
                                            message_id: str) -> Query:
        return self.session.query(UserRequests).filter(
            UserRequests.users_id == user.id,
            UserRequests.message_id == message_id
        ).first()
