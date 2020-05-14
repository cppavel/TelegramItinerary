import telebot
import dataBase


users = {}

bot = telebot.TeleBot("TOKEN")
db = dataBase.DataBase()
db.createEventsTable()
db.createTasksTable()

@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.from_user.id,"""/reg for registration. Вы можете продолжить без регистрации, если хотите.
    \n /addevent - добавить событие \n /addtask - добавить задание \n /deleteevent - удалить событие \n /deletetask - удалить задание
    \n /deleteuser - удалить пользователя со всеми заданиями (работает после регистрации)
    \n /getevents - получить события по параметрам
    \n /gettasks - получить задания по параметрам
    \n /settaskdone - пометить задание как сделанное""")

@bot.message_handler(commands=['reg'])
def register(message):
    db.addUser(message.from_user.id)
    bot.send_message(message.from_user.id, "Успешно зарегистрирован")

@bot.message_handler(commands=['addevent'])
def add_event(message):
    bot.send_message(message.from_user.id, 'Каково название твоего события?')
    bot.register_next_step_handler(message, get_event_name)

def get_event_name(message):
    global  users;
    users[message.from_user.id] ={}
    users[message.from_user.id]['name'] = message.text
    bot.send_message(message.from_user.id,'Какая категория у твоего события?')
    bot.register_next_step_handler(message, get_event_category)

def get_event_category(message):
    global users;
    users[message.from_user.id]['category'] = message.text
    bot.send_message(message.from_user.id,'Опиши свое событие?')
    bot.register_next_step_handler(message, get_event_description)

def get_event_description(message):
    global users;
    users[message.from_user.id]['description'] = message.text
    bot.send_message(message.from_user.id,'Введи время и дату события в формате YYYY.MM.DD-tt:tt')
    bot.register_next_step_handler(message, get_event_date)

def get_event_date(message):
    global users;
    try:
        datestr = message.text;
        datestrcpy = datestr
        datestr = datestr.replace(".", "")
        datestr = datestr.replace("-", "")
        datestr = datestr.replace(":", "")
        users[message.from_user.id]['date'] = int(datestr)
        db.addEvent(message.from_user.id,  users[message.from_user.id]['name'],users[message.from_user.id]['category']
                    , users[message.from_user.id]['description'], users[message.from_user.id]['date'])
        bot.send_message(message.from_user.id,
                         "Имя вашего события: " +
                         users[message.from_user.id]['name'] + "\nкатегория: " +
                         users[message.from_user.id]['category'] + "\nописание: " +
                         users[message.from_user.id]['description'] + "\nдата: " + datestrcpy)
        bot.send_message(message.from_user.id, "Событие успешно создано")
    except Exception:
        bot.send_message(message.from_user.id,"Введите еще раз, например 2019.12.25-01:00")
        bot.register_next_step_handler(message, get_event_date)

@bot.message_handler(commands=['addtask'])
def add_task(message):
    bot.send_message(message.from_user.id, 'Каково название твоего задания?')
    bot.register_next_step_handler(message, get_task_name)

def get_task_name(message):
    global users;
    users[message.from_user.id] = {}
    users[message.from_user.id]['name'] = message.text
    bot.send_message(message.from_user.id,'Какая категория у твоего задания?')
    bot.register_next_step_handler(message, get_task_category)

def get_task_category(message):
    global users;
    users[message.from_user.id]['category'] = message.text
    bot.send_message(message.from_user.id,'Опиши свое задание?')
    bot.register_next_step_handler(message, get_task_description)

def get_task_description(message):
    global users;
    users[message.from_user.id]['description'] = message.text
    bot.send_message(message.from_user.id,'Введи дедлайн задания в формате YYYY.MM.DD-tt:tt')
    bot.register_next_step_handler(message, get_task_deadline)

def get_task_deadline(message):
    global users;
    try:
        deadlinestr = message.text;
        deadlinestrcpy = deadlinestr
        deadlinestr = deadlinestr.replace(".", "")
        deadlinestr = deadlinestr.replace("-", "")
        deadlinestr = deadlinestr.replace(":", "")
        users[message.from_user.id]['deadline'] = int(deadlinestr)
        db.addTask(message.from_user.id,  users[message.from_user.id]['name'],users[message.from_user.id]['category'],
                     users[message.from_user.id]['description'],
                        users[message.from_user.id]['deadline'],"false")
        bot.send_message(message.from_user.id,
                         "Имя вашего события: " +
                         users[message.from_user.id]['name'] + "\nкатегория: " +
                         users[message.from_user.id]['category'] + "\nописание: " +
                         users[message.from_user.id]['description'] +
                            "\nдедлайн: " + deadlinestrcpy +"\nстатус: не выполнен" )
        bot.send_message(message.from_user.id, "Задание успешно создано")
    except Exception :
        bot.send_message(message.from_user.id,"Введите еще раз, например 2019.12.25-01:00")
        bot.register_next_step_handler(message, get_task_deadline)

