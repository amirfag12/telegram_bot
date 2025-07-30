import telebot
import sqlite3
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import random
import os
from flask import Flask
import threading
import telebot
import os


app = Flask(__name__)
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@app.route("/")
def home():
    return "Bot is alive!", 200

def run():
    app.run(host="0.0.0.0", port=10000)

# این یک ترد جدا برای وب‌سرور می‌سازه
threading.Thread(target=run).start()

# ------------------------------------
# ادمین ربات
#بازی اخرین حرف
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

# ذخیره آخرین حرف برای هر چت
last_char = {}
# ذخیره کلمات استفاده شده برای هر چت (set برای سرعت جستجو)
used_words = {}

@bot.message_handler(commands=['wordgame'])
def start_word_chain(message):
    chat_id = message.chat.id
    last_char[chat_id] = 'س'  # مثلا بازی رو با حرف 'س' شروع کن
    used_words[chat_id] = set()  # ریست کردن کلمات استفاده شده
    bot.send_message(chat_id, "بازی کلمه بعدی شروع شد! کلمه باید با حرف 'س' شروع بشه.")

@bot.message_handler(func=lambda message: message.chat.id in last_char)
def word_chain_game(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in last_char:
        return  # بازی شروع نشده

    # چک شروع کلمه با حرف مورد انتظار
    expected_char = last_char[chat_id]
    if not text or text[0] != expected_char:
        bot.reply_to(message, f"کلمه‌ات باید با حرف '{expected_char}' شروع بشه.")
        return

    # چک کلمه استفاده شده
    if text in used_words[chat_id]:
        bot.reply_to(message, f"این کلمه قبلاً استفاده شده! تو باختی.")
        # تموم کردن بازی
        last_char.pop(chat_id)
        used_words.pop(chat_id)
        return

    # ثبت کلمه جدید
    used_words[chat_id].add(text)

    # ربات جواب میده
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

    # بروزرسانی حرف مورد انتظار
    last_char[chat_id] = bot_word[-1]

#بازی حدس عدد

# دیکشنری برای ذخیره عدد هر چت (هر چت جداگانه بازی خودش رو داره)
games = {}

@bot.message_handler(commands=['numbergame'])
def start_guess(message):
    chat_id = message.chat.id
    number = random.randint(1, 100)  # عدد تصادفی از 1 تا 100
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
        del games[chat_id]  # پایان بازی، حذف عدد ذخیره شده

# ارسال جوک
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
    "می‌دونی چرا لاک‌پشت‌ها نماز نمی‌خونن؟ چون لاک دارن.",
    "می‌دونی چرا پنگوئن‌ها سواد ندارن؟ چون همیشه برف میاد، مدارسشون تعطیله!",
    "می‌دونی چرا فیل‌ها از سربازی معافند؟ چون کف پاشون صافه.",
    "یه روز یه مگس مریض می‌شه، مامانش واسش اسهال درست می‌کنه.",
    "یه روز یه سیره با یه پیتزاهه دعواش میشه میگه حیف سیرم وگرنه میخوردمت.",
    "می‌دونی وقتی سیگارا خوشحال می‌شن چی می‌شه؟ توتونشون عروسی میشه.",
    "یه روز یکی خودشو می‌مالوند به سپر ماشین، بهش گفتن چیکار می‌کنی؟ گفت دارم روزمو سپری می‌کنم.",
    "یه روز قلی میره بالای درخت چنار، بهش میگن داری چی کار می‌کنی؟ میگه دارم توت می‌خورم. میگن اینکه درخت چناره، میگه توت تو جیبمه.",
    "می‌دونی اگه ماکارونی‌ها قاطی پاطی بخورن چی میشه؟ نودل میکنن!",
    "می‌دوني کتری‌های سرباز وقتی فرماندشون صداشون میکنه چی میگن؟ میگن بله به جوشم!",
    "می‌دوني میوه‌ها موقع تولد به همدیگه چی کادو میدن؟ آواکادو!",
    "می‌دوني ماهی‌ها وقتی باهم دعواشون میشه کجا میرن؟ میرن جاجرود!",
    "می‌دوني اگه سوسیسو بزاری رو آتیش چی میشه؟ می‌سوسه!"
]



