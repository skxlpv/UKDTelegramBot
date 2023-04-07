from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.database.schedule_requests import set_primary, set_favorites, delete_favorite, delete_primary
from bot.handlers.menu import menu
from bot.keyboards.inline.schedule_keyboard import get_schedule_keyboard
from bot.states.UserStates import UserStates
from bot.storage.placeholders import callbacks, messages
from bot.utils.schedule_utils import day_schedule_display, week_schedule_display
from loader import dp, bot


@dp.callback_query_handler(state=UserStates.schedule_callback)
async def callback_schedule_buttons(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    isTeacher = data['isTeacher']
    group_id = data['group_id']
    match callback.data:
        case 'mn':
            await callback.answer(text=callbacks.MONDAY)
            await day_schedule_display(number=0, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'ts':
            await callback.answer(text=callbacks.TUESDAY)
            await day_schedule_display(number=1, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'wd':
            await callback.answer(text=callbacks.WEDNESDAY)
            await day_schedule_display(number=2, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'th':
            await callback.answer(text=callbacks.THURSDAY)
            await day_schedule_display(number=3, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'fr':
            await callback.answer(text=callbacks.FRIDAY)
            await day_schedule_display(number=4, callback=callback, group_id=group_id, isTeacher=isTeacher, state=state)
        case 'week':
            await callback.answer(text=callbacks.WEEK)
            await week_schedule_display(week='current', callback=callback,
                                        group_id=group_id, isTeacher=isTeacher, state=state)
        case 'next_week':
            await callback.answer(text=callbacks.NEXT_WEEK)
            await week_schedule_display(week='next', callback=callback,
                                        group_id=group_id, isTeacher=isTeacher, state=state)
        case 'primary':
            primary_status = set_primary(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            match primary_status:
                case -11:
                    delete_primary(user=callback.from_user.id, isTeacher=isTeacher)
                    await callback.answer(text=callbacks.NOT_PRIMARY)
                case 1:
                    await callback.answer(text=callbacks.PRIMARY)
            keyboard = get_schedule_keyboard(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            await bot.edit_message_reply_markup(message_id=callback.message.message_id, chat_id=callback.from_user.id,
                                                reply_markup=keyboard)
        case 'favorite':
            favorites_status = set_favorites(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            match favorites_status:
                case -11:
                    delete_favorite(user=callback.from_user.id, group_id=group_id,
                                    isTeacher=isTeacher)
                    await callback.answer(text=callbacks.PRIMARY)
                case -10:
                    await callback.answer(text=callbacks.FAVORITE_LIMIT)
                case 1:
                    await callback.answer(text=callbacks.FAVORITE)
            keyboard = get_schedule_keyboard(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
            await bot.edit_message_reply_markup(message_id=callback.message.message_id, chat_id=callback.from_user.id,
                                                reply_markup=keyboard)
        case 'menu':
            await callback.answer()
            await callback.message.reply(text=messages.MENU, parse_mode='HTML')
            await menu(message=callback.message)


@dp.callback_query_handler(state=UserStates.tip_callback)
async def callback_tip(callback: types.CallbackQuery):
    if callback.data == 'yes':
        await callback.answer()
        await callback.message.answer(text=messages.TIP_ANSWER, parse_mode='HTML')
        await UserStates.menu_handler.set()
    elif callback.data == 'no':
        await callback.answer()
        await callback.message.reply(text=messages.MENU, parse_mode='HTML')
        await UserStates.menu.set()
        await menu(message=callback.message)


def register_schedule_answer_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(callback_schedule_buttons)
    dispatcher.register_message_handler(callback_tip)
