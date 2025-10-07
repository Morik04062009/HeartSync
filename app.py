import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from handlers.start import start, cancel, handle_gender, handle_name, handle_age, handle_description, handle_photo, \
    handle_interests
from handlers.profile import profile, edit_profile, my_profile, handle_edit_choice
from handlers.search import search_profiles, like_profile, skip_profile, super_like_profile, show_likes
from handlers.matches import matches_list, handle_match_action
from handlers.chat import start_chat, send_message, chat_list, handle_chat_choice
from handlers.admin import admin_panel, broadcast_message, stats
from utils.filters import AdminFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("search", search_profiles))
    application.add_handler(CommandHandler("matches", matches_list))
    application.add_handler(CommandHandler("chats", chat_list))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("admin", admin_panel, filters=AdminFilter()))
    application.add_handler(CommandHandler("stats", stats, filters=AdminFilter()))
    application.add_handler(CommandHandler("broadcast", broadcast_message, filters=AdminFilter()))

    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^💫 Мой профиль$"), my_profile))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔍 Поиск$"), search_profiles))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^💌 Мои симпатии$"), show_likes))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^💞 Взаимные симпатии$"), matches_list))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^💬 Чаты$"), chat_list))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^✨ Редактировать$"), edit_profile))

    application.add_handler(CallbackQueryHandler(handle_gender, pattern="^gender_"))
    application.add_handler(CallbackQueryHandler(handle_edit_choice, pattern="^edit_"))
    application.add_handler(CallbackQueryHandler(like_profile, pattern="^like_"))
    application.add_handler(CallbackQueryHandler(skip_profile, pattern="^skip_"))
    application.add_handler(CallbackQueryHandler(super_like_profile, pattern="^super_"))
    application.add_handler(CallbackQueryHandler(handle_match_action, pattern="^match_"))
    application.add_handler(CallbackQueryHandler(handle_chat_choice, pattern="^chat_"))
    application.add_handler(CallbackQueryHandler(start_chat, pattern="^startchat_"))

    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description))

    application.run_polling()
    logger.info("💫 HeartSync бот запущен! by MIDWALE")

# by Midwale @midwale


if __name__ == "__main__":
    main()