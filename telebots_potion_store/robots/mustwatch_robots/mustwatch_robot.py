from telebots_potion_store.robots.nanobots.inline_markup_nanobot import InlineMarkupNanobot
from telebots_potion_store.robots.nanobots.message_editor_nanobot import MessageEditorNanobot
from telebots_potion_store.robots.mustwatch_robots.add_mustwatch import AddMustwatchRobot


class MustwatchRobot(AddMustwatchRobot, InlineMarkupNanobot, MessageEditorNanobot):
    __USER_IS_NOT_REGISTERED_MESSAGE = "Пользователь не зарегистрирован!"
    __ADD_OR_DELETE_MESSAGE = "Удалить или добавить маствотч?"
    __ADD_NEW_OR_TAKE_FROM_DATABASE = "Добавить новый маствотч или взять из группы?"

    async def start_conversation_with_user(self, message, register_state):
        if not register_state:
            await self.bot.reply_to(message,
                                    MustwatchRobot.__USER_IS_NOT_REGISTERED_MESSAGE)
        else:
            await self.bot.reply_to(message,
                                    MustwatchRobot.__ADD_OR_DELETE_MESSAGE,
                                    reply_markup=self.markup_add_or_delete_item())

    async def add_or_delete_item_response(self, call):
        if call.data == InlineMarkupNanobot.DELETE_BUTTON[1]:
            pass
        if call.data == InlineMarkupNanobot.ADD_BUTTON[1]:
            await self.edit_message_to_add_new_or_take_from_db_buttons(call)

    async def add_new_or_take_from_db_response(self, call):
        if call.data == InlineMarkupNanobot.ADD_NEW_MUSTWATCH_BUTTON[1]:
            await self.edit_message_to_whom_add_item_buttons(call)
        if call.data == InlineMarkupNanobot.TAKE_MUSWATCH_FROM_DB_BUTTON[1]:
            pass

    def get_user_data_from_to_me_call(self, call):
        if call.data == self.TO_ME_BUTTON[1]:
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            return chat_id, user_id

    async def add_or_delete_somebodies_item_response(self, call):
        if call.data == InlineMarkupNanobot.TO_ALL_BUTTON[1]:
            pass
        if call.data == InlineMarkupNanobot.TO_ME_BUTTON[1]:
            await self.edit_message_to_choose_item_kind(call)
        if call.data == InlineMarkupNanobot.TO_USER_BUTTON[1]:
            pass

    async def choose_item_kind_response(self, call):
        if call.data in (InlineMarkupNanobot.ANIMATION_BUTTON[1], InlineMarkupNanobot.CINEMA_BUTTON[1]):
            await self.edit_message_to_choose_item_timing(call)

    async def choose_item_timing_response(self, call):
        if call.data in (
                InlineMarkupNanobot.SHORT_FILM_BUTTON[1], InlineMarkupNanobot.FULL_FILM_BUTTON[1],
                InlineMarkupNanobot.SERIES_BUTTON[1]):
            await self.edit_message_to_send_item_title(call)
