from src.model.tables import Groups


class GroupsReader:

    def __init__(self, alchemist):
        self.session = alchemist.session

    def is_group_registered(self,
                            chat_id: str) -> bool:
        group = self.session.query(Groups).filter(Groups.id == chat_id).first()
        return bool(group)