@bot.message_handler(commands=['deleteevent'])
def delete_event(message):
    global users;
    users[message.from_user.id] = {}
    bot.send_message(message.from_user.id, 'Каково название твоего события?')
    bot.register_next_step_handler(message, delete_event_by_name)

def delete_event_by_name(message):
    global users;
    users[message.from_user.id]['name'] = message.text
    bot.send_message(message.from_user.id,'Какова дата твоего события (в формате YYYY.MM.DD-tt:tt)')
    bot.register_next_step_handler(message, delete_event_by_date)

def delete_event_by_date(message):
    global users;
    try:
        datestr = message.text;
        datestr = datestr.replace(".", "")
        datestr = datestr.replace("-", "")
        datestr = datestr.replace(":", "")
        users[message.from_user.id]['date'] = int(datestr)
        keyboard = telebot.types.InlineKeyboardMarkup();
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yesE');
        keyboard.add(key_yes);
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='noE');
        keyboard.add(key_no);
        question = 'Ты уверен(-а)?';
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    except Exception:
        bot.send_message(message.from_user.id, "Введите еще раз, например 2019.12.25-01:00")
        bot.register_next_step_handler(message, delete_event_by_date)

@bot.message_handler(commands=['deletetask'])
def delete_task(message):
    global users;
    users[message.from_user.id] = {}
    bot.send_message(message.from_user.id, 'Каково название твоего задания?')
    bot.register_next_step_handler(message, delete_task_by_name)

def delete_task_by_name(message):
    global users;
    users[message.from_user.id]['name'] = message.text
    bot.send_message(message.from_user.id,'Каков дедлайн твоего задания (в формате YYYY.MM.DD-tt:tt)')
    bot.register_next_step_handler(message, delete_task_by_deadline)

def delete_task_by_deadline(message):
    global users;
    try:
        deadlinestr = message.text;
        deadlinestr = deadlinestr.replace(".", "")
        deadlinestr = deadlinestr.replace("-", "")
        deadlinestr = deadlinestr.replace(":", "")
        users[message.from_user.id]['deadline'] = int(deadlinestr)
        keyboard = telebot.types.InlineKeyboardMarkup();
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yesT');
        keyboard.add(key_yes);
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='noT');
        keyboard.add(key_no);
        question = 'Ты уверен(-а)?';
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    except Exception:
        bot.send_message(message.from_user.id, "Введите еще раз, например 2019.12.25-01:00")
        bot.register_next_step_handler(message, delete_task_by_deadline)

@bot.message_handler(commands=['deleteuser'])
def delete_user(message):
    global users;
    users[message.from_user.id] = {}
    keyboard = telebot.types.InlineKeyboardMarkup();
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yesU');
    keyboard.add(key_yes);
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='noU');
    keyboard.add(key_no);
    question = 'Ты уверен(-а)?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.message_handler(commands=['getevents'])
def get_events(message):
    global users;
    users[message.from_user.id] = {}
    bot.send_message(message.from_user.id, 'Каков временной период? Введи его в формате YYYY.MM.DD-YYYY.MM.DD. Введи: none, если не важно ')
    bot.register_next_step_handler(message, get_events_time_period)

def get_events_time_period(message):
    global users;
    try:
        if not message.text == "none":
            dates = message.text.split('-')
            users[message.from_user.id]['date1'] = int(dates[0].replace('.','') +"0000")
            users[message.from_user.id]['date2'] = int(dates[1].replace('.','') +"0000")
        else:
            users[message.from_user.id]['date1'] = -1
            users[message.from_user.id]['date2'] = -1
        bot.send_message(message.from_user.id, 'Какая категория тебя интересует. Введи: none, если не важно')
        bot.register_next_step_handler(message, get_events_category)
    except:
        bot.send_message(message.from_user.id, 'Введи его в формате YYYY.MM.DD-YYYY.MM.DD')
        bot.register_next_step_handler(message, get_events_time_period)

def get_events_category(message):
    global users;
    users[message.from_user.id]['category'] = message.text
    data = db.getEvents(message.from_user.id,users[message.from_user.id]['date1'],users[message.from_user.id]['date2'],
                        users[message.from_user.id]['category'])
    bot.send_message(message.from_user.id, "Результат:\n\n"+eventConvertToString(data))


@bot.message_handler(commands=['gettasks'])
def get_tasks(message):
    global users;
    users[message.from_user.id] = {}
    bot.send_message(message.from_user.id, 'Каков дедлайн? Введи его в формате YYYY.MM.DD Введи: none, если не важно ')
    bot.register_next_step_handler(message, get_tasks_time_period)

