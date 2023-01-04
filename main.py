import alchemical_lab
import telebots_potion_store

database = alchemical_lab.Alchemist()
telebot = telebots_potion_store.Telebot()


@telebot.bot.message_handler(commands=["register"])
async def register_user(message):
    user_data = telebot.get_user_data(message)
    register_result = database.register_user(*user_data)
    await telebot.register_command_response(message, register_result)


@telebot.bot.message_handler(commands=["add_mustwatch"])
async def add_mustwatch(message):
    user_data = telebot.get_user_data(message)
    register_state = database.is_user_registered(*user_data)
    await telebot.start_conversation_with_user(message, register_state)


@telebot.bot.callback_query_handler(func=lambda call: True)
async def add_mustwatch_callback_queries(call):
    telebot.handle_callback_from_whom_button(call)


telebot.poll()
