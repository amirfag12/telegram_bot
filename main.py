import telebot
import sqlite3
import random

TOKEN = '7965728090:AAFoH7ZW3xf0MHCc5UzFvJAj3tOyM18xzsQ'
bot = telebot.TeleBot(TOKEN)

# ایجاد اتصال به دیتابیس و ساخت جدول گروه‌ها (اگر وجود نداشته باشد)
conn = sqlite3.connect('groups.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS groups (
    chat_id INTEGER PRIMARY KEY,
    title TEXT,
    username TEXT
)
''')
conn.commit()

# لیست کلمات بازی آخرین حرف
word_list = [
    'سیب', 'برگ', 'گربه', 'اسب', 'ببر', 'رود', 'دریا', 'اسبک', 'کوه', 'هرم',
    'مرد', 'دست', 'تخت', 'طرح', 'حلزون', 'نقشه', 'هوا', 'باغ', 'گل', 'لبخند',
    'دانه', 'زمین', 'نارنج', 'جنگل', 'لباس', 'سیاره', 'رنگ', 'گوش', 'شیر', 'ریشه',
    'هشت', 'تار', 'رودخانه', 'نقاشی', 'یار', 'رئیس', 'ساعت', 'تلویزیون', 'نارگیل', 'لب',
    'برف', 'فنجان', 'نقاب', 'بام', 'مرداب', 'باد', 'دریچه', 'همسایه', 'انگور', 'رام',
    'ماه', 'هواپیما', 'اندازه', 'زمستان', 'نسیم', 'میز', 'زنبور', 'رستوران', 'نان', 'نمک',
    'کبریت', 'تلفن', 'نقش', 'حیوان', 'نور', 'دل', 'باران', 'نام', 'موز', 'زمان',
    'نماد', 'دما', 'آسمان', 'هسته', 'سنگ', 'گنج', 'جاده', 'دریاچه', 'هرمز', 'زرد',
    'دفتر', 'رنگین', 'نانوا', 'تمرین', 'کوهستان', 'تنها', 'باد', 'یاد', 'دلبر', 'روز',
    'زمزمه', 'انار', 'راز', 'پری', 'بادبادک', 'سیمرغ', 'خرس', 'کلاغ', 'موش', 'شیرینی',
    'گلستان', 'آهو', 'بنفشه', 'پیام', 'ستاره', 'خورشید', 'ماهیان', 'دریاچه', 'کاغذ', 'آتش',
    'باغچه', 'کوهسار', 'فیل', 'گلدان', 'دشت', 'تندر', 'نسیم', 'باران', 'قناری', 'مرغ',
    'سوسک', 'شانه', 'آینه', 'پنجره', 'میزان', 'قفل', 'برفک', 'کفش', 'چتر', 'مروارید',
    'عقاب', 'زنبق', 'شمع', 'پیانو', 'کلید', 'پنبه', 'صخره', 'دانه', 'جنگل', 'تپه',
    'قندیل', 'ساحل', 'شکوفه', 'بندر', 'نیلوفر', 'خروس', 'گلدوزی', 'موج', 'باران', 'شعله',
    'سوزن', 'قیچی', 'کبوتر', 'کوهستان', 'نقاشی', 'بیشه', 'رودخانه', 'چشمه', 'گلبرگ', 'بلوط',
    'سایه', 'میدان', 'نخل', 'درخت', 'خاک', 'چراغ', 'ماه', 'خورشید', 'ستاره', 'ابر',
    'باد', 'رعد', 'برق', 'دشت', 'توفان', 'ساحل', 'جزیره', 'دریا', 'کوه', 'رود',
    'دریاچه',
]

# ذخیره وضعیت بازی کلمات و کلمات استفاده شده برای هر چت
last_char = {}
used_words = {}

# ذخیره عدد بازی حدس عدد برای هر چت
games = {}

# لیست جوک‌ها
jokes = [
    "می‌دونی چرا پرستوها پرواز می‌کنن؟ چون اگه پیاده برن خسته می‌شن.",
    "می‌دونی چرا سر نمکدون سوراخ داره؟ برا که نمکا خفه نشن.",
    "می‌دونی چرا ماهی‌ها دست نمیدن؟ چون دستاشون خیسه.",
    "می‌دونی اگه یه فیل بره بالا درخت چی میشه؟ یه فیل از رو زمین کم میشه.",
    "می‌دونی وقتی ماهی‌ها غذا می‌خورن چی میشه؟ سفره ماهی میاد جمع می‌کنه.",
    "می‌دونی اگه دوتا تیر آهن دعواشون بشه چی میشه؟ میرن پیش پیراهن تا مشکلشون حل بشه.",
    "می‌دونی وقتی یه فلش تعجب می‌کنه چی می‌گه؟ می‌گه واای حجمااام.",
    "می‌دونی اگه تو کاسه مسی غذا بخوری چی میشه؟ مسی ناراحت میشه.",
    "می‌دونی اگه حیوانات نادر رو شکار کنیم چی میشه؟ نادر ناراحت میشه.",
    "می‌دونین مریخیا به سیب‌زمینی چی می‌گن؟ سیب مریخی.",
    "می‌دونی اگر دوتا فیل برن رو درخت چی میشه؟ درخت می‌شکنه.",
    "می‌دونید اگه گوگل بمیره به بچه‌هاش چی می‌رسه؟ گوگل ارث.",
    "می‌دونی اگه یه جادوگری که سوار جاروش شده و داره یه مسیری رو طی می‌کنه، خسته شه چی کار می‌کنه؟ از جاروش پیاده می‌شه، سوار طی می‌شه و یه مسیری رو جارو می‌کنه.",
    "یه روز یه مرد رفت باغ وحش و دید زرافه داره فوتبال بازی می‌کنه!",
    "اگر پول توی باغچه رشد می‌کرد، همه کشاورز می‌شدن!",
    "چرا دانشجوها همیشه دیر می‌رسن؟ چون کلاس آخرشونه!",
    "یه مرغ اومد تو کلاس ریاضی، استاد گفت: چرا دیر اومدی؟ مرغ گفت: گیر کردم تو تخم مرغ!",
    "چرا قورباغه همیشه خوشحاله؟ چون هیچ وقت کار نمی‌کنه!",
    "یه روز یه بچه به باباش گفت: بابا من یه سوپر قهرمانم، بابا گفت: خوب، بشین سر کارت!",
    "چرا ماهی همیشه خیسه؟ چون تو آب زندگی می‌کنه!",
    "می‌دونید چرا هویج نارنجیه؟ چون بهش میاد.",
    "می‌دونید چرا ماشین آردی را نمی‌شورن؟ چون بهشون آب بخوره خمیر می‌شن.",
    "می‌دونید اگه زن فاضل گلوش گیر کنه چی می‌گه؟ می‌گه فاضلاب.",
    "می‌دونید چرا الکترون‌ها سوار چرخ و فلک نمیشن؟ چون باردارن براشون خوب نیست.",
    "می‌دونید چرا یخچال برف داره؟ چون آنتن نداره.",
    "می‌دونی چرا اسکلت از ساختمان نمی‌پره پایین؟ چون جیگر نداره.",
    "می‌دوني چرا لاک‌پشت‌ها نماز نمی‌خونن؟ چون لاک دارن.",
    "می‌دوني چرا پنگوئن‌ها سواد ندارن؟ چون همیشه برف میاد، مدارسشون تعطیله!",
    "می‌دوني چرا فیل‌ها از سربازی معافند؟ چون کف پاشون صافه.",
    "یه روز یه مگس مریض می‌شه، مامانش واسش اسهال درست می‌کنه.",
    "یه روز یه سیره با یه پیتزاهه دعواش میشه میگه حیف سیرم وگرنه میخوردمت.",
    "می‌دوني وقتی سیگارا خوشحال می‌شن چی می‌شه؟ توتونشون عروسی می‌شه.",
    "یه روز یکی خودشو می‌مالوند به سپر ماشین، بهش گفتن چیکار می‌کنی؟ گفت دارم روزمو سپری می‌کنم.",
    "یه روز قلی میره بالای درخت چنار، بهش میگن داری چی کار می‌کنی؟ میگه دارم توت می‌خورم. میگن اینکه درخت چناره، میگه توت تو جیبمه.",
    "می‌دوني اگه ماکارونی‌ها قاطی پاطی بخورن چی میشه؟ نودل میکنن!",
    "می‌دوني کتری‌های سرباز وقتی فرماندشون صداشون میکنه چی میگن؟ میگن بله به جوشم!",
    "می‌دوني میوه‌ها موقع تولد به همدیگه چی کادو میدن؟ آواکادو!",
    "می‌دوني ماهی‌ها وقتی باهم دعواشون میشه کجا میرن؟ میرن جاجرود!",
    "می‌دوني اگه سوسیسو بزاری رو آتیش چی میشه؟ می‌سوسه!"
]

# --- ذخیره گروه‌ها در دیتابیس وقتی ربات به گروه اضافه می‌شود ---
@bot.my_chat_member_handler()
def handle_my_chat_member(message):
    chat = message.chat
    new_status = message.new_chat_member.status

    if new_status in ['member', 'administrator']:
        chat_id = chat.id
        title = getattr(chat, 'title', None)
        username = getattr(chat, 'username', None)

        cursor.execute('INSERT OR IGNORE INTO groups (chat_id, title, username) VALUES (?, ?, ?)',
                       (chat_id, title, username))
        conn.commit()
        print(f"ربات به گروه '{title}' با شناسه {chat_id} اضافه شد.")

# --- دستور نمایش گروه‌های ذخیره شده ---
@bot.message_handler(commands=['showgroups'])
def show_groups(message):
    cursor.execute('SELECT chat_id, title, username FROM groups')
    groups = cursor.fetchall()

    if not groups:
        bot.reply_to(message, 'هیچ گروهی ذخیره نشده.')
        return

    text = "لیست گروه‌های ذخیره‌شده:\n\n"
    for chat_id, title, username in groups:
        if username:
            link = f"https://t.me/{username}"
        else:
            link = 'لینک موجود نیست'
        text += f"نام: {title or 'نامشخص'}\nآیدی: {chat_id}\nلینک: {link}\n\n"

    bot.reply_to(message, text)

# --- شروع بازی آخرین حرف ---
@bot.message_handler(commands=['wordgame'])
def start_wordgame(message):
    chat_id = message.chat.id
    last_char[chat_id] = None
    used_words[chat_id] = set()
    bot.send_message(chat_id, "بازی آخرین حرف شروع شد! شما اول شروع کنید. لطفا یک کلمه بفرستید.")

# --- پاسخ به کلمات بازی آخرین حرف ---
@bot.message_handler(func=lambda m: m.chat.id in last_char)
def play_wordgame(message):
    chat_id = message.chat.id
    user_word = message.text.strip()

    # چک کردن اگر کاربر اولین کلمه را فرستاده
    if last_char[chat_id] is None:
        if user_word not in word_list:
            bot.reply_to(message, "این کلمه در لیست ما نیست. لطفا یک کلمه معتبر بفرستید.")
            return
        last_char[chat_id] = user_word[-1]
        used_words[chat_id].add(user_word)
        bot.reply_to(message, f"کلمه ثبت شد. نوبت من...")

        # ربات کلمه‌ای پیدا می‌کند که با حرف آخر کلمه شما شروع شود و استفاده نشده باشد
        bot_word = None
        for w in word_list:
            if w[0] == last_char[chat_id] and w not in used_words[chat_id]:
                bot_word = w
                break

        if bot_word:
            used_words[chat_id].add(bot_word)
            last_char[chat_id] = bot_word[-1]
            bot.send_message(chat_id, f"{bot_word}\nنوبت شما، کلمه با حرف '{last_char[chat_id]}'")
        else:
            bot.send_message(chat_id, "من دیگه کلمه‌ای پیدا نکردم! شما برنده‌اید! 🎉")
            # بازی تمام شد
            del last_char[chat_id]
            del used_words[chat_id]
    else:
        # چک کردن شروع حرف
        if user_word[0] != last_char[chat_id]:
            bot.reply_to(message, f"کلمه باید با حرف '{last_char[chat_id]}' شروع شود.")
            return
        if user_word in used_words[chat_id]:
            bot.reply_to(message, "این کلمه قبلا استفاده شده است.")
            return
        if user_word not in word_list:
            bot.reply_to(message, "این کلمه در لیست ما نیست.")
            return

        used_words[chat_id].add(user_word)
        last_char[chat_id] = user_word[-1]
        bot.reply_to(message, "کلمه ثبت شد. نوبت من...")

        bot_word = None
        for w in word_list:
            if w[0] == last_char[chat_id] and w not in used_words[chat_id]:
                bot_word = w
                break

        if bot_word:
            used_words[chat_id].add(bot_word)
            last_char[chat_id] = bot_word[-1]
            bot.send_message(chat_id, f"{bot_word}\nنوبت شما، کلمه با حرف '{last_char[chat_id]}'")
        else:
            bot.send_message(chat_id, "من دیگه کلمه‌ای پیدا نکردم! شما برنده‌اید! 🎉")
            del last_char[chat_id]
            del used_words[chat_id]

# --- شروع بازی حدس عدد ---
@bot.message_handler(commands=['guess'])
def start_guess(message):
    chat_id = message.chat.id
    number = random.randint(1, 100)
    games[chat_id] = number
    bot.send_message(chat_id, "بازی حدس عدد شروع شد! من عددی بین 1 تا 100 انتخاب کردم. حدس بزنید.")

# --- حدس زدن عدد ---
@bot.message_handler(func=lambda m: m.chat.id in games)
def guess_number(message):
    chat_id = message.chat.id
    try:
        guess = int(message.text.strip())
    except ValueError:
        bot.reply_to(message, "لطفا یک عدد وارد کنید.")
        return

    number = games[chat_id]

    if guess == number:
        bot.send_message(chat_id, f"تبریک! عدد درست {number} بود. بازی تمام شد.")
        del games[chat_id]
    elif guess < number:
        bot.send_message(chat_id, "عدد بزرگتره، دوباره حدس بزنید.")
    else:
        bot.send_message(chat_id, "عدد کوچکتره، دوباره حدس بزنید.")

# --- ارسال جوک ---
@bot.message_handler(commands=['joke'])
def send_joke(message):
    joke = random.choice(jokes)
    bot.send_message(message.chat.id, joke)

# --- شروع ربات ---
print("ربات شروع به کار کرد.")
bot.infinity_polling()