def get_tasks_time_period(message):
    global users;
    try:
        if not message.text == "none":
            users[message.from_user.id]['deadline'] = int(message.text.replace('.','') +"0000")
        else:
            users[message.from_user.id]['deadline'] = -1
        bot.send_message(message.from_user.id, 'Какая категория тебя интересует. Введи: none, если не важно')
        bot.register_next_step_handler(message, get_tasks_category)
    except:
        bot.send_message(message.from_user.id, 'Введи его в формате YYYY.MM.DD')
        bot.register_next_step_handler(message, get_tasks_time_period)

def get_tasks_category(message):
    global users;
    users[message.from_user.id]['category'] = message.text
    keyboard = telebot.types.InlineKeyboardMarkup();
    key_yes = telebot.types.InlineKeyboardButton(text='Выполненные', callback_data='yesS');
    keyboard.add(key_yes);
    key_no = telebot.types.InlineKeyboardButton(text='Не выполненные', callback_data='noS');
    keyboard.add(key_no);
    question = 'Выбери?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.message_handler(commands=['settaskdone'])
def set_task_done(message):
    global users;
    users[message.from_user.id] = {}
    users[message.from_user.id]['id'] = message.from_user.id
    bot.send_message(message.from_user.id, 'Каково имя задания?')
    bot.register_next_step_handler(message, set_task_done_name)

def set_task_done_name(message):
    global users;
    users[message.from_user.id]['name'] = message.text
    bot.send_message(message.from_user.id,'Каков дедлайн? Введи его в формате YYYY.MM.DD-tt:tt')
    bot.register_next_step_handler(message, set_task_done_deadline)

def set_task_done_deadline(message):
    global users;
    try:
        datestr = message.text;
        datestr = datestr.replace(".", "")
        datestr = datestr.replace("-", "")
        datestr = datestr.replace(":", "")
        users[message.from_user.id]['deadline'] = int(datestr)
        db.changetaskStatus(message.from_user.id,users[message.from_user.id]['name'],
                            users[message.from_user.id]['deadline'],"true")
        bot.send_message(message.from_user.id, "Отмечено как сделанное!")
    except Exception:
        bot.send_message(message.from_user.id, "Введите еще раз, например 2019.12.25-01:00")
        bot.register_next_step_handler(message, set_task_done_deadline)







@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    id = call.from_user.id
    if call.data == "yesT":
        db.deleteTask(id, users[id]['name'], users[id]['deadline'])
        bot.send_message(call.message.chat.id, "Задание успешно удалено")

    if call.data == "yesE":
        db.deleteEvent(id, users[id]['name'], users[id]['date'])
        bot.send_message(call.message.chat.id, "Событие успешно удалено")

    if call.data == "yesU":
        db.deleteUser(id)
        bot.send_message(call.message.chat.id, "Все данные о пользователе удалены успешно")

    if call.data == "yesS":
        data = db.getTasks(id,users[id]['deadline'],users[id]['category'] ,"true")
        bot.send_message(call.message.chat.id, "Результат:\n\n"+taskConvertToString(data))

    if call.data == "noS":
        data = db.getTasks(id,users[id]['deadline'],users[id]['category'] ,"false")
        bot.send_message(call.message.chat.id, "Результат:\n\n"+taskConvertToString(data))


def eventConvertToString(data):
    strr = ''
    for x in data:
        strr += 'Имя: '+x[1] +"\n"
        strr += 'Категория: ' + x[2] +"\n"
        strr += 'Описание: ' + x[3] +"\n"
        date = str(x[4])
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        hour = date[8:10]
        minutes = date[10:]
        strr +='Дата: ' + year + '.' + month + '.' + day + ' Время: ' + hour +':'+minutes +"\n"
        strr = strr +"\n\n\n"

    return strr

def taskConvertToString(data):
    strr = ''
    for x in data:
        strr += 'Имя: '+x[1] +"\n"
        strr += 'Категория: ' + x[2] +"\n"
        strr += 'Описание: ' + x[3] +"\n"
        deadline = str(x[4])
        year = deadline[0:4]
        month = deadline[4:6]
        day = deadline[6:8]
        hour = deadline[8:10]
        minutes = deadline[10:]
        strr +='Дедлайн - Дата: ' + year + '.' + month + '.' + day + ' Время: ' + hour +':'+minutes +"\n"
        if x[5] == "true":
            strr += 'Статус: Выполнено'
        else:
            strr +='Статус: Не выполнено'
        strr = strr +"\n\n\n"

    return strr

if __name__ == "__main__":
    bot.polling()


