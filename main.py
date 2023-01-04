import alchemical_lab
import telebots_potion_store

database = alchemical_lab.Alchemist()
telebot = telebots_potion_store.Telebot()


@telebot.bot.message_handler(commands=["register"])
async def register_user(message):
    user_data = telebot.get_user_data(message)
    register_result = database.register_user(*user_data)
    await telebot.register_command_response(message, register_result)


telebot.poll()