@bot.message_handler(func=lambda message: message.text.strip().lower() == 'جوک')
def send_joke(message):
    joke = random.choice(jokes)
    bot.reply_to(message, joke)


# ترجمه
# translator = Translator()


# @bot.message_handler(func=lambda message: message.text == 'ترجمه')
# def translate_reply(message):
#     # بررسی می‌کنیم که پیام ریپلای باشه
#     if message.reply_to_message and message.reply_to_message.text:
#         original_text = message.reply_to_message.text

#         # تشخیص زبان متن
#         detected = translator.detect(original_text)
#         user_lang = detected.lang

#         # اگر زبان پیام فارسی نیست، ترجمه کن به فارسی
#         if user_lang != 'fa':
#             translated = translator.translate(original_text, dest='fa')
#             reply_text = f"بیا خارکصه اینم ترجمت:\n{translated.text}"
#             bot.reply_to(message.reply_to_message, reply_text)

#         # اگر زبان فارسی بود، ترجمه کن به انگلیسی (اختیاری)
#         else:
#             translated = translator.translate(original_text, dest='en')
#             reply_text = f"Translation to English:\n{translated.text}"
#             bot.reply_to(message.reply_to_message, reply_text)
#     else:
#         bot.reply_to(message, 'لطفاً روی پیامی ریپلای کنید که می‌خواهید ترجمه شود.')


# سکوت و آن سکوت
@bot.message_handler(func=lambda message: message.text == 'سکوت')
def mute_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if is_user_admin(chat_id, user_id):
        if message.reply_to_message:
            target_user_id = message.reply_to_message.from_user.id
            bot.restrict_chat_member(chat_id, target_user_id, can_send_messages=False)
            bot.restrict_chat_member(
                chat_id,
                target_user_id,
                can_send_messages=False,  # نمی‌تونه پیام متنی بفرسته
                can_send_media_messages=False,  # نمی‌تونه عکس و ویدیو بفرسته
                can_send_other_messages=False,  # می‌تونه سایر پیام‌ها (مثل استیکر و نظرسنجی) رو بفرسته
                can_add_web_page_previews=False  # می‌تونه پیش‌نمایش لینک‌ها رو اضافه کنه
                # سایر دسترسی‌ها رو تغییر نده (مثل دعوت اعضا، تغییر اطلاعات گروه و غیره)
            )

            bot.reply_to(message.reply_to_message, 'انقدر زر نزن بی شعور')
        else:
            bot.reply_to(message, "ریپلای نکردی اسگل")
    else:
        bot.reply_to(message, 'ادمین نیسی کونی')


@bot.message_handler(func=lambda message: message.text == 'سیکوت')
def unmute_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if is_user_admin(chat_id, user_id):
        if message.reply_to_message:
            target_user_id = message.reply_to_message.from_user.id
            bot.restrict_chat_member(chat_id, target_user_id, can_send_messages=True)
            bot.restrict_chat_member(
                chat_id,
                target_user_id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )

            bot.reply_to(message.reply_to_message, 'از سکوت در اوردمت زیاد زر بزنی سکوت میکنم دوریاره')
        else:
            bot.reply_to(message, 'باز ریپلای نزدی که کصکش')
    else:
        bot.reply_to(message, "انقد کص نگو ادمین نیسی")


# جواب به پیاما
@bot.message_handler(func=lambda message: message.text == 'ممنون')
def thankyou(message):
    bot.reply_to(message, 'خواهش میکنم کص کش')


@bot.message_handler(func=lambda message: message.text == 'سلام')
def hi(message):
    bot.reply_to(message, 'سلام جاکش')


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        welcome_text = f' @{message.from_user.username} خوش اومدی کص کش!'
        bot.send_message(message.chat.id, text=welcome_text)


def is_user_admin(chat_id, user_id):
    admins = bot.get_chat_administrators(chat_id)
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False


