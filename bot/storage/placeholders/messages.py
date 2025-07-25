# favorites
from bot.storage.placeholders import buttons

BOT_DEPRECATED_MESSAGE = """
<strong><b>! Розклад переїхав до @TechSupportUKD_bot !</b></strong>

<b>📘 @TechSupportUKD_bot: Технічний асистент університету</b>

• ❓ <b>Популярні питання</b> — перелік поширених запитань і відповідей. Часто саме там є розв’язок вашої проблеми.

• 🔑 <b>Вхід у СДО</b> — скидання паролю (за умови введеної пошти) та інструкції для авторизації на різних пристроях.

• 📚 <b>Відсутні курси або екзамени</b> — автоматичне вирішення проблем із відсутніми курсами чи екзаменами.

• 📅 <b>Розклад занять</b> — перегляд розкладу для студентів і викладачів, а також інформація про вільні аудиторії.

• 🔬 <b>Предмети та вибіркові дисципліни</b> — інформація про ваші предмети, вибіркові дисципліни та посилання для їх вибору.

• 👤 <b>Інформація про студента</b> — дані про групу, пошту, освітній ступінь і статус відрахування.

• 🧑‍💼 <b>Зв'язок зі спеціалістом</b> — можливість <u>задати питання</u> та <u>переглянути історію звернень</u>.

• 🎓 <b>Академічна успішність</b> — перегляд оцінок за всіма дисциплінами.

<i>Система створена для того, щоб надати вам максимальний комфорт та самостійний доступ до важливої інформації.</i>
"""

SELECT_FROM_LIST = 'Виберіть зі списку:'
NOT_PICKED_ANY_GROUP = 'Схоже, ви не додали жодної групи в обрані!'
NOT_FOUND_OR_DELETED = 'Схоже, даний розклад не було знайдено або його було видалено'

# menu
PICK_OPTION = 'Будь ласка, виберіть бажану опцію:'
TIP = 'От халепа! Схоже, ви ще не додали основний розклад! Підказати як це зробити?'

# schedule buttons
MENU = '<em><strong>Головне меню!</strong></em>'
TIP_ANSWER = f'Натисніть кнопку <b><i>{buttons.FIND_SCHEDULE}</i></b>.\n\nЗдійсніть пошук за групою чи викладачем/-кою.' \
             'Щойно розклад відобразиться, оберіть пункт <b><i>"Позначити основним"</i></b>.\n\n' \
             'Виконавши ці кроки, обраний розклад з\'явиться в панелі ' \
             '<b><i>"Мій розклад"</i></b>.'

# search
SEARCH_PARAMS = 'Оберіть параметри пошуку розкладу: '
CHOOSE_ROLE = 'Вкажіть роль:'
GROUP_FULL_NAME = 'Надішліть повну назву шуканої групи:'
DEGREE_TYPE = 'Оберіть форму навчання'
INSTITUTION_TYPE = 'Оберіть НЗ'

PICK_SPECIALITY = 'Оберіть спеціальність:'
PICK_SPECIALITY_FAIL = 'Оберіть спеціальність:'

TEACHER_SELECT = "Оберіть викладача/ку із запропонованих:"
TEACHER_INITIALS = "Введіть П.І.Б. викладача/ки:"
TEACHER_INITIALS_FAIL = "Введіть П.І.Б. викладача/ки:"
TEACHER_NOT_FOUND = 'Викладача/ку не знайдено! Спробуйте ще раз!'

COURSE_NUM = '%s курс'
COURSE_SELECT = 'Оберіть курс:'
COURSE_SELECT_FAIL = 'Будь ласка, оберіть курс!'

GROUP_SELECT = 'Оберіть групу:'
GROUP_SELECT_FAIL = 'Будь ласка, оберіть групу!'
GROUP_NOT_FOUND = 'Групу не знайдено! Спробуйте ще раз.'

# settings
SETTINGS_INFO = 'Ви в меню нашалаштувань!'
YOUR_SETTINGS = 'Ваші поточні налаштування:'

# start
WELCOME = """Привіт та ласкаво просимо! 🤗
Мета даного бота - допомога у пошуку розкладу 
для всіх учасників освітнього процесу Університету Короля Данила!

Щоб ознайомитися із повним списком команд та можливостей, 
перейдіть на сторінку допомоги за допомогою команди /help. \n
Готові? Отож, розпочнімо!⚡️"""

#    UTILS
# render_schedule
NO_CLASSES = '\nНа заданому проміжку часу пари відсутні, хорошого відпочинку!'
BREAK_LINE = '_' * 35
CLASSES_QUANTITY = f'{BREAK_LINE}\n' \
                   '<code>Загальна кількість пар: %s </code>'
SEARCH_NAME = '<code><u>%s</u></code>'
DAY_AND_DATE = '<code><u>%s, %s</u></code>'
LESSON = '%s <b>%s</b> | %s\n' \
         '<i>%s</i> %s %s\n' \
         '<pre>%s</pre>\n' \
         '<b>%s</b>\n'
ADDITIONS_TO_LESSON = '\n%s\n' \
                      '%s\n'
ERROR_NOT_EXIST = 'Отакої! Розклад відсутній!'
ERROR_OBJECT_NOT_EXIST = 'Отакої! Групу/викладача не знайдено!'
ERROR_BLOCKED = 'Розклад заблокований адміністратором'
ERROR_ERROR = 'Халепа! Схоже, виникла помилка. Зверніться до адміністратора'
ERROR_SERVER = 'Халепа! Схоже, виникла помилка сервера'
# schedule_utils
YOUR_SCHEDULE = 'Ваш розклад:'

# help text
HELP = """
<i><b>Команди</b></i>:
/start - перезапуск бота;
/cancel - скасування дії;
/settings - налаштування бота;
/help - виклик допомоги;


<i><b>Функціонал</b></i>:
Для пошуку розкладу за критеріями потрібно обрати <i>спеціальність, курс та групу</i>.
Для пошуку розкладу за назвою групи потрібно ввести <i>повну назву вашої групи</i> (наприклад "ІПЗс-21-2").
Для пошуку розкладу за викладачем/кою потрібно ввести <i>П.І.Б. викладача/ки</i> 
(наприклад "Іваненко Іван Іванович", або ж просто "Іваненко").
<i>За замовчуванням бот видає розклад на сьогоднішній день.</i>


<i><b>Мій розклад</b></i>:
Щоб позначити розклад основним, знайдіть бажаний розклад на натисніть кнопку <b>"Позначити основним"</b> на клавіатурі нижче.
Тепер цей розклад буде доступним за одним лише натиском кнопки <b>"Мій розклад"</b> в головному меню. 
Окрім того, якщо в налаштуваннях обрано <b>"Надсилати розклад зранку: Так"</b>, 
о 6:00 ранку ви отримуватимете повідомлення з цим розкладом на сьогодні.


<i><b>Обрані</b></i>:
Щоб додати розклад в обрані, знайдіть бажаний розклад та натисніть кнопку <b>"В обране"</b> на клавіатурі нижче.
Тепер цей розклад можна буде швидко знайти в списку обраних, що доступний за кнопкою <b>"Обрані"</b> в головному меню.


При виявленні будь-яких технічних несправностей, просимо звертатись на пошту tel.admin@ukd.edu.ua.
<code>З найкращими побажаннями, розробники.</code>
"""
