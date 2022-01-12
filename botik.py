from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio

from random import randint

from config import TOKEN, Owner, Moder
import markups as nav
from db import Database
from pyqiwip2p import QiwiP2P

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Важные переменные
db = Database('DataBase.db')
usersowner = db.get_users_owner()
balance = 0

def clicker():
	global balance
	balance = balance + 1

def is_number(_str):
	try:
		int(_str)
		return True
	except ValueError:
		return False

# Команда старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	if not db.user_exists(message.from_user.id):
		db.add_user(message.from_user.id, message.from_user.username)
	await bot.send_message(message.from_user.id, f'Приветик :3\nВаш счёт: {db.user_money(message.chat.id)} руб.\nВаш баланс: {balance} чебукоинов', reply_markup=nav.MainMenu)

@dp.message_handler(commands=['sendall'])
async def sendall(message):
    if message.from_user.id == Owner:
    	text = message.text[9:]
    	users = db.get_users()
    	for row in users:
    		try:
    			await bot.send_message(row[0], text)
    			if int(row[1]) != 1:
    				db.set_active(row[0], 1)
    		except:
    			db.set_active(row[0], 0)

    	await bot.send_message(message.from_user.id, f'Успешная рассылка!')

@dp.message_handler(commands=['stats'])
async def stats_command(message: types.Message):
	if message.from_user.id == Owner:
		await bot.send_message(message.from_user.id, 'Вся статистика\n по кнопкам внизу :3', reply_markup=nav.stats_kb)
	elif message.from_user.id == Moder:
		await bot.send_message(message.from_user.id, 'Вся статистика\n по кнопкам внизу :3', reply_markup=nav.stats_kb)
	else: 
		await bot.send_message(message.from_user.id, 'Эта команда нечего не делает')

# Команда помощи
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
	await bot.send_message(message.from_user.id, 'Нужна помощь?\nПиши: @Kai41k\nТакже если ты нашёл баг,\nТо пиши подробно сюда @Kai41k')

@dp.message_handler(content_types=['text'])
async def get_message(message):
 	if message.text == "Информация":
 		await bot.send_message(message.from_user.id, text = 'Информация\nБот создан Пользователем @Kai41k')

 	if message.text == "Статистика":
 		await bot.send_message(message.chat.id, text = 'Хочешь просмотреть статистику бота?', reply_markup=nav.stats_menu)

@dp.message_handler()
async def bot_mess(message: types.Message):
	if is_number(message.text):
		message_money = int(message.text)
		if message_money >= 1:
			comment = str(message.from_user.id) + '_' + str(randint(1000, 9999))
			bill = p2p.bill(amount=message_money, lifetime=15, comment=comment)

			db.add_check(message.from_user.id, message_money, bill.bill_id)

			await bot.send_message(message.from_user.id, f'Вам нужно отправить {message_money} руб. на наш счёт QIWI\nСсылка: {bill.pay_url}\nУказав комментарий к оплате: {comment}', reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id))

		else:
			await bot.send_message(message.from_user.id, 'Минимальная сумма для пополнения 1 руб.')
	else:
		await bot.send_message(message.from_user.id, 'Введите целое число')

# Действие инлайн кнопок при нажатии
@dp.callback_query_handler(text='btnclick')
async def clicker_btn(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	clicker()
	await bot.send_message(callback.from_user.id, f'+1 Клик.\nВаш баланс: {balance} чебукоин', reply_markup=nav.MainMenu)

@dp.callback_query_handler(text='btnRandom')
async def randomizer(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Рандомное число: {0}'.format(randint(0, 100)), reply_markup=nav.btnmenu_menu)

@dp.callback_query_handler(text='btnchannel')
async def channel(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Новостной канал:', reply_markup=nav.channel_menu)

# Инлайн кнопка назад
@dp.callback_query_handler(text='back')
async def back(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Вы в главном меню', reply_markup=nav.MainMenu)

@dp.callback_query_handler(text='btnsettings')
async def settings(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Настроек пока нет,\nНо скоро они будут', reply_markup=nav.settings_menu)

@dp.callback_query_handler(text='btnmenu')
async def menu(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Меню этого бота :3', reply_markup=nav.btnmenu_menu)

@dp.callback_query_handler(text='btnhochu')
async def hochu(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Хочешь такого же бота?\nТогда пиши по кнопке внизу', reply_markup=nav.hochu_menu)

@dp.callback_query_handler(text='btnshop')
async def shop(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Магазин:\nЗдесь ты можешь пополнить баланс', reply_markup=nav.shop_menu)

@dp.callback_query_handler(text='top_up')
async def top_up(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Введите сумму пополнения!')


@dp.callback_query_handler(text_contains='check_')
async def check(callback: types.CallbackQuery):
	bill = str(callback.data[6:])
	info = db.get_check(bill)
	if info != False:
		if str(p2p.check(bill_id=bill).status) == 'PAID':
			user_money = db.user_money(callback.from_user.id)
			money = int(info[2])
			db.set_money(callback.from_user.id, user_money+money)
			await bot.send_message(callback.from_user.id, 'Ваш счёт пополнен! Нажмите /start')


		else:
			await bot.send_message(callback.from_user.id, 'Вы не оплатили счёт!', reply_markup=nav.buy_menu(False, bill=bill))
	else:
		await bot.send_message(callback.from_user.id, 'Счёт не найден')

@dp.callback_query_handler(text_contains='join') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "JOIN" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "JOIN"
async def join(call: types.CallbackQuery):
	if call.message.chat.id == Owner:
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'Вот статистика бота:\nid, user_id, username, money, active\n{usersowner}')
	elif call.message.chat.id == Moder:
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'Вот статистика бота:\nid, user_id, username, money, active\n{usersowner}')
	else: 
		await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'У тебя нет админки\n Куда ты полез')
 
 
 
@dp.callback_query_handler(text_contains='cancle') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "cancle" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "cancle"
async def cancle(call: types.CallbackQuery):
	await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "Ты вернулся В главное меню. Жми опять кнопки", parse_mode='Markdown')

@dp.message_handler(content_types=['text'])
async def get_message(message):
 	if message.text == "Информация":
 		await bot.send_message(message.from_user.id, text = 'Информация\nБот создан пользователем: @Kai41k')

 	if message.text == "Статистика":
 		await bot.send_message(message.chat.id, text = 'Хочешь просмотреть статистику бота?', reply_markup=nav.stats_menu)


if __name__ == '__main__':
	print('Бот запущен :3')
	executor.start_polling(dp, skip_updates=True)