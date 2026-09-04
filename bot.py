import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇩🇿 مرحبًا بك في بوت ورقتي\n\n"
        "📋 هنا سنجمع التسجيلات والمسابقات والخدمات الرسمية في الجزائر.\n\n"
        "🔎 قريبًا يمكنك البحث عن:\n"
        "• مسابقات التوظيف\n"
        "• التسجيلات الجامعية\n"
        "• التكوين المهني\n"
        "• التربية\n"
        "• السكن\n"
        "• المنح\n"
        "• مختلف الخدمات الإدارية\n\n"
        "🚀 البوت قيد التطوير."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ الأوامر المتاحة حاليًا:\n\n"
        "/start - تشغيل البوت\n"
        "/help - المساعدة"
    )


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("🇩🇿 War9ati Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()