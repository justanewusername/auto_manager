import datetime
from typing import Callable

from dateutil.parser import parse
from telebot.types import Message
from telegram.controllers.general import BaseController
from aiogram import aiogram

from telegram.views import AmView, MgView
from telegram.views.favourite_view import FavouriteView
from telegram.views.history_view import HistoryView
from telegram.views.pc_view import PcView
from telegram.views.search_view import SearchView
from telegram.views.start_view import StartView


class StartController(BaseController):
    def __init__(self, config, category_manager: Callable[..., CategoryManagerProtocol],
                 form_manager: Callable[..., FormManagerProtocol], user_manager: Callable[..., UserManagerProtocol],
                 favourite_manager: Callable[..., FavouriteManagerProtocol],
                 history_manager: Callable[..., HistoryManagerProtocol],
                 plot_get: Callable[..., PlotGet]):
        self.config = config
        self.category_manager = category_manager
        self.form_manager = form_manager
        self.user_manager = user_manager
        self.favourite_manager = favourite_manager
        self.history_manager = history_manager
        self.plot_get = plot_get

    def set_up(self, bot: TeleBot) -> None:

        @bot.message_handler(commands=[self.config.Commands.Start])
        def start_handler(message: Message, data: dict):
            view = StartView(bot, message, data)
            msg = view.show_main_menu(self.config)
            bot.register_next_step_handler(msg, choose_menu_command, data)

        def choose_menu_command(message: Message, data: dict):
            ls: LocalizationServiceProtocol = data['ls']
            if ls.get('search_command') in message.text:
                search_handler(message, data)
            elif ls.get('am_command') in message.text:
                am_handler(message, data)
            elif ls.get('mg_command') in message.text:
                mg_handler(message, data)
            elif ls.get('pc_command') in message.text:
                pc_handler(message, data)
            elif ls.get('favourites_command') in message.text:
                favourite_handler(message, data)
            elif ls.get('history_command') in message.text:
                history_handler(message, data)
            else:
                bot.register_next_step_handler(message, choose_menu_command, data)

        @bot.message_handler(commands=[self.config.Commands.ManagerMenu])
        def mg_handler(message: Message, data: dict):
            view = MgView(bot, message, data)
            data['view'] = view
            msg = view.show_welcome()
            bot.register_next_step_handler(msg, choose_mg_command, data)

        def choose_mg_command(message: Message, data: dict):
            ls: LocalizationServiceProtocol = data['ls']
            view: MgView = data['view']
            if message.text == ls.get('show_stats'):
                msg = view.ask_dates()
                bot.register_next_step_handler(msg, show_statistics, data)
            elif message.text == ls.get('back'):
                start_handler(message, data)
            else:
                bot.register_next_step_handler(message, choose_mg_command, data)

        def show_statistics(message: Message, data: dict):
            view: MgView = data['view']
            try:
                dates = message.text.split(' ')
                for plot in self.plot_get().get_plot_new_users(dates[0], dates[1], data['user'].id):
                    msg = bot.send_photo(message.chat.id, plot)
                bot.register_next_step_handler(msg, choose_mg_command, data)
            except Exception:
                msg = view.show_date_error()
                bot.register_next_step_handler(msg, show_statistics, data)

        @bot.message_handler(commands=[self.config.Commands.AdminMenu])
        def am_handler(message: Message, data: dict):
            view = AmView(bot, message, data)
            data['view'] = view
            msg = view.show_welcome()
            bot.register_next_step_handler(msg, choose_am_command, data)

        def choose_am_command(message: Message, data: dict):
            ls: LocalizationServiceProtocol = data['ls']
            if message.text == ls.get('back'):
                start_handler(message, data)
            elif message.text == ls.get('change_managers_command'):
                managers = self.user_manager().get_by_role(self.config.Roles.Manager)
                msg = data['view'].show_managers(managers)
                bot.register_next_step_handler(msg, choose_managers_command, data)
            else:
                bot.register_next_step_handler(message, choose_am_command, data)

        def choose_managers_command(message: Message, data: dict):
            ls: LocalizationServiceProtocol = data['ls']
            view: AmView = data['view']
            if message.text == ls.get('add_manager'):
                msg = view.ask_id()
                bot.register_next_step_handler(msg, change_manager, data, False)
            elif message.text == ls.get('remove_manager'):
                msg = view.ask_id()
                bot.register_next_step_handler(msg, change_manager, data, True)
            elif message.text == ls.get('back'):
                am_handler(message, data)
            else:
                bot.register_next_step_handler(message, choose_managers_command, data)

        def change_manager(message: Message, data: dict, is_delete):
            view: AmView = data['view']
            if not message.text.isdigit() or not self.user_manager().exists(int(message.text)):
                view.invalid_id()
            else:
                if is_delete:
                    self.user_manager().delete(int(message.text))
                    view.successful_delete()
                else:
                    user = self.user_manager().get(int(message.text))
                    user.role = self.config.Roles.Manager
                    self.user_manager().update(user)
                    view.successful_update()
                am_handler(message, data)

        @bot.message_handler(commands=[self.config.Commands.PersonalCabinet])
        def pc_handler(message: Message, data: dict):
            view = PcView(bot, message, data)
            data['view'] = view
            msg = view.show_info()
            bot.register_next_step_handler(msg, choose_pc_command, data)

        def choose_pc_command(message: Message, data: dict):
            ls: LocalizationServiceProtocol = data['ls']
            view: PcView = data['view']
            if message.text == ls.get('change_name'):
                msg = view.ask_name()
                bot.register_next_step_handler(msg, set_name, data, ls)
            elif message.text == ls.get('change_location'):
                msg = view.ask_location()
                bot.register_next_step_handler(msg, set_location, data, data['user'], ls)
            elif message.text == ls.get('return_command'):
                start_handler(message, data)
            else:
                bot.register_next_step_handler(message, choose_pc_command, data)

        def set_name(message: Message, data: dict, ls: LocalizationServiceProtocol):
            if message.text == ls.get('back'):
                pc_handler(message, data)
            else:
                user_manager = self.user_manager()
                user: User = data['user']
                view: PcView = data['view']
                name = message.text.split(' ')
                if len(name) < 2:
                    msg = view.invalid_name()
                    msg = view.ask_name()
                    bot.register_next_step_handler(msg, set_name, data, ls)
                    return
                try:
                    user.name = name[0]
                    user.second_name = name[1]
                    user_manager.update(user)
                except ValidationException as ex:
                    msg = view.validation_exception(ex)
                    msg = view.ask_name()
                    bot.register_next_step_handler(msg, set_name, data, ls)
                view.successful_update()
                msg = view.show_info()
                bot.register_next_step_handler(msg, choose_pc_command, data)

        def set_location(message: Message, data: dict, user: User, ls: LocalizationServiceProtocol):
            if message.text == ls.get('back'):
                pc_handler(message, data)
            else:
                view: PcView = data['view']
                if message.location is None:
                    msg = view.invalid_location()
                    msg = view.ask_location()
                    bot.register_next_step_handler(msg, set_location, data, user, ls)
                else:
                    user.latitude = message.location.latitude
                    user.longitude = message.location.longitude
                    try:
                        self.user_manager().update(user)
                    except ValidationException as ex:
                        msg = view.validation_exception(ex)
                        msg = view.ask_location()
                        bot.register_next_step_handler(msg, set_location, data, user, ls)
                    view.successful_update()
                    msg = view.show_info()
                    bot.register_next_step_handler(msg, choose_pc_command, data)

        @bot.message_handler(commands=[self.config.Commands.Search])
        def search_handler(message: Message, data: dict):
            categories = self.category_manager().get_all_categories()
            view = SearchView(bot, message, data)
            data['categories'] = categories
            data['view'] = view
            msg = view.show_categories([key for key in categories.keys()])
            bot.register_next_step_handler(msg, choose_category, data)

        def choose_category(message: Message, data: dict):
            key = message.text
            ls: LocalizationServiceProtocol = data['ls']
            categories = data['categories']
            view = data['view']
            if ls.get('return_command') in key or ls.get('menu_command') in key:
                start_handler(message, data)
            elif key not in categories.keys():
                view.key_error()
                msg = view.show_categories([key for key in categories.keys()])
                bot.register_next_step_handler(msg, choose_category, data)
            elif len(categories[key]) == 0:
                show_form(message, key, data, True, None)
            else:
                msg = view.show_categories([key for key in categories[key].keys()])
                data['categories'] = categories[key]
                bot.register_next_step_handler(msg, choose_category, data)

        def show_form(message: Message, category: str, data: dict, length: bool, form: Form | None):
            view = data['view']
            user: User = data['user']
            if form is None:
                form = self.form_manager().get_form(category, (user.latitude, user.longitude), 5)
            if form is None:
                msg = view.show_not_exists_error()
                bot.register_next_step_handler(msg, choose_category, data)
            elif user.credits <= 0:
                msg = view.show_credits_error()
                search_handler(msg, data)
            else:
                if length:
                    msg = view.show_form_short(form)
                else:
                    msg = view.show_form_long(form)
                user.credits -= 1
                self.history_manager().create(History(form.form_url, None, user.id))
                self.user_manager().update(user)
                bot.register_next_step_handler(msg, choose_form_command, data, category, form)

        def choose_form_command(message: Message, data: dict, category: str, form):
            ls: LocalizationServiceProtocol = data['ls']
            view: SearchView = data['view']
            if message.text == ls.get('return_command'):
                search_handler(message, data)
            elif message.text == ls.get('next_command'):
                show_form(message, category, data, True, None)
            elif message.text == ls.get('long_description'):
                show_form(message, category, data, False, form)
            elif message.text == ls.get('short_description'):
                show_form(message, category, data, True, form)
            elif message.text == ls.get('to_favourite_command'):
                try:
                    self.category_manager().add_to_favourites(category, data['user'].id)
                    message = view.added_favourite(True)
                except Exception:
                    message = view.added_favourite(False)
                bot.register_next_step_handler(message, choose_form_command, data, category, form)
            elif message.text == ls.get('change_radius_command'):
                bot.register_next_step_handler(message, choose_form_command, data, category, form)
            else:
                view.invalid_command()
                bot.register_next_step_handler(message, choose_category, data, category)

        @bot.message_handler(commands=[self.config.Commands.Favourites])
        def favourite_handler(message: Message, data: dict) -> None:
            view = FavouriteView(bot, message, data['ls'])
            ls: LocalizationServiceProtocol = data['ls']

            favourite = self.favourite_manager().get_all(message.from_user.id)
            if len(favourite) < 1:
                view.favourite_error()
                start_handler(message, data)
            else:
                msg = view.show_favourites(favourite)
                bot.register_next_step_handler(msg, redact_favourites, view, ls, favourite, data)

        def redact_favourites(message: Message, view: FavouriteView, ls: LocalizationServiceProtocol,
                              favourite: list[str], data: dict):
            if message.text == ls.get('back'):
                start_handler(message, data)
            else:
                msg = view.redact_favourites(favourite)
                bot.register_next_step_handler(msg, choice_of_category, ls, view, data)

        def choice_of_category(message: Message, ls: LocalizationServiceProtocol, view: FavouriteView, data: dict):
            if message.text != ls.get('back'):
                msg = view.ask_about_removal()
                bot.register_next_step_handler(msg, remove_category, ls, view, message.text, data)
                return
            else:
                favourite_handler(message, data)

        def remove_category(message: Message, ls: LocalizationServiceProtocol, view: FavouriteView,
                            choice_category: str, data: dict):
            if message.text == ls.get('yes'):
                try:
                    self.favourite_manager().delete(message.from_user.id, choice_category)
                    view.successful_removal()
                except:
                    view.remove_error()
            favourite = self.favourite_manager().get_all(message.from_user.id)
            redact_favourites(message, view, ls, favourite, data)

        @bot.message_handler(commands=[self.config.Commands.History])
        def history_handler(message: Message, data: dict) -> None:
            view = HistoryView(bot, message, data['ls'])
            ls: LocalizationServiceProtocol = data['ls']

            history = self.history_manager().get_all(message.from_user.id)
            if len(history) < 1:
                view.history_error()
                start_handler(message, data)
            else:
                msg = view.show_history(history)
                bot.register_next_step_handler(msg, start_handler(message, data), ls, data)
