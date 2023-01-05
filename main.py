import alchemical_lab
import telebots_potion_store

database = alchemical_lab.Alchemist()
telebot = telebots_potion_store.Telebot()


@telebot.bot.message_handler(commands=["register"])
async def register_user(message):
    user_data = telebot.get_user_data_from_message(message)
    register_result = database.register_user(*user_data)
    await telebot.register_command_response(message, register_result)


@telebot.bot.message_handler(commands=["mustwatch"])
async def mustwatch(message):
    user_data = telebot.get_user_data_from_message(message)
    register_state = database.is_user_registered(*user_data)
    await telebot.start_conversation_with_user(message, register_state)


@telebot.bot.callback_query_handler(func=lambda call: True)
async def mustwatch_callback_queries(call):
    await telebot.add_or_delete_item_response(call)
    await telebot.add_new_or_take_from_db_response(call)
    user_data = telebot.get_user_data_from_to_me_call(call)
    await telebot.add_or_delete_somebodies_item_response(call)
    await telebot.choose_item_kind_response(call)
    await telebot.choose_item_timing_response(call)


telebot.poll()