# -----------
# پین کردن پیام
@bot.message_handler(func=lambda message: message.text == 'پین')
def pin_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if is_user_admin(chat_id, user_id):
        if message.reply_to_message:
            bot.pin_chat_message(chat_id, message.reply_to_message.message_id)
            bot.reply_to(message, 'پین شد کص کش')
        else:
            bot.reply_to(message, 'کص کش ریپلای کن رو پیام')

    else:
        bot.send_message(message, 'ادمین نیستم کصکش')


@bot.message_handler(func=lambda message: message.text == 'بردار')
def unpin_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if is_user_admin(chat_id, user_id):
        bot.unpin_chat_message(chat_id)
        bot.reply_to(message, 'برداشتم کص کش')
    else:
        bot.send_message(message.chat.id, 'ادمین نیستم کمکم کن')


# ------------------------------
# # ADMIN_ID = 985386314 # شناسه ادمین رو اینجا بزار
# # ساخت جدول دیتابیس
# def init_db():
#     with sqlite3.connect('users.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id INTEGER UNIQUE,
#                 firstname TEXT,
#                 lastname TEXT,
#                 phone_number TEXT
#             )
#         """)
#         conn.commit()
#
# init_db()
#
# # دکمه درخواست شماره تماس
# contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# contact_button = KeyboardButton('ارسال شماره تماس', request_contact=True)
# contact_keyboard.add(contact_button)
#
# user_data = {}
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, 'سلام! لطفاً شماره تماس خود را ارسال کن.', reply_markup=contact_keyboard)
#
# @bot.message_handler(content_types=['contact'])
# def handle_contact(message):
#     contact = message.contact
#     user_id = message.from_user.id
#     phone = contact.phone_number
#     user_data[user_id] = {'phone_number': phone}
#
#     bot.send_message(message.chat.id, 'شماره تماس دریافت شد. لطفاً نام خود را وارد کنید:')
#     bot.register_next_step_handler(message, get_firstname)
#
# def get_firstname(message):
#     user_id = message.from_user.id
#     user_data[user_id]['firstname'] = message.text
#     bot.send_message(message.chat.id, 'لطفاً نام خانوادگی خود را وارد کنید:')
#     bot.register_next_step_handler(message, get_lastname)
#
# def get_lastname(message):
#     user_id = message.from_user.id
#     user_data[user_id]['lastname'] = message.text
#
#     # ذخیره در دیتابیس
#     data = user_data[user_id]
#     with sqlite3.connect('users.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("""
#                 INSERT OR REPLACE INTO users (user_id, firstname, lastname, phone_number)
#                 VALUES (?, ?, ?, ?)
#             """, (user_id, data['firstname'], data['lastname'], data['phone_number']))
#             conn.commit()
#             bot.send_message(message.chat.id, 'اطلاعات شما با موفقیت ذخیره شد. ممنون!')
#         except Exception as e:
#             bot.send_message(message.chat.id, 'مشکلی پیش آمد، دوباره تلاش کنید.')
#             print('DB ERROR:', e)
#
# @bot.message_handler(commands=['list'])
# def show_list(message):
#     if message.from_user.id != ADMIN_ID:
#         bot.send_message(message.chat.id, 'شما دسترسی به این بخش را ندارید ❌')
#         return
#
#     with sqlite3.connect('users.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT id,firstname, lastname, phone_number FROM users")
#         rows = cursor.fetchall()
#
#     if not rows:
#         bot.send_message(message.chat.id, 'هیچ کاربری ثبت نشده است.')
#         return
#
#     text = "لیست کاربران ثبت شده:\n\n"
#     for row in rows:
#         text += f"ID: {row[0]}\nنام: {row[1]}\nنام خانوادگی: {row[2]}\nشماره تماس: {row[3]}\n\n"
#
#     bot.send_message(message.chat.id, text)
#
# bot.polling()
# -----------------------------
# تمزین ترکیبی
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# button=KeyboardButton('send your contact',request_contact=True)
# keyboard.add(button)
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.reply_to(message,'welcome the new bot')
#

