from telebot.types import Message
from telebot_controller.command_handlers.helpers.user_data_collector import UserDataCollector


class MustwatchRatingHandler(UserDataCollector):
    __NO_RATED_MUSTWATCHES_MESSAGE = "В этой группе пока никто не оценил маствотчи..."

    def __make_bot_message_mustwatches_rating(self, watches_dict: dict) -> str:
        bot_message = ""
        for key in watches_dict:
            bot_message += str(watches_dict[key]) + " — " + key + "\n"
        return bot_message

    async def send_mustwatches_rating(self, message: Message, watches_dict: dict) -> None:
        bot_message = self.__make_bot_message_mustwatches_rating(watches_dict)
        if not bot_message:
            bot_message = MustwatchRatingHandler.__NO_RATED_MUSTWATCHES_MESSAGE
        await self.bot.send_message(message.chat.id, bot_message)
