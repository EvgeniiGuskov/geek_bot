from telebots_potion_store.robots.nanobots.keyboard_nanobot import KeyboardNanobot


class AddMustwatchRobot(KeyboardNanobot):
    __USER_IS_NOT_REGISTERED_MESSAGE = "Пользователь не зарегистрирован!"
    __TO_WHOM_ADD_MUSTWATCH_MESSAGE = "Кому добавить маствотч?"

    async def start_conversation_with_user(self, message, register_state):
        if not register_state:
            await self.bot.reply_to(message, AddMustwatchRobot.__USER_IS_NOT_REGISTERED_MESSAGE)
        else:
            await self.bot.reply_to(message, AddMustwatchRobot.__TO_WHOM_ADD_MUSTWATCH_MESSAGE,
                                    reply_markup=self.markup_whom_add())

    def handle_callback_from_whom_button(self, call):
        if call.data == "all":
            print("all")
        elif call.data == "me":
            print("me")
        elif call.data == "user":
            print("user")
