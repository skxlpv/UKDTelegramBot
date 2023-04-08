# favorites
from bot.storage.placeholders import buttons

SELECT_FROM_LIST = 'Виберіть зі списку:'
NOT_PICKED_ANY_GROUP = 'Вибачте, ви не додали жодної групи'
NOT_FOUND_OR_DELETED = 'Вибачте, даний розклад не знайдено чи було видалено'

# menu
PICK_OPTION = 'Будь ласка, виберіть бажану опцію'
TIP = 'От халепа! Схоже, ви ще не додали основний розклад! Підказати як це зробити?'

# schedule buttons
MENU = '<em><strong>Головне меню!</strong></em>'
TIP_ANSWER = f'Після повернення в <b>Головне Меню</b>, ' \
             f'натисніть кнопку <b>"{buttons.FIND_SCHEDULE}"</b>.\n\n' \
             'Здійсніть пошук за групою чи викладачем/-кою. ' \
             'Щойно розклад відобразиться, оберіть пункт ' \
             '<b>"Позначити основним"</b>.\n\n' \
             'Виконавши ці кроки, Ви зможете отримати ' \
             'інформацію про Ваш основний розклад ' \
             'у декілька кроків!'

# search
SEARCH_PARAMS = 'Будь ласка, оберіть параметри пошуку розкладу'
CHOOSE_ROLE = 'Вкажіть роль'
GROUP_FULL_NAME = 'Надішліть повну назву шуканої групи'

PICK_SPECIALITY = 'Оберіть спеціальність'
PICK_SPECIALITY_FAIL = 'Будь ласка, оберіть спеціальність'

TEACHER_SELECT = "Оберіть викладача із запропонованих"
TEACHER_INITIALS = "Введіть П.І.Б. викладача/-ки"
TEACHER_INITIALS_FAIL = "Будь ласка, введіть П.І.Б. викладача"
TEACHER_NOT_FOUND = 'Вчителя не знайдено! Спробуйте ще раз!'

COURSE_NUM = '%s курс'
COURSE_SELECT = 'Оберіть курс'
COURSE_SELECT_FAIL = 'Будь ласка, оберіть курс'

GROUP_SELECT = 'Оберіть групу'
GROUP_SELECT_FAIL = 'Будь ласка, оберіть групу'
GROUP_NOT_FOUND = 'Групу не знайдено! Спробуйте ще раз!'

# settings
SETTINGS_INFO = 'Тут ви можете змінювати ваші налаштування'
YOUR_SETTINGS = 'Ваші поточні налаштування:'

# start
WELCOME = 'Вітаю, %s!\n' \
          'Я -- офіційний бот-асистент від Університету Короля Данила!\n'

#    UTILS
# render_schedule
NO_CLASSES = '\nЦього дня у вас немає пар, хорошого відпочинку!'
BREAK_LINE = '_'*35
CLASSES_QUANTITY = f'{BREAK_LINE}\n' \
                   '<code>Загальна кількість пар: %s </code>'
SEARCH_NAME = '<code><u>%s</u></code>'
DAY_AND_DATE = '<code><u>%s, %s</u></code>'
LESSON = '%s <b>%s</b> | %s\n'\
         '<i>%s</i> (%s)\n'\
         '<pre>%s</pre>\n'
# schedule_utils
YOUR_SCHEDULE = 'Ваш розклад:'
