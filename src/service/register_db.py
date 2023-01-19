from config.database.tables import Groups, Users, UserRequests


class RegisterDb:
    FILL_DATA = "FILL_DATA"

    def __init__(self, alchemist, db_check, db_upd):
        self.db_check = db_check
        self.db_upd = db_upd
        self.session = alchemist.session

    def register_user(self,
                      chat_id: str,
                      user_id: str) -> bool:
        try:
            if not self.db_check.is_user_registered(chat_id, user_id):
                if not self.db_check.is_group_registered(chat_id):
                    self.db_upd.insert_values(Groups, id=chat_id)
                users_record = self.db_upd.insert_values(Users,
                                                         telegram_user_id=user_id,
                                                         group_id=chat_id)
                self.db_upd.insert_values(UserRequests,
                                          users_id=users_record.id,
                                          chosen_user_id=RegisterDb.FILL_DATA,
                                          title=RegisterDb.FILL_DATA)
            self.session.commit()
        except:
            self.session.rollback()
