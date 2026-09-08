import telebot
from telebot import types

TOKEN = "8203196013:AAGut2-WTs_WwipIzLHd5pszqcxZ2tNQv4E"
bot = telebot.TeleBot(TOKEN)

# --- ХРАНИЛИЩЕ ССЫЛОК ---

# Ссылки на теорию
theory_links = {
    "lesson1": "https://gannamath2026.github.io/trenager_programs/json_files/ege-1.json",
    "lesson2": "https://gannamath2026.github.io/trenager_programs/json_files/ege-1.json",
    "lesson3": "https://gannamath2026.github.io/trenager_programs/json_files/ege-1.json",
}

# Ссылки на домашние задания
homework_links = {
    "1": "https://gannamath2026.github.io/trenager_programs/json_files/СТРУКТУРА%20ЕГЭ%20МАТЕМАТИКА/00%20%20НЕДЕЛЯ%201/ПАРАМЕТРЫ%2018%20-%20%206%20ЗАДАЧ.pdf",
    "2": "https://gannamath2026.github.io/trenager_programs/json_files/СТРУКТУРА%20ЕГЭ%20МАТЕМАТИКА/00%20%20НЕДЕЛЯ%201/ПАРАМЕТРЫ%2018%20-%20%206%20ЗАДАЧ.pdf",
    "3": "https://gannamath2026.github.io/trenager_programs/json_files/СТРУКТУРА%20ЕГЭ%20МАТЕМАТИКА/00%20%20НЕДЕЛЯ%201/ПАРАМЕТРЫ%2018%20-%20%206%20ЗАДАЧ.pdf",
}

# Ссылки на видеоразборы (Rutube)
video_links = {
    "lesson1": "https://rutube.ru/video/f3f188baeb8cfc8bd23de567131d48d1/",
    "lesson2": "https://rutube.ru/video/f3f188baeb8cfc8bd23de567131d48d1/",
    "lesson3": "https://rutube.ru/video/f3f188baeb8cfc8bd23de567131d48d1/",
}

# --- КОМАНДА /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_theory = types.KeyboardButton("📖 Теория")
    btn_homework = types.KeyboardButton("📝 Домашнее задание")
    btn_videos = types.KeyboardButton("🎥 Видеоразборы")
    btn_help = types.KeyboardButton("❓ Помощь")

    keyboard.add(btn_theory, btn_homework, btn_videos, btn_help)

    bot.send_message(
        message.chat.id,
        "📚 Добро пожаловать в учебный бот!\n\n"
        "Выберите раздел, нажав на кнопку ниже:",
        reply_markup=keyboard
    )

# --- ОБРАБОТЧИК КНОПОК ---
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id

    # ===== ТЕОРИЯ =====
    if message.text == "📖 Теория":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("Урок 1. Введение", callback_data="theory_lesson1")
        btn2 = types.InlineKeyboardButton("Урок 2. Основы", callback_data="theory_lesson2")
        btn3 = types.InlineKeyboardButton("Урок 3. Практика", callback_data="theory_lesson3")
        btn_back = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")

        keyboard.add(btn1, btn2, btn3, btn_back)
        bot.send_message(chat_id, "📖 Выберите урок:", reply_markup=keyboard)

    # ===== ДОМАШНЕЕ ЗАДАНИЕ =====
    elif message.text == "📝 Домашнее задание":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("ДЗ к уроку 1", callback_data="homework_1")
        btn2 = types.InlineKeyboardButton("ДЗ к уроку 2", callback_data="homework_2")
        btn3 = types.InlineKeyboardButton("ДЗ к уроку 3", callback_data="homework_3")
        btn_back = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")

        keyboard.add(btn1, btn2, btn3, btn_back)
        bot.send_message(chat_id, "📝 Выберите домашнее задание:", reply_markup=keyboard)

    # ===== ВИДЕОРАЗБОРЫ =====
    elif message.text == "🎥 Видеоразборы":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("Разбор урока 1", callback_data="video_lesson1")
        btn2 = types.InlineKeyboardButton("Разбор урока 2", callback_data="video_lesson2")
        btn3 = types.InlineKeyboardButton("Разбор урока 3", callback_data="video_lesson3")
        btn_back = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")

        keyboard.add(btn1, btn2, btn3, btn_back)
        bot.send_message(
            chat_id,
            "🎥 Выберите видеоразбор на Rutube:",
            reply_markup=keyboard
        )

    # ===== ПОМОЩЬ =====
    elif message.text == "❓ Помощь":
        bot.send_message(
            chat_id,
            "❓ Как пользоваться ботом:\n\n"
            "1. Нажмите 📖 Теория — бот даст ссылку на материал\n"
            "2. Нажмите 📝 Домашнее задание — бот даст ссылку на ДЗ\n"
            "3. Нажмите 🎥 Видеоразборы — бот даст ссылку на Rutube\n\n"
            "Все ссылки открываются в браузере."
        )

    else:
        bot.send_message(
            chat_id,
            "❓ Я не понимаю эту команду.\n"
            "Нажмите кнопку с нужным разделом или /start для перезапуска."
        )

