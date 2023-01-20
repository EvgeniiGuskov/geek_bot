from config.telebot.telebot import Telebot
from config.database.alchemist import Alchemist
from src.controller.telebot_adapter import TelebotAdapter
from src.view.events_listeners.register_listener.register_view import RegisterViewer
from src.view.events_listeners.mustwatch_rating_listener.mustwatch_rating_view import \
    MustwatchRatingViewer
from src.view.events_listeners.mustwatch_listener.mustwatch_view import MustwatchViewer
from src.service.register_service import RegisterService
from src.service.mustwatch_rating_service import MustwatchRatingService
from src.service.mustwatch_service import MustwatchService
from src.model.data_access_layer.groups.groups_reader import GroupsReader
from src.model.data_access_layer.users.users_reader import UsersReader
from src.model.data_access_layer.user_requests.user_requests_reader import UserRequestsReader
from src.model.data_access_layer.watches.watches_reader import WatchesReader
from src.model.data_access_layer.mustwatches.mustwatches_reader import MustwatchesReader
from src.model.data_access_layer.watches.watches_redactor import WatchesRedactor
from src.model.data_access_layer.groups.groups_redactor import GroupsRedactor
from src.model.data_access_layer.users.users_redactor import UsersRedactor
from src.model.data_access_layer.user_requests.user_requests_redactor import UserRequestsRedactor
from src.model.data_access_layer.mustwatches.mustwatches_redactor import MustwatchesRedactor
from src.view.buttons import Button as btn


class App:

    def __init__(self):
        self.telebot = Telebot()
        self.telebot_adapter = TelebotAdapter(self.telebot)
        self.reg_viewer = RegisterViewer(self.telebot)
        self.mw_rating_viewer = MustwatchRatingViewer(self.telebot)
        self.mw_viewer = MustwatchViewer(self.telebot)

        self.alchemist = Alchemist()
        self.groups_read = GroupsReader(self.alchemist)
        self.users_read = UsersReader(self.alchemist)
        self.user_requests_read = UserRequestsReader(self.alchemist)
        self.watches_read = WatchesReader(self.alchemist)
        self.mustwatches_read = MustwatchesReader(self.alchemist)
        self.watches_redact = WatchesRedactor(self.alchemist)
        self.groups_redact = GroupsRedactor(self.alchemist)
        self.users_redact = UsersRedactor(self.alchemist)
        self.user_requests_redact = UserRequestsRedactor(self.alchemist)
        self.mustwatches_redact = MustwatchesRedactor(self.alchemist)
        self.db_reg = RegisterService(self.alchemist,
                                      self.groups_read,
                                      self.users_read,
                                      self.groups_redact,
                                      self.users_redact,
                                      self.user_requests_redact)
        self.db_mw_rating = MustwatchRatingService(self.alchemist,
                                                   self.watches_read)
        self.db_mw = MustwatchService(self.alchemist,
                                      self.users_read,
                                      self.user_requests_read,
                                      self.watches_read,
                                      self.mustwatches_read,
                                      self.watches_redact,
                                      self.user_requests_redact,
                                      self.mustwatches_redact)
