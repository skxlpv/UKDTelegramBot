from aiogram import Bot, Dispatcher, executor, types
import requests
import time
from loader import bot, dp
from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.utils import schedule_utils

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id = message.from_user.id,
                         text=f'Вітаю,{message.from_user.first_name} {message.from_user.last_name}!\n '
                             f'Я -- офіційний бот-асистент від Університету Короля Данила!', parse_mode='html')
    await message.delete()
    await bot.send_message(chat_id = message.from_user.id, text = 'Будь ласка, виберіть бажану опцію',
                           reply_markup=menu_keyboard)


@dp.message_handler(regexp = "Мій розклад")
async def first_answer(message: types.Message):
    if message.text == 'Знайти розклад':
        await bot.send_message(chat_id = message.from_user.id, text ="hello:)")
        await message.delete()
    elif message.text == 'Мій розклад':
        time_str = time.strftime("%d.%m.%Y")
        url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=group&OBJ_ID=&OBJ_name=%B2%CF%C7%F1-21-2&dep_name=&ros_text=separated&begin_date={time_str}&end_date={time_str}&req_format=json&coding_mode=UTF8&bs=ok'
        data = requests.get(url).json()
        await my_schedule(message, data)
        await message.delete()
    elif message.text == 'Обране':
        await bot.send_message(chat_id = message.from_user.id, text ="papa:)")
        await message.delete()


@dp.message_handler()
async def my_schedule(message: types.Message, data):
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


@dp.message_handler()
async def day_schedule(callback: types.CallbackQuery):
    pass


def register_schedule_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start)
    dispatcher.register_message_handler(first_answer)
    dispatcher.register_message_handler(my_schedule)
    dispatcher.register_message_handler(day_schedule)

