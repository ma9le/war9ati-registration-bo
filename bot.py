import os
import logging
import requests
from bs4 import BeautifulSoup

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

EDUCATION_URL = "https://www.education.gov.dz/"


def get_education_news():
    try:
        r = requests.get(
            EDUCATION_URL,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        for link in soup.find_all("a", href=True):
            title = link.get_text(" ", strip=True)
            url = link["href"]

            if not title:
                continue

            if url.startswith("/"):
                url = EDUCATION_URL.rstrip("/") + url

            if url.startswith("http"):
                results.append((title, url))

        return results[:15]

    except Exception as e:
        logging.error(e)
        return []


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
        "اختر الخدمة التي تريدها:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "open":
        news = get_education_news()

        if news:
            text = "📢 منشورات وزارة التربية:\n\n"

            for title, url in news:
                text += f"📌 {title}\n🔗 {url}\n\n"
        else:
            text = "⚠️ تعذر جلب المنشورات حاليًا."

    elif query.data == "upcoming":
        text = "📅 التسجيلات القادمة\n\n🚧 قيد التطوير."

    elif query.data == "closing":
        text = "⏳ التسجيلات التي ستغلق قريبًا\n\n🚧 قيد التطوير."

    elif query.data == "sectors":
        text = (
            "🏛️ القطاعات:\n\n"
            "🎓 التعليم\n"
            "💼 التوظيف\n"
            "🏫 التعليم العالي\n"
            "🔧 التكوين المهني\n"
            "🏠 السكن\n"
            "⚖️ العدل\n"
            "🪪 الخدمات الإدارية"
        )

    elif query.data == "wilaya":
        text = "📍 البحث حسب الولاية\n\n🚧 قيد التطوير."

    else:
        text = "❌ خطأ."

    await query.edit_message_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "استعمل /start لفتح القائمة الرئيسية."
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