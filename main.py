import alchemical_lab
import telebots_potion_store

database = alchemical_lab.Alchemist()
telebot = telebots_potion_store.Telebot()


@telebot.bot.message_handler(commands=["register"])
async def register_user(message):
    user_data = telebot.get_user_data_from_message(message)
    register_result = database.register_user(*user_data)
    await telebot.register_command_response(message, register_result)


@telebot.bot.message_handler(commands=["manage_mustwatch"])
async def add_mustwatch(message):
    user_data = telebot.get_user_data_from_message(message)
    register_state = database.is_user_registered(*user_data)
    await telebot.start_conversation_with_user(message, register_state)


@telebot.bot.callback_query_handler(func=lambda call: True)
async def mustwatch_callback_queries(call):
    user_data = telebot.get_user_choice_from_add_or_delete_call(call)
    database.update_user_request_with_message_id_and_add_or_delete(*user_data)
    await telebot.edit_add_or_delete_response_to_choose_user(call)


telebot.poll()
