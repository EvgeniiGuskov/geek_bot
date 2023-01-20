class RegisterService:
    FILL_DATA = "FILL_DATA"

    def __init__(self, alchemist, groups_read, users_read, groups_redact, users_redact, user_requests_redact):
        self.groups_read = groups_read
        self.users_read = users_read
        self.groups_redact = groups_redact
        self.users_redact = users_redact
        self.user_requests_redact = user_requests_redact
        self.session = alchemist.session

    def register_user(self,
                      chat_id: str,
                      user_id: str) -> bool:
        try:
            if not self.users_read.is_user_registered(chat_id, user_id):
                if not self.groups_read.is_group_registered(chat_id):
                    self.groups_redact.insert_values(id=chat_id)
                users_record = self.users_redact.insert_values(telegram_user_id=user_id,
                                                               group_id=chat_id
                                                               )
                self.user_requests_redact.insert_values(
                    users_id=users_record.id,
                    chosen_user_id=RegisterService.FILL_DATA,
                    title=RegisterService.FILL_DATA
                )
            self.session.commit()
        except:
            self.session.rollback()
