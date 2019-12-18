from config import TG_TOKEN
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from models import session, User, Products

def admin(update, context):
    if update.message.from_user.id == 426603840:
        buttons = [[InlineKeyboardButton("Продукты", callback_data="admin_products"),
                    InlineKeyboardButton("Рассылка", callback_data="distribution")]]
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text="Вход админа", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        context.bot.send_message(chat_id=update.message.from_user.id,
                                 text="Ошибка входа")


def product_for_user(update, context):
    telegram_user = update.effective_user
    #prodct_num = update.message.from_user
    buttons = [[InlineKeyboardButton("Купить", callback_data="admin_delete")]]
    select_product = session.query(Products).all()
    for f in select_product:
        print(f.id, f.name, f.discription)

        #f_id=f.id;f_name=f.name;f_discription=f.discription
        context.bot.send_message(chat_id=telegram_user.id, text="{id}, {name}, {discription}".format(id=f.id,name=f.name, discription=f.discription))
    context.bot.send_message(chat_id=telegram_user.id, text="Выберите действие: ",
                             reply_markup=InlineKeyboardMarkup(buttons))


def product_for_admin(update, context):

    telegram_user = update.effective_user
    buttons = [[InlineKeyboardButton("Удалить", callback_data="admin_delete"),
                InlineKeyboardButton("Добавить", callback_data="admin_add"),
                InlineKeyboardButton("Изменить", callback_data="admin_change")]]
    select_product = session.query(Products).all()
    for f in select_product:
        context.bot.send_message(chat_id=telegram_user.id, text="{id}, {name}, {discription}".format(id=f.id,name=f.name, discription=f.discription))
    context.bot.send_message( chat_id=telegram_user.id,text="Выберите действие: ",reply_markup = InlineKeyboardMarkup(buttons))


def delete_product(update, context):
    telegram_user = update.effective_user
    products = session.query(Products).first()
    context.bot.send_message(chat_id=telegram_user.id, text="Введите название продукта, который хотите удалить: ")
    text = update.message.text
    text = "".join(text.split())
    buttons = [[InlineKeyboardButton("Старт", callback_data="admin_start")]]
    if text == products.name:
        session.delete(products)
        session.commit()
        context.bot.send_message(chat_id=telegram_user.id, text="Продукт был удален ",reply_markup = InlineKeyboardMarkup(buttons))
    else:
        context.bot.send_message(chat_id=telegram_user.id, text="Такого продукта нет ",reply_markup = InlineKeyboardMarkup(buttons))

def add_product(update, context):
    telegram_user = update.effective_user
    context.bot.send_message(chat_id=telegram_user.id, text="Введите название продукта, затем его описание, чтоб добавить новый продукт: ")
    text = update.message.text

    if 'name' not in context.user_data:
        val = context.validators.String()
        context.user_data['name'] = val.to_python(text)
    elif 'discription' not in context.user_data:
        val = context.validators.Number()
        context.user_data['discription'] = val.to_python(text)
        new_product = Products(name = context.user_data['name'],  discription=context.user_data['discription'])
        session.add(new_product)
        session.commit()
        context.bot.send_message(chat_id=telegram_user.id, text="Продукт добавлен: ")
        del context.user_data['name']
        del context.user_data['discription']

def distribution(update, context):
    telegram_user = update.effective_user
    for i in User:
        context.bot.send_message(chat_id=i,text="Привет всем: ")
    context.bot.send_message(chat_id=telegram_user.id,text="Рассылка завершена: ")


def start(update, context):
    buttons = [[InlineKeyboardButton("Просмотр продуктов", callback_data="show_products")]]
    context.bot.send_message(chat_id=update.message.from_user.id, text="Здравствуйте, Вас приветствует бот Products_bot",
                             reply_markup=InlineKeyboardMarkup(buttons))
    telegram_user = update.message.from_user

    user = session.query(User).filter(User.chat_id == telegram_user.id).first()
    if user is None:
        session.add(
            User(
                chat_id=telegram_user.id,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                username=telegram_user.username
               )
        )
        session.commit()

updater = Updater(TG_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('admin', admin))

dp.add_handler(MessageHandler(Filters.text, delete_product))
dp.add_handler(MessageHandler(Filters.text, add_product))

dp.add_handler(CallbackQueryHandler(product_for_admin, pattern="admin_products"))
dp.add_handler(CallbackQueryHandler(product_for_user, pattern="show_products"))
dp.add_handler(CallbackQueryHandler(delete_product, pattern="admin_delete"))
dp.add_handler(CallbackQueryHandler(add_product, pattern="admin_add"))
dp.add_handler(CallbackQueryHandler(distribution, pattern="distribution"))
dp.add_handler(CallbackQueryHandler(admin, pattern="admin_start"))

updater.start_polling()
updater.idle()
