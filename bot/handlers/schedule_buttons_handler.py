from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.database.schedule_requests import set_primary, set_favorites, delete_favorite, delete_primary
from bot.handlers.menu import menu
from bot.keyboards.inline.schedule_keyboard import get_schedule_keyboard
from bot.states.UserStates import UserStates
from bot.utils.schedule_utils import day_schedule_display, week_schedule_display
from loader import dp, bot


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
            primary_status = set_primary(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            match primary_status:
                case -11:
                    delete_primary(user=callback.from_user.id, isTeacher=isTeacher)
                    await callback.answer('Цей розклад більще не є основним')
                case 1:
                    await callback.answer(text='Тепер цей розклад є основним')
            keyboard = get_schedule_keyboard(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            await bot.edit_message_reply_markup(message_id=callback.message.message_id, chat_id=callback.from_user.id,
                                                reply_markup=keyboard)
        case 'favorite':
            favorites_status = set_favorites(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            match favorites_status:
                case -11:
                    delete_favorite(user=callback.from_user.id, group_id=group_id,
                                    isTeacher=isTeacher)
                    await callback.answer('Розклад був успішно видалений з обраних!')
                case -10:
                    await callback.answer('Неможливо додати розклад в обрані! '
                                          'Перевищенно ліміт')
                case 1:
                    await callback.answer('Розклад був успішно доданий до обраних!')
            keyboard = get_schedule_keyboard(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            await bot.edit_message_reply_markup(message_id=callback.message.message_id, chat_id=callback.from_user.id,
                                                reply_markup=keyboard)
        case 'menu':
            await callback.answer()
            await callback.message.reply('<em><strong>Головне меню!</strong></em>', parse_mode='HTML')
            await menu(message=callback.message)


@dp.callback_query_handler(state=UserStates.tip_callback)
async def callback_tip(callback: types.CallbackQuery):
    if callback.data == 'yes':
        await callback.answer()
        await callback.message.answer(text='Після повернення в <b>Головне Меню</b>, '
                                           'натисніть кнопку <b>"Знайти розклад"</b>.\n\n'
                                           'Здійсніть пошук за групою чи викладачем/-кою. '
                                           'Щойно розклад відобразиться, оберіть пункт '
                                           '<b>"Позначити основним"</b>.\n\n'
                                           'Виконавши ці кроки, Ви зможете отримати '
                                           'інформацію про Ваш основний розклад '
                                           'в кілька кліків!', parse_mode='HTML')
        await UserStates.menu_handler.set()
    elif callback.data == 'no':
        await callback.answer()
        await callback.message.reply('<em><strong>Головне меню!</strong></em>', parse_mode='HTML')
        await UserStates.menu.set()
        await menu(message=callback.message)


def register_schedule_answer_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(callback_schedule_buttons)
    dispatcher.register_message_handler(callback_tip)
