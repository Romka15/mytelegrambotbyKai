from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

stats_kb = ReplyKeyboardMarkup(resize_keyboard=True)

info = KeyboardButton("Информация")
stats = KeyboardButton("Статистика")
stats_kb.add(stats, info)

stats_menu = InlineKeyboardMarkup()

stats_menu.add(InlineKeyboardButton(f'Да', callback_data = 'join'))
stats_menu.add(InlineKeyboardButton(f'Нет', callback_data = 'cancle'))

# Основное меню
MainMenu = InlineKeyboardMarkup(row_width=1)

btn_click = InlineKeyboardButton(text='Клик', callback_data='btnclick')

# Кнопка Кликера
MainMenu.add(btn_click)

# Кнопка Настройки и Новости
btn_settings = InlineKeyboardButton(text='Настройки', callback_data='btnsettings')
btn_channel = InlineKeyboardButton(text='Новости', callback_data='btnchannel')
MainMenu.row(btn_settings, btn_channel)

# Кнопка Меню и Хочу бота
btn_menu = InlineKeyboardButton(text='Меню', callback_data='btnmenu')
btn_hochu = InlineKeyboardButton(text='Хочу бота', callback_data='btnhochu')
MainMenu.row(btn_menu, btn_hochu)

# Кнопка Магазина
btn_shop = InlineKeyboardButton(text='Магазин', callback_data='btnshop')
MainMenu.add(btn_shop)

# Меню Новостей
channel_menu = InlineKeyboardMarkup(row_width=1)

# Кнопка со ссылкой на канал
btn_chann = InlineKeyboardButton('Канал', url='https://t.me/Kai41k_progects')
channel_menu.add(btn_chann)

# Кнопка назад
btn_back = InlineKeyboardButton(text='Назад', callback_data='back')
channel_menu.add(btn_back)

# Меню заказа бота
hochu_menu = InlineKeyboardMarkup(row_width=1)

# Кнопка со ссылкой на меня
btn_me = InlineKeyboardButton('Заказать', url='https://t.me/Kai41k')
hochu_menu.add(btn_me, btn_back)

# Меню настройки
settings_menu = InlineKeyboardMarkup(row_width=1).add(btn_back)

# Меню кнопки меню
btnmenu_menu = InlineKeyboardMarkup(row_width=1)

btn_random = InlineKeyboardButton(text='Рандомное число', callback_data='btnRandom')
btn_donate = InlineKeyboardButton('Поддержать автора', url='https://qiwi.com/n/KAI41K')
btnmenu_menu.add(btn_random, btn_donate, btn_back)

# Меню магазина
shop_menu = InlineKeyboardMarkup(row_width=1)

btn_shop_donate = InlineKeyboardButton('Пополнить баланс', url='https://qiwi.com/n/KAI41K')

# btn_TopUp = InlineKeyboardButton(text='Пополнить счёт', callback_data='top_up')

shop_menu.add(btn_shop_donate, btn_back)

def buy_menu(isUrl=True, url='', bill=''):
	qiwiMenu = InlineKeyboardMarkup(row_width=1)
	if isUrl:
		btnUrlQIWI = InlineKeyboardButton(text='Ссылка на оплату', url=url)
		qiwiMenu.insert(btnUrlQIWI)

	btncheckQIWI = InlineKeyboardButton(text='Проверить оплату', callback_data='check_'+bill)
	qiwiMenu.insert(btncheckQIWI)
	return qiwiMenu
