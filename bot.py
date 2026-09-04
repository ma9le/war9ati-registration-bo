import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from collector import get_education_news


logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def main_menu():
    keyboard = [
        [InlineKeyboardButton("📢 التسجيلات المفتوحة", callback_data="open")],
        [InlineKeyboardButton("📅 التسجيلات القادمة", callback_data="upcoming")],
        [InlineKeyboardButton("⏳ التي ستغلق قريبًا", callback_data="closing")],
        [InlineKeyboardButton("🏛️ حسب القطاع", callback_data="sectors")],
        [InlineKeyboardButton("📍 حسب الولاية", callback_data="wilaya")],
        [InlineKeyboardButton("🔄 تحديث", callback_data="refresh")]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇩🇿 أهلاً بك في بوت ورقتي\n\n"
        "📋 التسجيلات والمسابقات والخدمات الرسمية في الجزائر.\n\n"
        "اختر ما تريد:",
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ["open", "refresh"]:

        news = get_education_news()

        if not news:
            text = (
                "📢 التسجيلات المفتوحة\n\n"
                "⚠️ لم يتم العثور على إعلانات حاليًا."
            )
        else:
            text = "📢 آخر الإعلانات الرسمية:\n\n"

            for item in news:
                text += (
                    f"📌 {item['title']}\n"
                    f"🔗 {item['url']}\n\n"
                )

    elif query.data == "upcoming":

        text = (
            "📅 التسجيلات القادمة\n\n"
            "🚧 سيتم إضافة نظام اكتشاف التسجيلات القادمة."
        )

    elif query.data == "closing":

        text = (
            "⏳ التسجيلات التي ستغلق قريبًا\n\n"
            "🚧 سيتم إضافة نظام حساب تاريخ الغلق."
        )

    elif query.data == "sectors":

        text = (
            "🏛️ القطاعات\n\n"
            "🎓 التربية\n"
            "🏫 التعليم العالي\n"
            "💼 التوظيف\n"
            "🔧 التكوين المهني\n"
            "🏠 السكن\n"
            "⚖️ العدل\n"
            "🪪 الخدمات الإدارية\n"
            "🛡️ الأمن والدفاع"
        )

    elif query.data == "wilaya":

        text = (
            "📍 حسب الولاية\n\n"
            "🚧 سيتم إضافة الولايات الـ58."
        )

    else:
        text = "❌ حدث خطأ."

    await query.edit_message_text(
        text,
        reply_markup=main_menu()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ أرسل /start لفتح القائمة الرئيسية."
    )


def main():

    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🇩🇿 War9ati Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()