# --- ОБРАБОТЧИК НАЖАТИЙ НА INLINE-КНОПКИ ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    # ---- ТЕОРИЯ (ОТПРАВЛЯЕМ ССЫЛКУ) ----
    if data.startswith("theory_"):
        lesson = data.replace("theory_", "")
        link = theory_links.get(lesson)

        if link:
            bot.send_message(
                chat_id,
                f"📖 **{lesson.replace('lesson', 'Урок')}**\n\n"
                f"🔗 Ссылка на материал:\n{link}\n\n"
                "👆 Нажмите на ссылку, чтобы открыть файл."
            )
            bot.answer_callback_query(call.id, "✅ Ссылка отправлена!")
        else:
            bot.send_message(chat_id, f"❌ Ссылка на урок {lesson} не найдена.")
            bot.answer_callback_query(call.id, "❌ Ссылка не найдена")

    # ---- ДЗ (ОТПРАВЛЯЕМ ССЫЛКУ) ----
    elif data.startswith("homework_"):
        lesson = data.replace("homework_", "")
        link = homework_links.get(lesson)

        if link:
            bot.send_message(
                chat_id,
                f"📝 **Домашнее задание к уроку {lesson}**\n\n"
                f"🔗 Ссылка на файл:\n{link}\n\n"
                "👆 Нажмите на ссылку, чтобы открыть задание."
            )
            bot.answer_callback_query(call.id, "✅ Ссылка отправлена!")
        else:
            bot.send_message(chat_id, f"❌ Ссылка на ДЗ к уроку {lesson} не найдена.")
            bot.answer_callback_query(call.id, "❌ Ссылка не найдена")

    # ---- ВИДЕО (ОТПРАВЛЯЕМ ССЫЛКУ НА RUTUBE) ----
    elif data.startswith("video_"):
        lesson = data.replace("video_", "")
        link = video_links.get(lesson)

        if link:
            bot.send_message(
                chat_id,
                f"🎥 **Видеоразбор к {lesson.replace('lesson', 'уроку')}**\n\n"
                f"📺 Смотреть на Rutube:\n{link}\n\n"
                "👆 Нажмите на ссылку, чтобы открыть видео."
            )
            bot.answer_callback_query(call.id, "✅ Ссылка отправлена!")
        else:
            bot.send_message(chat_id, f"❌ Ссылка на видео к уроку {lesson} не найдена.")
            bot.answer_callback_query(call.id, "❌ Ссылка не найдена")

    # ---- НАЗАД ----
    elif data == "back_to_menu":
        bot.delete_message(chat_id, message_id)
        send_welcome(call.message)
        bot.answer_callback_query(call.id, "🔙 Возврат в меню")

# --- ЗАПУСК ---
print("✅ Бот запущен и готов к работе!")
bot.polling()