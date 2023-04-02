from datetime import datetime, timedelta

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import set_primary, get_from_collection
from bot.handlers.menu import menu
from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from bot.utils.schedule_utils import my_schedule_func, my_schedule_big_func, name_func
from loader import dp


async def week_schedule_display(week, callback, group, isTeacher, today=datetime.now()):
    weekday = today.weekday()

    if week == 'current':
        current_or_next = 'поточний'
        monday = today - timedelta(days=weekday)
        current_friday = today - timedelta(days=(-weekday - 4))
        friday = today - timedelta(days=(-weekday - 5))
    elif week == 'next':
        current_or_next = 'наступний'
        monday = today - timedelta(days=weekday - 7)
        current_friday = today - timedelta(days=(-weekday - 1))
        friday = today - timedelta(days=(-weekday - 2))
    else:
        print('Week argument in week_schedule_display() is invalid. '
              'Must be either "current" or "next"')
        raise ValueError

    name = name_func(group, isTeacher)
    final_string_of_lessons = my_schedule_big_func(group, isTeacher, monday, friday)
    await callback.message.edit_text(text=f"Розклад на {current_or_next} тиждень\nдля {name}, з "
                                          f"{monday.strftime('%d.%m')} по {current_friday.strftime('%d.%m')}"
                                          f"\n—————\n\n{final_string_of_lessons}", reply_markup=schedule_keyboard)


async def day_schedule_display(number, day_of_week, callback, group, isTeacher, today=datetime.now()):
    weekday = today.weekday()

    monday = today - timedelta(days=(weekday - number))
    time_str = monday.strftime('%d.%m.%Y')
    final_string_of_lessons = my_schedule_func(group_id=group, isTeacher=isTeacher, time_str=time_str)
    await callback.message.edit_text(text=f'{day_of_week} - {monday.strftime("%d.%m")}\n'
                                          f'{final_string_of_lessons}', reply_markup=schedule_keyboard)


@dp.callback_query_handler(state=UserStates.schedule_callback)
async def callback_schedule_buttons(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    isTeacher = data.get('isTeacher')
    # primary = get_from_collection(callback.from_user.id, 'primary')
    group = data.get('group_id')

    if callback.data == 'mn':
        await callback.answer(text='Розклад на понеділок')
        await day_schedule_display(number=0, day_of_week='Понеділок', callback=callback,
                                   group=group, isTeacher=isTeacher)

    elif callback.data == 'ts':
        await callback.answer(text='Розклад на вівторок')
        await day_schedule_display(number=1, day_of_week='Вівторок', callback=callback,
                                   group=group, isTeacher=isTeacher)

    elif callback.data == 'wd':
        await callback.answer(text='Розклад на середу')
        await day_schedule_display(number=2, day_of_week='Середа', callback=callback,
                                   group=group, isTeacher=isTeacher)

    elif callback.data == 'th':
        await callback.answer(text='Розклад на четвер')
        await day_schedule_display(number=1, day_of_week='Четвер', callback=callback,
                                   group=group, isTeacher=isTeacher)

    elif callback.data == 'fr':
        await callback.answer(text='Розклад на п\'ятницю')
        await day_schedule_display(number=1, day_of_week='П\'ятниця', callback=callback,
                                   group=group, isTeacher=isTeacher)

    elif callback.data == 'Week':
        await callback.answer(text='Розклад на тиждень')
        await week_schedule_display(week='current', callback=callback,
                                    group=group, isTeacher=isTeacher)

    elif callback.data == 'Next':
        await callback.answer(text='Розклад на наступний тиждень')
        await week_schedule_display(week='next', callback=callback,
                                    group=group, isTeacher=isTeacher)

    elif callback.data == 'general_schedule':
        set_primary(user=callback.from_user.id, group_id=group, isTeacher=True)  # ISSUE: str(group)
        await callback.answer(text='Тепер цей розклад є основним')

    elif callback.data == 'favorite':
        await callback.answer(text='Обрані поки не імплементовані!')

    elif callback.data == 'menu':
        await callback.message.reply('Ми знову у головному меню!')
        await UserStates.menu.set()
        await menu(message=callback.message)


@dp.callback_query_handler(state=UserStates.tip_callback)
async def callback_tip(callback: types.CallbackQuery):
    if callback.data == 'yes':
        await callback.message.answer(text='Після повернення в <b>Головне Меню</b>, натисніть кнопку '
                                           '<b>"Знайти розклад"</b>. Введіть дані спеціальності, року поступлення та '
                                           'групи. Затім  в наступному меню оберіть пункт <b>"Позначити розклад '
                                           'Основним"</b>.Після цього, ви зможете з легкістю переглядати інформацію '
                                           'про обраний розклад в кілька тапів!', parse_mode='HTML')
        await UserStates.menu_handler.set()
    elif callback.data == 'no':
        await callback.message.reply('Ми знову у головному меню!')
        await UserStates.menu.set()
        await menu(message=callback.message)


def register_schedule_answer_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(callback_schedule_buttons)
    dispatcher.register_message_handler(callback_tip)
