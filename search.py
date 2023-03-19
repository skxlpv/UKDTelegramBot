import logging
from urllib import parse

import requests
from main import API_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#############################   API GET CALL   ##################################
response = requests.get('http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=obj_list&req_mode=group&show_ID=yes&req_format=json&coding_mode=UTF8&bs=ok')
obj = response.json()
departments = obj['psrozklad_export']['departments'][0]['objects']
#################################################################################

API_TOKEN = API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Global Variables

#////////////////////////////////////  MAIN CODE   ////////////////////////////////////
buttonChoiceSearch = InlineKeyboardButton(text='За критеріями', callback_data='choiceSearch')
buttonManualSearch = InlineKeyboardButton(text='За назвою', callback_data='manualSearch')
searchKeyboard = InlineKeyboardMarkup().add(buttonChoiceSearch, buttonManualSearch)

buttonRoleStudent = InlineKeyboardButton(text='Студент/ка', callback_data='student')
buttonRoleTeacher = InlineKeyboardButton(text='Викладач/ка', callback_data='teacher')
roleKeyboard = InlineKeyboardMarkup().add(buttonRoleStudent, buttonRoleTeacher)

specialtyKeyboard = ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
for value in range(len(departments)):
    groupName = departments[value]['name']
    specialtyKeyboard.insert(groupName)


# course choice handler
@dp.message_handler(commands=['search'])
async def start(message: types.Message):
    await message.answer('Оберіть параметри пошуку', reply_markup=searchKeyboard)


@dp.callback_query_handler(text = ['choiceSearch', 'manualSearch', 'student'])
async def callback_handler(call: types.CallbackQuery):
    match call.data:
        case 'choiceSearch':
            await call.message.edit_text('Вкажіть роль', reply_markup=roleKeyboard)
        case 'student':
            await call.message.delete()
            await call.message.answer('Оберіть спеціальність', reply_markup=specialtyKeyboard)
            

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)