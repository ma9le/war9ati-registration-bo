import os
import logging
import requests
from bs4 import BeautifulSoup

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

EDUCATION_URL = "https://www.education.gov.dz/"


def get_education_news():
    try:
        response = requests.get(
            EDUCATION_URL,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for link in soup.find_all("a", href=True):
            title = link.get_text(" ", strip=True)
            href = link["href"]

            if not title:
                continue

            if href.startswith("/"):
                href = EDUCATION_URL.rstrip("/") + href

            if href.startswith("http"):
                results.append({
                    "title": title,
                    "url": href
                })

        return results[:10]

    except Exception as e:
        logging.error("Collector error: %s", e)
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
        "نساعدك في العثور على التسجيلات والمسابقات "
        "والخدمات الرسمية في الجزائر.\n\n"
        "اختر ما تريد:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "open":
        news = get_education_news()

        if not news:
            text = (
                "📢 التسجيلات المفتوحة\n\n"
                "⚠️ لم أتمكن حاليًا من جلب الإعلانات."
            )
        else:
            items = []

            for item in news:
                items.append(
                    f"📌 {item['title']}\n"
                    f"🔗 {item['url']}"
                )

            text = (
                "📢 آخر المنشورات من وزارة التربية الوطنية:\n\n"
                + "\n\n".join(items)
            )

    elif query.data == "upcoming":
        text = (
            "📅 التسجيلات القادمة\n\n"
            "🚧 سيتم تنظيمها تلقائيًا حسب تاريخ بداية التسجيل."
        )

    elif query.data == "closing":
        text = (
            "⏳ التي ستغلق قريبًا\n\n"
            "🚧 سيتم إضافة نظام حساب تاريخ غلق التسجيلات."
        )

    elif query.data == "sectors":
        text = (
            "🏛️ حسب القطاع\n\n"
            "🎓 التعليم\n"
            "💼 التوظيف\n"
            "🏫 التعليم العالي\n"
            "🔧 التكوين المهني\n"
            "🏠 السكن\n"
            "⚖️ العدل\n"
            "🪪 الخدمات الإدارية\n"
            "🛡️ الأمن والدفاع"
        )

    elif query.data == "wilaya":
        text = (
            "📍 حسب الولاية\n\n"
            "🚧 سيتم إضافة البحث حسب الولايات الجزائرية."
        )

    else:
        text = "❌ حدث خطأ."

    await query.edit_message_text(text)


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