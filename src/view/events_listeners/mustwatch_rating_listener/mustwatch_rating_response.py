from typing import Dict

from src.view.message_text_responses import MessageTextResponse


class MustwatchRatingResponse:

    @staticmethod
    def make_bot_message_mustwatches_rating(watches_dict: Dict[int, str]) -> str:
        bot_message = ""
        for key in watches_dict:
            bot_message += str(watches_dict[key]) + " — " + key + "\n"
        if bot_message == "":
            bot_message = MessageTextResponse.NO_RATED_MUSTWATCHES_MESSAGE
        return bot_message
