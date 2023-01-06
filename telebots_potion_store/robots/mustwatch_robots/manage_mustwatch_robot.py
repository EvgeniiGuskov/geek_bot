from telebots_potion_store.robots.nanobots.message_editor_nanobot import MessageEditorNanobot
from telebots_potion_store.robots.nanobots.inline_markup_nanobot import InlineMarkupNanobot


class ManageMustwatchRobot(MessageEditorNanobot):
    __USER_IS_NOT_REGISTERED_MESSAGE = "Чтобы добавить маствотч, вам нужно зарегистрироваться!"
    __ADD_OR_DELETE_MESSAGE = "Удалить или добавить маствотч?"
    __CHOOSE_USER_MESSAGE = "Кому добавить маствотч?"
    __SEND_ITEM_TITLE_MESSAGE = "Напишите название маствотча"

    async def start_conversation_with_user(self, message, register_state):
        __USER_IS_NOT_REGISTERED_MESSAGE = "Пользователь не зарегистрирован!"

        if not register_state:
            await self.bot.reply_to(message,
                                    ManageMustwatchRobot.__USER_IS_NOT_REGISTERED_MESSAGE)
        else:
            await self.bot.reply_to(message,
                                    ManageMustwatchRobot.__ADD_OR_DELETE_MESSAGE,
                                    reply_markup=self.markup_add_or_delete_item())

    async def __edit_message_to_choose_user_buttons(self, call):
        await self.edit_message_text_and_buttons(
            call,
            ManageMustwatchRobot.__CHOOSE_USER_MESSAGE,
            self.markup_choose_user_add_item
        )

    async def edit_add_or_delete_response_to_choose_user(self, call):
        if call.data == InlineMarkupNanobot.DELETE_BUTTON[1]:
            pass
        if call.data == InlineMarkupNanobot.ADD_BUTTON[1]:
            await self.__edit_message_to_choose_user_buttons(call)
