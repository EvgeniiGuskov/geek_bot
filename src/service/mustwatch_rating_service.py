from typing import Dict


class MustwatchRatingService:

    def __init__(self, alchemist, watches_read):
        self.watches_read = watches_read
        self.session = alchemist.session

    def get_rated_watches_dict(self,
                               chat_id: str) -> Dict[str, float]:
        watches_dict_items = self.watches_read.get_watches_title_and_score_dict_items(chat_id)
        return dict(watches_dict_items)
