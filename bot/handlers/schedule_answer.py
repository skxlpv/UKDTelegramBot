from aiogram import Dispatcher, types
import requests
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext

from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard

from bot.states.UserStates import UserStates
from bot.utils.schedule_utils import my_schedule_func, my_schedule_big_func

from loader import dp


@dp.callback_query_handler(state=UserStates.schedule_callback)
async def callback_schedule_buttons(callback: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    group = data.get('group_id')
    student = data.get('student')
    dt = datetime.now()
    day = dt.weekday()

    if callback.data == 'mn':
        monday = dt - timedelta(days=day)
        time_str = monday.strftime('%d.%m.%Y')
        final_string_of_lessons = my_schedule_func(group, time_str, student )
        await callback.message.edit_text(text=f'Понеділок - {monday.strftime("%d.%m")}\nf3ogiog4jg\n—————\n'
                                              f'{final_string_of_lessons}',reply_markup=schedule_keyboard)
    elif callback.data == 'ts':
        tuesday = dt - timedelta(days=(day - 1))
        time_str = tuesday.strftime('%d.%m.%Y')
        final_string_of_lessons = my_schedule_func(group, time_str, student )
        await callback.message.edit_text(text=f'Вівторок - {tuesday.strftime("%d.%m")}\nf3ogiog4jg\n—————\n'
                                              f'{final_string_of_lessons}', reply_markup=schedule_keyboard)
    elif callback.data == 'wd':
        wednesday = dt - timedelta(days=(day - 2))
        time_str = wednesday.strftime('%d.%m.%Y')
        final_string_of_lessons = my_schedule_func(group, time_str, student )
        await callback.message.edit_text(text=f'Середа - {wednesday.strftime("%d.%m")}\nf3ogiog4jg\n—————\n'
                                              f'{final_string_of_lessons}', reply_markup=schedule_keyboard)
    elif callback.data == 'th':
        thursday = dt - timedelta(days=(day - 3))
        time_str = thursday.strftime('%d.%m.%Y')
        final_string_of_lessons = my_schedule_func(group, time_str, student )
        await callback.message.edit_text(text=f'Четвер - {thursday.strftime("%d.%m")}\nf3ogiog4jg\n—————\n'
                                              f'{final_string_of_lessons}', reply_markup=schedule_keyboard)
    elif callback.data == 'fr':
        friday = dt - timedelta(days=(day - 4))
        time_str = friday.strftime('%d.%m.%Y')
        final_string_of_lessons = my_schedule_func(group, time_str, student )
        await callback.message.edit_text(text=f"П'ятниця - {friday.strftime('%d.%m')}\nf3ogiog4jg\n—————\n"
                                              f"{final_string_of_lessons}\n", reply_markup=schedule_keyboard)
    elif callback.data == 'Week':
        monday = dt - timedelta(days=day)
        curfriday = dt - timedelta(days=(day - 4))
        friday = dt - timedelta(days=(day - 5))
        final_string_of_lessons = my_schedule_big_func(group, student, monday, friday)
        await callback.message.edit_text(text=f"Розклад на весь пточний тиждень\nдля f3ogiog4jg, з "
                                              f"{monday.strftime('%d.%m')} по {curfriday.strftime('%d.%m')}"
                                              f"\n—————\n\n{final_string_of_lessons}", reply_markup=schedule_keyboard)
    elif callback.data == 'Next':
        monday = dt - timedelta(days=day - 7)
        curfriday = dt - timedelta(days=(-day - 1))
        friday = dt - timedelta(days=(-day - 2))
        final_string_of_lessons = my_schedule_big_func(group, student, monday, friday)
        await callback.message.edit_text(text=f"Розклад на весь наступний тиждень\nдля f3ogiog4jg, з "
                                              f"{monday.strftime('%d.%m')} по {curfriday.strftime('%d.%m')}"
                                              f"\n—————\n\n{final_string_of_lessons}", reply_markup=schedule_keyboard)
    elif callback.data == 'general_schedule':
        await callback.message.answer("General schedule is not implemented")
    elif callback.data == 'favorite':
        await callback.message.answer("Favorites is not implemented")
    elif callback.data == 'menu':
        await callback.message.answer(text="Ви увійшли в меню, будьласка виберіть дію", reply_markup=menu_keyboard)
        await UserStates.menu_handler.set()


def register_schedule_answer_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(callback_schedule_buttons)
