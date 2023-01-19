from typing import Dict
from sqlalchemy import desc

from src.model.database_updater import DatabaseUpdater
from src.model.database_checker import DatabaseChecker
from config.database.tables import Groups, Users, UserRequests, Watches, Mustwatches


class MustwatchRatingDb:

    def __init__(self, alchemist, db_check, db_upd):
        self.db_check = db_check
        self.db_upd = db_upd
        self.session = alchemist.session

    def get_rated_watches_dict(self,
                               chat_id: str) -> Dict[str, float]:
        watches_dict_items = self.session.query(Watches.title, Watches.general_score).filter(
            Watches.group_id == chat_id,
            Watches.general_score != None
        ).order_by(desc(Watches.general_score))
        return dict(watches_dict_items)
