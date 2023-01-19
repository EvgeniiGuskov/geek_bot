from config.telebot.telebot import Telebot
from config.database.alchemist import Alchemist
from src.controller.user_data_collector import UserDataCollector
from src.view.commands_handlers.register_handler.register_command_handler import RegisterCommandHandler
from src.view.commands_handlers.mustwatch_rating_handler.mustwatch_rating_command_handler import \
    MustwatchRatingCommandHandler
from src.view.commands_handlers.mustwatch_handler.mustwatch_command_handler import MustwatchCommandHandler
from src.service.register_db import RegisterDb
from src.service.mustwatch_rating_db import MustwatchRatingDb
from src.service.mustwatch_db import MustwatchDb
from src.model.database_checker import DatabaseChecker
from src.model.database_updater import DatabaseUpdater


class App:

    def __init__(self):
        self.telebot = Telebot()
        self.user_data_collector = UserDataCollector(self.telebot)
        self.reg_viewer = RegisterCommandHandler(self.telebot)
        self.mw_rating_viewer = MustwatchRatingCommandHandler(self.telebot)
        self.mw_viewer = MustwatchCommandHandler(self.telebot)

        self.alchemist = Alchemist()
        self.db_check = DatabaseChecker(self.alchemist)
        self.db_upd = DatabaseUpdater(self.alchemist)
        self.db_reg = RegisterDb(self.alchemist, self.db_check, self.db_upd)
        self.db_mw_rating = MustwatchRatingDb(self.alchemist, self.db_check, self.db_upd)
        self.db_mw = MustwatchDb(self.alchemist, self.db_check, self.db_upd)
