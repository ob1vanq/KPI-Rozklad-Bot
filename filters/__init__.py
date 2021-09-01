from aiogram import Dispatcher

from filters.is_admin import AdminFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
