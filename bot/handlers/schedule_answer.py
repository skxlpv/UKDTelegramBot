from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import set_primary
from bot.handlers.menu import menu
from bot.states.UserStates import UserStates
from bot.utils.schedule_utils import day_schedule_display, week_schedule_display
from loader import dp


@dp.callback_query_handler(state=UserStates.schedule_callback)
async def callback_schedule_buttons(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    isTeacher = data['isTeacher']
    group_id = data['group_id']

    match callback.data:
        case 'mn':
            await callback.answer(text='Розклад на понеділок')
            await day_schedule_display(number=0, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'ts':
            await callback.answer(text='Розклад на вівторок')
            await day_schedule_display(number=1, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'wd':
            await callback.answer(text='Розклад на середу')
            await day_schedule_display(number=2, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'th':
            await callback.answer(text='Розклад на четвер')
            await day_schedule_display(number=3, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'fr':
            await callback.answer(text='Розклад на п\'ятницю')
            await day_schedule_display(number=4, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'week':
            await callback.answer(text='Розклад на тиждень')
            await week_schedule_display(week='current', callback=callback,
                                        group_id=group_id, isTeacher=isTeacher, state=state)
        case 'next_week':
            await callback.answer(text='Розклад на наступний тиждень')
            await week_schedule_display(week='next', callback=callback,
                                        group_id=group_id, isTeacher=isTeacher, state=state)
        case 'primary':
            set_primary(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            await callback.answer(text='Тепер цей розклад є основним')
        case 'favorite':
            await callback.answer(text='Обрані поки не імплементовані!')
        case 'menu':
            await callback.answer()
            await callback.message.reply('<em><strong>Головне меню!</strong></em>', parse_mode='HTML')
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
        await callback.message.reply('<em><strong>Головне меню!</strong></em>', parse_mode='HTML')
        await UserStates.menu.set()
        await menu(message=callback.message)


def register_schedule_answer_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(callback_schedule_buttons)
    dispatcher.register_message_handler(callback_tip)
