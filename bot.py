# bot.py
# Telegram bot for basketball inspiration

import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set. Please set it before running the bot.")


# Text constants for both languages
TEXTS = {
    "ru": {
        "choose_language": "Пожалуйста, выберите язык 🌍",
        "language_ru": "Русский",
        "language_en": "English",
        "welcome_msg": """Привет ☀️

Хочешь летать, как Джордан? ☕️

Доминировать, как Коби? 🍿

Бросать трешки, как Карри? 💅""",
        "dream_button": "было бы неплохо 🏀",
        "dream_response": """Мечтать не вредно! ✨🌪☄️

А начать можно с простого — прийти на тренировку в это воскресенье 🙌🏻

Запись на занятие @Vladislava_Zhorzholiani 🐝""",
        "work_focus_btn": "Над чем работаем 🦾",
        "coach_info_btn": "О тренере 🎅🏼",
        "details_btn": "Детали 📌",
        "media_btn": "Медиа 🎬",
        "work_focus_msg": """→ специальная физическая подготовка 🦵

→ техническая подготовка (блоки: дриблинг, пассинг, защита, броски, входы, завершения) ⛹🏻‍♀️

→ взаимодействия (заслоны, игра против заслонов, игра в количественном преимуществе) 👬

→ игра 3х3, 4х4, 5х5 🎮

@Vladislava_Zhorzholiani ⬅️ записаться можно здесь""",
        "coach_info_msg": """Информация о тренере:

🏀 Игровой опыт — профессиональный клуб «Надежда» (Оренбург), КМС
🎓 Профильное образование: МГАФК и КГУФКСТ (бакалавриат)
🏆 Выступления за университетские команды и в лиге «Москвичка»

👟 Тренерская деятельность: практика в «Локомотиве», «Первый шаг», Академия ЦСКА. Опыт работы за рубежом.

📄 Все подтверждающие дипломы и сертификаты имеются, в том числе: курс повышения квалификации, курс персонального тренера тренажёрного зала, семинар «Движение вверх», EHCB Congress (EuroLeague Head Coaches Board), Gloria Sport Arena, Antalya.

💼 В настоящее время работаю проект-менеджером.
Тренировки — не основная деятельность, а возможность делать что-то по-настоящему классное и полезное.

🤍 В работе ценю индивидуальный подход, небольшие группы, безопасность и дружескую атмосферу.

@Vladislava_Zhorzholiani ⬅️ задать вопросы""",
        "details_msg": """Стоимость тренировок: 💎

🫂 Групповое занятие — 250k ₫ 
Площадка оплачивается отдельно — 30k ₫ 
(если сбор организует местный администратор)
🎟 Абонемент на групповые занятия (4 тренировки) — 800k ₫ 

🫵 Индивидуальное занятие — 400k ₫ 
🎟 Абонемент на 4 индивидуальные тренировки — 1200k ₫

Локация (https://maps.app.goo.gl/me8U2qbEep9wYKE57)📍

При себе нужно иметь:
👟 спортивную форму и обувь 
🥤 питьевую воду 
😉 хорошее настроение 
🏀 баскетбольный мяч

Расскажи о своем опыте игры @Vladislava_Zhorzholiani""",
        "media_msg": """Оставляю тут ссылку на мой <a href="https://www.instagram.com/zhorzholiani_vladislava?utm_source=qr&igsh=MWxmc2xpaGp2Y3E4aA==">профиль в инстаграме</a> 🤹‍♀️

Там можно посмотреть <b>видео</b>, посвященные тренировкам, 
чтобы получить представление процесса 🥁
в котором я приглашаю вас принять участие 🙏🏻"""
    },
    "en": {
        "choose_language": "Please choose your language 🌍",
        "language_ru": "Русский",
        "language_en": "English",
        "welcome_msg": """Hi ☀️

Want to fly like Jordan? ☕️

Dominate like Kobe? 🍿

Drain threes like Curry? 💅""",
        "dream_button": "Sounds good 🏀",
        "dream_response": """There's nothing wrong with dreaming big ✨
But every journey starts with a first step —
come to practice this Sunday 🙌🏻

@Vladislava_Zhorzholiani ✍️""",
        "work_focus_btn": "Training Focus 🦾",
        "coach_info_btn": "Coach Profile 🎅🏼",
        "details_btn": "Training Details 📌",
        "media_btn": "Media 🎬",
        "work_focus_msg": """→ Strength & Conditioning 🦵

→ Technical Skills
(dribbling, passing, defense, shooting, drives & finishes) ⛹🏻

→ Team Play & Tactics
(screens, defending screens, playing with numerical advantage) 👬

→ Game Play
3×3, 4×4, 5×5 🎮

📩 To sign up: @Vladislava_Zhorzholiani""",
        "coach_info_msg": """About the Coach

🏀 Playing experience — professional club "Nadezhda" (Orenburg), Candidate for Master of Sport (CMS)
🎓 Sports education — Moscow State Academy of Physical Education (bachelor's degree)
🏆 Competitive experience — university teams and the "Moskvichka league"

👟 Coaching experience — internships and coaching practice with "Lokomotiv", "First Step Academy", and "CSKA Basketball Academy".
International coaching experience abroad.

📄 Certifications & qualifications include:
advanced coaching courses, certified personal trainer course (gym-based), "Movement Up" seminar,
EHCB Congress (EuroLeague Head Coaches Board), Gloria Sports Arena, Antalya.

💼 Currently working as a project manager.
Coaching is not my main occupation, but a way to create something truly meaningful and impactful.

🤍 Coaching philosophy — individual approach, small groups, safety, and a supportive, friendly environment.

Feel free to ask: @Vladislava_Zhorzholiani""",
        "details_msg": """Training Prices: 💎

🫂 Group session — 250k ₫
Court fee is paid separately — 30k ₫
(if collected by the local administrator)

🎟 Group package (4 sessions) — 800k ₫

🫵 Individual session — 400k ₫ 
🎟 Individual package (4 sessions) — 1200k ₫

📍 Location:

What to bring:
👟 sportswear & sneakers
🥤 drinking water
😉 good mood
🏀 basketball

Book a session here: @Vladislava_Zhorzholiani""",
        "media_msg": """Check out my Instagram <a href="https://www.instagram.com/zhorzholiani_vladislava?utm_source=qr&igsh=MWxmc2xpaGp2Y3E4aA==">profile</a> 

Training videos to see how sessions look and feel 🙌🏻

🤍 I'd be really happy to have you join."""
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a language selection message when the command /start is issued."""
    try:
        # Reset language choice
        context.user_data["lang"] = None
        
        # Ask for language choice - show in English as requested
        keyboard = [
            [
                InlineKeyboardButton(TEXTS["ru"]["language_ru"], callback_data='set_lang_ru'),
                InlineKeyboardButton(TEXTS["en"]["language_en"], callback_data='set_lang_en')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(TEXTS["en"]["choose_language"], reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in start handler: {e}", exc_info=True)
        try:
            if update.message:
                await update.message.reply_text("Sorry, there was an error. Please try again.")
        except Exception:
            logger.error("Failed to send error message in start handler")


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set the language and continue with the selected language flow."""
    query = None
    try:
        query = update.callback_query
        await query.answer()
        
        # Extract language from callback data
        lang_parts = query.data.split('_')
        if len(lang_parts) < 3:
            raise ValueError(f"Invalid callback data format: {query.data}")
        lang = lang_parts[2]  # Either 'ru' or 'en'
        if lang not in TEXTS:
            raise ValueError(f"Unsupported language: {lang}")
        context.user_data["lang"] = lang
        
        # Send media group with 3 images
        media_group = [
            InputMediaPhoto("https://i.ibb.co/1D0XmFh/photo-2026-01-06-16-04-16.jpg"),
            InputMediaPhoto("https://i.ibb.co/VcDYXkCn/photo-2026-01-06-16-04-22.jpg"),
            InputMediaPhoto("https://i.ibb.co/zh1JgJ1z/photo-2026-01-06-16-04-25.jpg")
        ]
        await query.message.reply_media_group(media=media_group)
        
        # Get the appropriate texts based on selected language
        texts = TEXTS[lang]
        
        # Send the welcome message with inline button
        keyboard = [[InlineKeyboardButton(texts["dream_button"], callback_data='dream')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(texts["welcome_msg"], reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in set_language handler: {e}", exc_info=True)
        try:
            if query and query.message:
                await query.message.reply_text("Sorry, there was an error. Please try again.")
        except Exception:
            logger.error("Failed to send error message in set_language handler")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline button press."""
    try:
        query = update.callback_query
        
        # CallbackQueries need to be answered, even if no notification to the user is needed
        await query.answer()
        
        # Get language from context, default to ru if not set
        lang = context.user_data.get("lang", None)
        
        # If language is not set, show language selection
        if lang is None:
            keyboard = [
                [
                    InlineKeyboardButton(TEXTS["ru"]["language_ru"], callback_data='set_lang_ru'),
                    InlineKeyboardButton(TEXTS["en"]["language_en"], callback_data='set_lang_en')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(TEXTS["en"]["choose_language"], reply_markup=reply_markup)
            return
        
        texts = TEXTS[lang]
        
        # Create the inline keyboard with the required buttons
        keyboard = [
            [
                InlineKeyboardButton(texts["work_focus_btn"], callback_data='work_focus'),
                InlineKeyboardButton(texts["coach_info_btn"], callback_data='coach_info')
            ],
            [
                InlineKeyboardButton(texts["details_btn"], callback_data='details'),
                InlineKeyboardButton(texts["media_btn"], callback_data='media')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send the response message with inline keyboard attached in a single message
        response_message = texts["dream_response"]
        
        # Edit the original message instead of sending a new one
        await query.edit_message_text(text=response_message, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in button_handler: {e}", exc_info=True)
        try:
            query = update.callback_query
            if query:
                await query.edit_message_text(text="Sorry, there was an error. Please try again.", reply_markup=None)
        except Exception:
            logger.error("Failed to send error message in button_handler")


async def work_focus_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the 'work_focus' button."""
    try:
        query = update.callback_query
        
        # CallbackQueries need to be answered
        await query.answer()
        
        # Get language from context, default to ru if not set
        lang = context.user_data.get("lang", None)
        
        # If language is not set, show language selection
        if lang is None:
            keyboard = [
                [
                    InlineKeyboardButton(TEXTS["ru"]["language_ru"], callback_data='set_lang_ru'),
                    InlineKeyboardButton(TEXTS["en"]["language_en"], callback_data='set_lang_en')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(TEXTS["en"]["choose_language"], reply_markup=reply_markup)
            return
        
        texts = TEXTS[lang]
        
        work_focus_message = texts["work_focus_msg"]
        
        # Create the inline keyboard with the required buttons
        keyboard = [
            [
                InlineKeyboardButton(texts["work_focus_btn"], callback_data='work_focus'),
                InlineKeyboardButton(texts["coach_info_btn"], callback_data='coach_info')
            ],
            [
                InlineKeyboardButton(texts["details_btn"], callback_data='details'),
                InlineKeyboardButton(texts["media_btn"], callback_data='media')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the message using the query.edit_message_text method (which handles message_id and chat_id automatically)
        await query.edit_message_text(text=work_focus_message, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in work_focus_handler: {e}", exc_info=True)
        try:
            query = update.callback_query
            if query:
                await query.edit_message_text(text="Sorry, there was an error. Please try again.", reply_markup=None)
        except Exception:
            logger.error("Failed to send error message in work_focus_handler")


async def coach_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the 'coach_info' button."""
    try:
        query = update.callback_query
        
        # CallbackQueries need to be answered
        await query.answer()
        
        # Get language from context, default to ru if not set
        lang = context.user_data.get("lang", None)
        
        # If language is not set, show language selection
        if lang is None:
            keyboard = [
                [
                    InlineKeyboardButton(TEXTS["ru"]["language_ru"], callback_data='set_lang_ru'),
                    InlineKeyboardButton(TEXTS["en"]["language_en"], callback_data='set_lang_en')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(TEXTS["en"]["choose_language"], reply_markup=reply_markup)
            return
        
        texts = TEXTS[lang]
        
        coach_info_message = texts["coach_info_msg"]
        
        # Create the inline keyboard with the required buttons
        keyboard = [
            [
                InlineKeyboardButton(texts["work_focus_btn"], callback_data='work_focus'),
                InlineKeyboardButton(texts["coach_info_btn"], callback_data='coach_info')
            ],
            [
                InlineKeyboardButton(texts["details_btn"], callback_data='details'),
                InlineKeyboardButton(texts["media_btn"], callback_data='media')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the message using the query.edit_message_text method
        await query.edit_message_text(text=coach_info_message, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in coach_info_handler: {e}", exc_info=True)
        try:
            query = update.callback_query
            if query:
                await query.edit_message_text(text="Sorry, there was an error. Please try again.", reply_markup=None)
        except Exception:
            logger.error("Failed to send error message in coach_info_handler")


async def details_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the 'details' button."""
    try:
        query = update.callback_query
        
        # CallbackQueries need to be answered
        await query.answer()
        
        # Get language from context, default to ru if not set
        lang = context.user_data.get("lang", None)
        
        # If language is not set, show language selection
        if lang is None:
            keyboard = [
                [
                    InlineKeyboardButton(TEXTS["ru"]["language_ru"], callback_data='set_lang_ru'),
                    InlineKeyboardButton(TEXTS["en"]["language_en"], callback_data='set_lang_en')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(TEXTS["en"]["choose_language"], reply_markup=reply_markup)
            return
        
        texts = TEXTS[lang]
        
        details_message = texts["details_msg"]
        
        # Create the inline keyboard with the required buttons
        keyboard = [
            [
                InlineKeyboardButton(texts["work_focus_btn"], callback_data='work_focus'),
                InlineKeyboardButton(texts["coach_info_btn"], callback_data='coach_info')
            ],
            [
                InlineKeyboardButton(texts["details_btn"], callback_data='details'),
                InlineKeyboardButton(texts["media_btn"], callback_data='media')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the message using the query.edit_message_text method
        await query.edit_message_text(text=details_message, reply_markup=reply_markup, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error in details_handler: {e}", exc_info=True)
        try:
            query = update.callback_query
            if query:
                await query.edit_message_text(text="Sorry, there was an error. Please try again.", reply_markup=None)
        except Exception:
            logger.error("Failed to send error message in details_handler")


async def media_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the 'media' button."""
    try:
        query = update.callback_query
        
        # CallbackQueries need to be answered
        await query.answer()
        
        # Get language from context, default to ru if not set
        lang = context.user_data.get("lang", None)
        
        # If language is not set, show language selection
        if lang is None:
            keyboard = [
                [
                    InlineKeyboardButton(TEXTS["ru"]["language_ru"], callback_data='set_lang_ru'),
                    InlineKeyboardButton(TEXTS["en"]["language_en"], callback_data='set_lang_en')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(TEXTS["en"]["choose_language"], reply_markup=reply_markup)
            return
        
        texts = TEXTS[lang]
        
        media_message = texts["media_msg"]
        
        # Create the inline keyboard with the required buttons
        keyboard = [
            [
                InlineKeyboardButton(texts["work_focus_btn"], callback_data='work_focus'),
                InlineKeyboardButton(texts["coach_info_btn"], callback_data='coach_info')
            ],
            [
                InlineKeyboardButton(texts["details_btn"], callback_data='details'),
                InlineKeyboardButton(texts["media_btn"], callback_data='media')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the message using the query.edit_message_text method
        await query.edit_message_text(text=media_message, reply_markup=reply_markup, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error in media_handler: {e}", exc_info=True)
        try:
            query = update.callback_query
            if query:
                await query.edit_message_text(text="Sorry, there was an error. Please try again.", reply_markup=None)
        except Exception:
            logger.error("Failed to send error message in media_handler")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).connect_timeout(50.0).read_timeout(50.0).build()
    
    # Add callback query handler for language selection FIRST (to ensure priority)
    application.add_handler(CallbackQueryHandler(set_language, pattern='^set_lang_'))
    
    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^dream$'))
    application.add_handler(CallbackQueryHandler(work_focus_handler, pattern='^work_focus$'))
    application.add_handler(CallbackQueryHandler(coach_info_handler, pattern='^coach_info$'))
    application.add_handler(CallbackQueryHandler(details_handler, pattern='^details$'))
    application.add_handler(CallbackQueryHandler(media_handler, pattern='^media$'))
    
    # Add command handler for /start LAST (so it doesn't interfere with other handlers)
    application.add_handler(CommandHandler("start", start))
    
    # Run the bot until the user presses Ctrl-C
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()