# --------------------
# تمریت دیتا بیس
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
# Button = KeyboardButton('send your number :', request_contact=True)
# keyboard.add(Button)
# with sqlite3.connect('user1.db') as conn:
#     cursor = conn.cursor()
#     create_table_query = """
#         create table if not exists ueser1 (
#         Id INTEGER PRIMARY KEY,
#         firstname text,
#         lastname text,
#         phone_number text
#         );
#     """
#
#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, 'Welcome !', reply_markup=keyboard)
#
#
# @bot.message_handler(content_types=['contact'])
# def send_contact(message):
#     with sqlite3.connect('user1.db') as conn:
#         cursor = conn.cursor()
#         inser_data_query = """
#         insert into users (ID,firstname,lastname,phone_number)
#         values (?,?,?,?)
#         """
#         data = (message.contact.user_id,message.contact.first_name, message.contact.last_name, message.contact.phone_number)
#         cursor.execute(inser_data_query, data)
#

# bot.reply_to(message.chat.id, f'{message.contact})


# -----------------------------------------
# # درست کردن کیبورد
# keyboard = ReplyKeyboardMarkup (resize_keyboard=True,row_width=1)
# Button = KeyboardButton(text='send your phone number',request_contact=True)
# keyboard.add(Button)
# # ساختن دیتا بیس
# with sqlite3.connect('user.db') as connection:
#      cursor = connection.cursor()
#      create_table_query="""
#         CREATE TABLE IF NOT EXISTS users(
#         ID primary key ,
#         first_name TEXT,
#         last_name TEXT,
#         phone_number TEXT
#      );
#      """
#      cursor.execute(create_table_query)
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id,text="welcome amir bot",reply_markup=keyboard)
#
# @bot.message_handler(content_types=['contact'])
# def contact(message):
# #    bot.send_message(message.chat.id,text=f'{message.contact} ')
#     with sqlite3.connect('user.db') as connection:
#         cursor = connection.cursor()
#         insert_data_query="""
#             Insert INTO users (ID,first_name,last_name,phone_number)
#             VALUES (? ,? ,? ,? )
#         """
#         data = (message.contact.user_id,message.contact.first_name,message.contact.last_name,message.contact.phone_number)
#         cursor.execute(insert_data_query,data)
#
# bot.polling()
# ----------------------------------------------
# ااضافه کردن کویری به دیتا بیس
# connection=sqlite3.connect('user.db')
# cursor=connection.cursor()
# create_table_query = """
#     CREATE TABLE IF NOT EXISTS users(
#         ID integer primary key ,
#         firstname TEXT ,
#         lastname TEXT ,
#         phone_number TEXT
# );
# """
# cursor.execute(create_table_query)
# connection.commit()
# connection.close()
#
# sample_data_query= """
#     INSERT INTO users(id,firstname,lastname,phone_number)
#     VALUES (?, ?, ?, ?)
# """
# sample_data=[(89789,'John','Smith','555555555'),
#              (879,'amir','fag','09190601238'),
#              (78978,'mimi','sda','48784851515')
#              ]
# # with sqlite3.connect('user.db') as connection:
# #     cursor = connection.cursor()
# #     cursor.executemany(sample_data_query,sample_data)
# fetch_data_query = """
# SELECT id,firstname,lastname,phone_number FROM users
# """
# rows = []
# with sqlite3.connect('user.db') as connection:
#     cursor = connection.cursor()
#     cursor.execute(fetch_data_query)
#     rows = cursor.fetchall()
# for row in rows:
#     print(
#         f'id{row[0]}fn{row[1]}ln{row[2]}ph{row[3]}'
#       )

