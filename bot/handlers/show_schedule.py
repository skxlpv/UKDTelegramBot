from aiogram import Dispatcher, types
import requests
import time

from aiogram.dispatcher.filters import CommandStart

from bot.handlers.search import search_schedule
from loader import bot, dp
from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.utils import schedule_utils


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Вітаю, {message.from_user.first_name}!\n'
                                f'Я -- офіційний бот-асистент від Університету Короля Данила!\n'
                                f'Будь ласка, виберіть бажану опцію',
                           reply_markup=menu_keyboard)


@dp.message_handler(text=["Знайти розклад", "Мій розклад", "Обране"])
async def first_answer(message: types.Message):
    if message.text == 'Знайти розклад':
        await search_schedule(message=message)
        # await GeneralStates.search_schedule.set()
    elif message.text == 'Мій розклад':
        await my_schedule(message)
    elif message.text == 'Обране':
        await bot.send_message(chat_id=message.from_user.id, text="Favorites is not implemented")


async def my_schedule(message: types.Message):
    time_str = time.strftime("%d.%m.%Y")
    url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=group&OBJ_ID=&OBJ_name=%B2%CF%C7%F1-21-2&dep_name=&ros_text=separated&begin_date={time_str}&end_date={time_str}&req_format=json&coding_mode=UTF8&bs=ok'
    data = requests.get(url).json()

    data = data['psrozklad_export']['roz_items']
    schedule_list = []
    for i in data:
        r = f'{i["reservation"]}'
        r = r.replace("<i> <b><small><font color=Navy>", "")
        r = r.replace("</font></small></b></i>", "")
        if i['type'] == "Л":
            emoji = "📖"
        else:
            emoji = "⚒️"
        if i['title'] == "":
            schedule_list.append(f'🕑  {i["lesson_time"]}\n🌀  {r}\n- - - - - - - - -')
        elif i['reservation'] == "":
            schedule_list.append(f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                                 f'{i["room"]}\n- - - - - - - - -')
        else:
            schedule_list.append(f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                                 f'{i["room"]}\n🌀  {r}\n- - - - - - - - -')

    string_of_lessons = ''
    for i in schedule_list:
        string_of_lessons += i + '\n'
    final_string_of_lessons = schedule_utils.remove_last_line_from_string(string_of_lessons)
    await bot.send_message(chat_id=message.from_user.id, text=f'ІПЗс-21-2\n—————\n{final_string_of_lessons}',
                           reply_markup=schedule_keyboard)


@dp.message_handler()   # temporary solution for incorrect input handling
async def incorrect_input(message: types.Message):
    await message.answer('Некоректний ввід!')


def register_schedule_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start)
    dispatcher.register_message_handler(first_answer)
    dispatcher.register_message_handler(my_schedule)
