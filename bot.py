import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from collector import get_education_news

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 التسجيلات المفتوحة", callback_data="open")],
        [InlineKeyboardButton("📅 التسجيلات القادمة", callback_data="upcoming")],
        [InlineKeyboardButton("⏳ التي ستغلق قريبًا", callback_data="closing")],
        [InlineKeyboardButton("🏛️ حسب القطاع", callback_data="sectors")],
        [InlineKeyboardButton("📍 حسب الولاية", callback_data="wilaya")],
    ]

    await update.message.reply_text(
        "🇩🇿 أهلاً بك في بوت ورقتي\n\n"
        "نساعدك في العثور على التسجيلات والمسابقات والخدمات الرسمية في الجزائر.\n\n"
        "اختر ما تريد:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "open": "📢 التسجيلات المفتوحة\n\n🚧 سيتم إضافة التسجيلات الرسمية هنا.",
        "upcoming": "📅 التسجيلات القادمة\n\n🚧 سيتم إضافة التسجيلات القادمة هنا.",
        "closing": "⏳ التي ستغلق قريبًا\n\n🚧 سيتم إضافة التنبيهات هنا.",
        "sectors": "🏛️ حسب القطاع\n\n🎓 التعليم\n💼 التوظيف\n🏠 السكن\n🎓 التعليم العالي\n🔧 التكوين المهني\n⚖️ العدل\n🪪 الخدمات الإدارية",
        "wilaya": "📍 حسب الولاية\n\n🚧 سيتم إضافة البحث حسب الولاية هنا."
    }

    await query.edit_message_text(messages.get(query.data, "❌ خطأ"))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ استعمل /start لفتح القائمة الرئيسية."
    )


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🇩🇿 War9ati Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()