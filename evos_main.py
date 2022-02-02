from evos_db import Database
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, CallbackContext, ConversationHandler,
                          CommandHandler, CallbackQueryHandler, MessageHandler, Filters)


db = Database()
# db.add_category()
button = [
    [KeyboardButton("🛒 Buyurtma qilish")],
    [KeyboardButton("🛍 Buyurtmalarim"), KeyboardButton("👨‍👩‍👦 Proneo Oilasi")],
    [KeyboardButton("✍️ Fikr bildirish"), KeyboardButton("⚙️ Sozlamalar")]
]


# "parse_mode = 'HTML' "
def start(update, context):
    update.message.reply_text("Quyidagilardan  birini tanlang",
                              reply_markup=ReplyKeyboardMarkup(button))

    return 1


def menu(update, context):
    categories = db.get_menu()
    buttons = [
        [InlineKeyboardButton("📖Barcha menyular", url='https://telegra.ph/EVOS-MENU-04-05-2')]
    ]
    a = make_button(categories,"parent")
    buttons.extend(a)

    update.message.reply_text("Kategoriyalardan birini tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a> ",
                              parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
    return 2
def inline_query(update,context):
    query = update.callback_query
    data = query.data
    print(data)
    data_sp = data.split("_")
    if data_sp[0] == "category":
        if data_sp[1] == "parent":
            global ID
            ID = data_sp[2]
            categories = db.get_child_menu(int(data_sp[2]))
            buttons = make_button(categories,"child")
            buttons.append([InlineKeyboardButton("Ortga",callback_data="category_back")])
            query.message.edit_text("Kategoriyalardan birini tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a> ",
                                      parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
        elif data_sp[1] == "child":
            types = db.get_type(int(data_sp[2]))
            buttons= []
            btn = []
            for type in types:
                btn.append(
                    InlineKeyboardButton(f"{type['name']}", callback_data=f"product_{data_sp[2]}_{type['id']}"))
                if len(btn) == 2:
                    buttons.append(btn)
                    btn = []
            if btn:
                buttons.append(btn)
            buttons.append([InlineKeyboardButton("⬅️Ortga",callback_data=f"category_parent_{ID}")])
            query.message.delete()
            query.message.reply_text(
                "Kategoriyalardan birini tanlang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
        elif data_sp[1] == "back":
            query.message.delete()
            menu(query,context)
    elif data_sp[0] == "product":
        ctg_id = int(data_sp[1])
        type_id = int(data_sp[2])
        product = db.get_product(ctg_id, type_id)
        buttons = []
        btn = []
        for i in range(1,10):
            btn.append(InlineKeyboardButton(f"{i}",callback_data=f"count_{product['id']}_{i}"))
            if len(btn) == 3:
                buttons.append(btn)
                btn = []

        buttons.append([
            InlineKeyboardButton("⬅️Ortga",callback_data=f"category_child_{data_sp[1]}"),
            InlineKeyboardButton("⬆️Menyu",callback_data="category_back")
        ])

        query.message.delete()
        info = f"Narxi: {product['price']}\nTarkibi:{product['description']}\nMiqdorini tanlang yoki kiriting"
        query.message.reply_photo(photo=open(f"{product['photo']}","rb"),caption=info,
                                  reply_markup=InlineKeyboardMarkup(buttons))
    elif data_sp[0] == "count":
        pr_id = int(data_sp[1])
        count = int(data_sp[2])
        product = db.get_product_by_id(pr_id)
        savatcha = f"Savatchada:\n\n\n{product['name']}\n\n{count}❌{product['price']}\nSizning Umumiy xaridingiz {count*product['price']}so'm"
        query.message.delete()
        query.message.reply_text(savatcha)


def make_button(categories,holat):
    buttons = []
    btn = []
    for category in categories:
        btn.append(InlineKeyboardButton(f"{category['name']}", callback_data=f"category_{holat}_{category['id']}"))
        if len(btn) == 2:
            buttons.append(btn)
            btn = []
    if btn:
        buttons.append(btn)
    return buttons

def main():
    TOKEN = ""
    updater = Updater(TOKEN)
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.regex("🛒 Buyurtma qilish"), menu)
            ],
        states={
            1: [MessageHandler(Filters.regex("🛒 Buyurtma qilish"), menu)],
            2: [
                CallbackQueryHandler(inline_query),
                MessageHandler(Filters.regex("🛒 Buyurtma qilish"), menu),
                CommandHandler('start', start)
            ]
        },
        fallbacks=[]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