# ----------------------------------------
# تمرین درست کردن دیتا بیس
# connecting=sqlite3.connect('user1.db')
# cursor=connecting.cursor()
# create_table_query="""
#
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY ,
#         firstname TEXT ,
#         lastname TEXT ,
#         phone_number TEXT
#     );
# """
# cursor.execute(create_table_query)
# connecting.commit()
# connecting.close()
# ----------------------------------------
# ------------------------------------
# تمرین دکمه ها
# lowerbutton = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
# lowerbutton.add(*['game', 'movie', 'music'])
#
# bot.message_handler(commands=['start'])
# ef send_welcome(message):
#    bot.reply_to(message, 'لطفاً علاقه خود را انتخاب کنید:', reply_markup=flowerbutton)
#
# bot.message_handler(func=lambda message: True)
# ef echo_all(message):
#    if message.text == 'game':
#        bot.reply_to(message,'your choise a game')
#    elif message.text == 'movie':
#        bot.reply_to(message,'your choise a movie')
#    elif message.text == 'music':
#        bot.reply_to(message,'your choise a music')
#    else:
#        bot.reply_to(message,'ypur choise is wrong!')
# ---------------------------------------------------
#     آموزش دکمه
# renamekeyboard=ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
# renamekeyboard.add('button1','button2')
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message,'check the button!',reply_markup=renamekeyboard)
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     if message.text == 'button1':
#         bot.reply_to(message,'button 1 is working')
#     elif message.text == 'button2':
#         bot.reply_to(message,'button 2 is working')
#     else:
#         bot.reply_to(message,'buttons is not working')
# reply_keyboard = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
# reply_keyboard.add('button1','button2')
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, 'check the button!',reply_markup=reply_keyboard)
#
# @bot.message_handler(func=lambda message:True)
# def check_message(message):
#     if message.text == 'button1':
#         bot.reply_to(message, 'button1 works!')
#     elif message.text == 'button2':
#         bot.reply_to(message, 'button2 works!')
#     else:
#         bot.reply_to(message,f'didnt work: {message.text}')

# # اضافه کردن دکمه به بات
# from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
# button1 = InlineKeyboardButton(text='button1', callback_data='btn1')
# button2 = InlineKeyboardButton(text='button2', callback_data='btn2')
# button3 = InlineKeyboardButton(text='button3', callback_data='btn3')
# inline_keyboards=InlineKeyboardMarkup(row_width=1)
# inline_keyboards.add(button1, button2,button3)
#
#
# @bot.message_handler(commands=['start'])
# def wlcome(message):
#         bot.send_message(message.chat.id,'welcome to Amirfag',reply_markup=inline_keyboards)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def check_button(call):
#     if call.data == 'btn1':
#         bot.answer_callback_query(call.id,'btn 1 work',show_alert=True)
#     elif call.data == 'btn2':
#         bot.answer_callback_query(call.id,'btn 2 work')
#     elif call.data == 'btn3':
#         bot.answer_callback_query(call.id,'Btn3 is clicked. Great choice!',show_alert=True)
# تمرین روز جمعه
# ------------------------------
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, "enter your name?")
#     bot.register_next_step_handler(message,nametest)
# def nametest(message):
#     user_data[message.chat.id]={}
#     user_data[message.chat.id]['name']=message.text
#     bot.send_message(message.chat.id, f"hello your name is {message.text}\n enter your age?")
#     bot.register_next_step_handler(message, get_age)
# def get_age(message):
#        user_data[message.chat.id]={}
#        user_data[message.chat.id]['age']=message.text
#        bot.send_message(message.chat.id, "now send your documnet:")
#
# @bot.message_handler(content_types=['document'])
# def document(message):
#     user_data[message.chat.id]['document']=message.document.file_name
#     data=user_data[message.chat.id]
#     bot.send_document(message.chat.id, f'your name is {data[nametest]}\n your age is {data[get_age]}\n your document is {message.document.file_name}')
# #---------------------------------------------------------
# # فرستادن عکس به کاربر
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     photo_url = "https://news-cdn.varzesh3.com/pictures/2025/07/17/B/2uyu2qi29.webp?w=350"
#     bot.send_photo(
#         chat_id=message.chat.id,
#         photo=photo_url,
#         caption="سلام! خوش اومدی 😊",
#         reply_to_message_id=message.message_id  # ریپلای به پیام کاربر
#     )
#
# # اجرای ربات
# #----------------------------------------------------------


