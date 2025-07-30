import telebot
import random
import os
from flask import Flask
import threading

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# ------------------------------------
# کدهای رباتت (کپی شده از کد تو)
word_list = [
    'سیب', 'برگ', 'گربه', 'اسب', 'ببر', 'رود', 'دریا', 'اسبک', 'کوه', 'هرم',
    # ... (بقیه کلمات رو کامل بذار)
]

last_char = {}
used_words = {}

@bot.message_handler(commands=['wordgame'])
def start_word_chain(message):
    chat_id = message.chat.id
    last_char[chat_id] = 'س'
    used_words[chat_id] = set()
    bot.send_message(chat_id, "بازی کلمه بعدی شروع شد! کلمه باید با حرف 'س' شروع بشه.")

@bot.message_handler(func=lambda message: message.chat.id in last_char)
def word_chain_game(message):
    chat_id = message.chat.id
    text = message.text.strip()
    if chat_id not in last_char:
        return

    expected_char = last_char[chat_id]
    if not text or text[0] != expected_char:
        bot.reply_to(message, f"کلمه‌ات باید با حرف '{expected_char}' شروع بشه.")
        return

    if text in used_words[chat_id]:
        bot.reply_to(message, f"این کلمه قبلاً استفاده شده! تو باختی.")
        last_char.pop(chat_id)
        used_words.pop(chat_id)
        return

    used_words[chat_id].add(text)
    last_letter = text[-1]
    possible_words = [w for w in word_list if w[0] == last_letter and w not in used_words[chat_id]]

    if not possible_words:
        bot.reply_to(message, "دیگه کلمه‌ای ندارم، تو برنده‌ای!")
        last_char.pop(chat_id)
        used_words.pop(chat_id)
        return

    bot_word = random.choice(possible_words)
    bot.reply_to(message, bot_word)
    used_words[chat_id].add(bot_word)
    last_char[chat_id] = bot_word[-1]

# بازی حدس عدد
games = {}

@bot.message_handler(commands=['numbergame'])
def start_guess(message):
    chat_id = message.chat.id
    number = random.randint(1, 100)
    games[chat_id] = number
    bot.send_message(chat_id, "بیناموس بین 1تا 100 عدد بگو!")

@bot.message_handler(func=lambda message: message.chat.id in games)
def guess_number(message):
    chat_id = message.chat.id
    try:
        guess = int(message.text)
    except ValueError:
        bot.reply_to(message, "کص کش فقط عدد")
        return

    number = games[chat_id]
    if guess < number:
        bot.reply_to(message, "اون کیری از این بزرگ تره!")
    elif guess > number:
        bot.reply_to(message, "اون کیری از این کوچیک تره!")
    else:
        bot.reply_to(message, "خایتم درست گفتی.")
        del games[chat_id]

# ارسال جوک
jokes = [
    "می‌دونی چرا پرستوها پرواز می‌کنن؟ چون اگه پیاده برن خسته می‌شن.",
    تو جاده تصادف میشه \n زنه از فضولی میگه برین کنار من زنشم
    میره میبینه ی خره افتاده زمین,
]

@bot.message_handler(func=lambda message: message.text.strip().lower() == 'جوک')
def send_joke(message):
    joke = random.choice(jokes)
    bot.reply_to(message, joke)

# سایر دستورات شما مثل سکوت، پین، جواب سلام و ممنون و غیره
# اینجا به خاطر کوتاهی نمی‌ذارم، خودت اضافه کن طبق کد اولیه

# Flask route برای پینگ و سلامت ربات
@app.route("/")
def home():
    return "Bot is alive!", 200

def run():
    app.run(host="0.0.0.0", port=10000)

if __name__ == '__main__':
    # وب‌سرور Flask رو توی ترد جدا ران کن
    threading.Thread(target=run).start()
    # ربات رو اجرا کن
    bot.infinity_polling()
