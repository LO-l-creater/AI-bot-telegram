import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get('8688216650:AAEC7vFagTxI7RKojYeIILmFh4jcpDa5yXE')
OPENROUTER_API_KEY = os.environ.get('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')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    try:
        answer = response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        answer = "❌ Ошибка: OpenRouter не вернул ответ. Проверь токен или лимиты."

    await update.message.reply_text(answer)

def main():
    print("Бот запущен...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()