# user_data= []
# @bot.message_handler(commands=['start'])
# def ask_name(message):
#     bot.send_message(message.chat.id,'اسمتو بگو')
#     bot.register_next_step_handler(message,askphone)
# def askphone(message):
#     user_data[message.chat.id] = {"name": message.text}
#     bot.send_message(message.chat.id,"شماره خودتو بزن")
#     bot.register_next_step_handler(message,askemail)
# def askemail(message):
#     user_data[message.chat.id]['phone'] = message.text
#     bot.send_message(message.chat.id,"ایمیل خودتو بزن")
#     bot.register_next_step_handler(message,finish_signeup)
# def finish_signeup(message):
#     user_data[message.chat.id]['email'] = message.text
#     bot.send_message(message.chat.id,"اطلاعات شما با موفقیت ذخیره شد")
# @bot.message_handler(commands=['list'])
# def show_user_list(message, ADMIN_ID=985386314):
#     if message.chat.id != ADMIN_ID:
#         bot.send_message(message.chat.id, "شما دسترسی به این دستور ندارید ❌")
#         return
#
#     for uid, info in user_data.items():
#         text = f"ID: {uid}\nName: {info['name']}\nPhone: {info['phone']}\nEmail: {info['email']}"
#         bot.send_message(message.chat.id, text)


# -------------------------------------------------------------------
# @bot.message_handler(commands=["list"])
# def show_user_list(message):
#     if message.chat.id !=
# def welcome(message):
#      bot.send_message(message.chat.id,"welcome to my bot")
#      if message.chat.id not in user_ID:
#             user_ID.append(message.chat.id)
#
# @bot.message_handler(commands=['A856'])
# def send_update(message):
#     for id in user_ID:
#         bot.send_message(id,"avalible")


# تمرین جلسه 5 اسم گرفتن . سن گرفتن از کاربر و نمایش آن
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id,f"hello\t please enter your name")
#     bot.register_next_step_handler(message, namepro)
#
# def namepro(message):
#         global message_name
#         message_name = message.text
#         bot.send_message(message.chat.id,f"welcome to {message_name}\t please enter your age")
#         bot.register_next_step_handler(message,agepro)
# def agepro(message):
#         age = message.text
#         bot.reply_to(message,f" your  name is {message_name}\n your age is {age} \n thank you and have good day\t ❤️")
# -----------------------------------------------------------------------------------------------------------------------
# تمرین جلسه دوم آشنایی با تایپ های مخلف
# @bot.message_handler(commands=['start'])
# def welcome(message):
# bot.reply_to(message, ("سلام"))
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id,"اسم تو بگو")
#     bot.register_next_step_handler(message, process_name )
# def process_name(message):
#     name = message.text
#     bot.send_message(message.chat.id,f"سلام  {name}" '  چند سالته؟')
#
#     bot.register_next_step_handler(message, process_age)
# def process_age(message):
#     age = message.text
#     bot.send_message(message.chat.id,f"تو {age} سالته\n مرسی"'')
#
#
# @bot.message_handler(commands=['bye'])
# def bye_message(message):
#     bot.reply_to(message, ("خدا نگهدار"))
#
# @bot.message_handler(commands=['help'])
# def help_message(message):
#     bot.reply_to(message,('این ربات برای کمک به تو درست شده'))
# @bot.message_handler(commands=['info'])
# def info_message(message):
#     bot.reply_to(message,('این ربات توسط امیر ساخته شده '))
#
# @bot.message_handler(content_types=['document', 'audio'])
# def handle_document_audio(message):
#     if message.audio:
#         bot.reply_to(message, 'آهنگ فرستادی')
#     elif message.document:
#         bot.reply_to(message, 'فایل فرستادی')
# @bot.message_handler(content_types=['photo'])
# def handle_document_photo(message):
#     if message.photo:
#         bot.reply_to(message, 'عکس فرستادی')
#
# @bot.message_handler(regexp='پدر')
# def handle_2024(message):
#     bot.reply_to(message, 'من پدرت هستم')
#
#
#
# @bot.message_handler(func=lambda msg: msg.text == '😂')
# def somthing(message):
#     bot.reply_to(message, "استیکر فرستادی")
bot.polling(none_stop=True, timeout=60)
