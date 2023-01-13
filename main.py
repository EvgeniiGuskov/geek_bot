import database_manager
import telebot_controller

database = database_manager.Alchemist()
telebot = telebot_controller.Telebot()


def is_callback_protected_from_intruder(call):
    user_data = telebot.get_user_data_and_message_id_from_call(call)
    return database.is_callback_protected_from_intruder(*user_data)


@telebot.bot.message_handler(commands=["register"],
                             chat_types=["private", "group", "supergroup"])
async def register_user(message):
    user_data = telebot.get_user_data_from_message(message)
    register_result = database.register_user(*user_data)
    await telebot.register_command_response(message, register_result)


@telebot.bot.message_handler(commands=["manage_mustwatch"],
                             chat_types=["private", "group", "supergroup"])
async def add_mustwatch(message):
    user_data = telebot.get_user_data_from_message(message)
    register_state = database.is_user_registered(*user_data)
    user_request_data = await telebot.start_conversation_with_user(message, register_state, *user_data)
    if user_request_data:
        database.prepare_user_request(*user_request_data)


@telebot.bot.message_handler(commands=["mustwatch_rating"],
                             chat_types=["private", "group", "supergroup"])
async def show_mustwatch_rating(message):
    chat_id = telebot.get_chat_id_from_message(message)
    rated_watches_dict = database.get_rated_watches_dict(chat_id)
    await telebot.send_mustwatches_rating(message, rated_watches_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data in (telebot.DELETE_BUTTON_CALLBACK,
                                    telebot.ADD_BUTTON_CALLBACK,
                                    telebot.SHOW_MUSTWATCHES_BUTTON_CALLBACK
                                    )
)
async def chosen_action_on_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = telebot.get_user_choice_from_call(call)
        database.update_user_request_add_or_delete_and_chosen_user(*user_choice)
        if call.data != telebot.ADD_BUTTON_CALLBACK:
            user_data = telebot.get_user_data_from_call(call)
            watches_dict = database.get_watches_dict(*user_data)
        else:
            watches_dict = dict()
        await telebot.edit_add_or_delete_response_to_choose_user_or_title(call, watches_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data in (telebot.ALL_BUTTON_CALLBACK,
                                    telebot.ME_BUTTON_CALLBACK,
                                    telebot.CHOOSE_USER_BUTTON_CALLBACK
                                    )
)
async def choose_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        if call.data in (telebot.ALL_BUTTON_CALLBACK, telebot.ME_BUTTON_CALLBACK):
            user_choice = telebot.get_user_choice_from_call(call)
            database.update_user_request_chosen_user(*user_choice)
            user_data = telebot.get_user_data_from_call(call)
            watches_dict = database.get_watches_dict(*user_data)
            await telebot.edit_choose_user_response_to_choose_title(call, watches_dict)
        else:
            user_data = telebot.get_user_data_from_call(call)
            raw_users_dict = database.get_users_dict(*user_data)
            users_dict = await telebot.convert_telegram_user_id_to_full_name(call, raw_users_dict)
            await telebot.edit_choose_user_response_to_choose_specific_user(call, users_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(telebot.CHOOSE_SPECIFIC_USER_BUTTON_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = telebot.get_specific_user_choice_from_call(call)
        database.update_user_request_chosen_user(*user_choice)
        user_data = telebot.get_user_data_from_call(call)
        watches_dict = database.get_watches_dict(*user_data)
        await telebot.edit_choose_user_response_to_choose_title(call, watches_dict)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(telebot.CHOOSE_TITLE_BUTTON_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = telebot.get_title_choice_from_call(call)
        database.update_user_request_chosen_title(*user_choice)
        user_data = telebot.get_user_data_from_call(call)
        user_request_values = database.get_user_request_values(*user_data)
        chosen_user = database.get_chosen_user_from_user_request(*user_data)
        chat_id = telebot.get_chat_id_from_call(call)
        message_id = database.get_message_id_from_user_request(*user_data)
        add_or_delete = database.get_add_or_delete(*user_data)
        bot_message = await telebot.make_bot_message_from_user_request_values(call.message, *user_request_values)
        await telebot.edit_choose_title_to_confirm_request_or_rate_mustwatch(call, add_or_delete, chosen_user, chat_id,
                                                                             message_id,
                                                                             bot_message)


@telebot.bot.callback_query_handler(
    func=lambda call: call.data.startswith(telebot.MUSTWATCH_SCORE_CALLBACK)
)
async def choose_specific_user_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_choice = telebot.get_user_score_choice_from_call(call)
        database.update_user_request_user_score(*user_choice)
        user_data = telebot.get_user_data_from_call(call)
        user_request_values = database.get_user_request_values(*user_data)
        bot_message = await telebot.make_bot_message_from_user_request_values(call.message, *user_request_values)
        await telebot.edit_send_mustwatch_user_score_response_to_confirm_request(call.message.chat.id, call.message.id,
                                                                                 bot_message)


@telebot.bot.callback_query_handler(func=lambda call: call.data == telebot.ADD_NEW_MUSTWATCH_BUTTON_CALLBACK)
async def add_new_mustwatch_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        await telebot.edit_add_or_choose_title_to_send_title(call)
        user_data = telebot.get_user_data_from_call(call)
        database.delete_title_from_user_request(*user_data)


@telebot.bot.message_handler(func=lambda message: len(message.text) < 256,
                             chat_types=["private", "group", "supergroup"])
async def add_title(message):
    user_data = telebot.get_user_data_from_message(message)
    is_user_registered_and_typed_title = database.is_user_registered(
        *user_data) and not database.is_title_filled_at_user_request(
        *user_data)
    if is_user_registered_and_typed_title:
        database.update_user_request_title(*user_data, message.text)
        user_request_values = database.get_user_request_values(*user_data)
        bot_message = await telebot.make_bot_message_from_user_request_values(message, *user_request_values)
        message_id = database.get_message_id_from_user_request(*user_data)
        await telebot.edit_send_title_response_to_confirm_request(message.chat.id, message_id, bot_message)


@telebot.bot.callback_query_handler(func=lambda call: call.data in
                                                      (
                                                              telebot.CHANGE_USER_REQUEST_BUTTON_CALLBACK,
                                                              telebot.CONFIRM_USER_REQUEST_BUTTON_CALLBACK)
                                    )
async def change_or_confirm_user_request_callback_queries(call):
    if is_callback_protected_from_intruder(call):
        user_data = telebot.get_user_data_from_call(call)
        is_user_request_executed = database.execute_user_request(call, *user_data)
        if is_user_request_executed:
            await telebot.edit_confirm_request_response_to_conversation_end(call)


telebot.poll()
