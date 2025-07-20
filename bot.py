from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import os

# 🔐 Сюди встав свій токен бота
TOKEN = "7345811292:AAHOqOBzidqWsz0YnpE5HJ6S0nMrSXxQXdo"

# 🔧 ID каналів для перевірки
channel_ids = [-1002457040012, -1002850244680, -1002763140931, -1002342966703]

# 🔗 Інвайт-посилання на канали
invite_links = [
    "https://t.me/+K8MxCDL55J03ZGVi",
    "https://t.me/+uylyFvSWa002ZmE6",
    "https://t.me/+PcyxcifpWYI5YWJi",
    "https://t.me/+uU9K2U97lpEyM2Ey"
]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 📲 Головне меню
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i, link in enumerate(invite_links):
        keyboard.insert(InlineKeyboardButton(text=f"Спонсор {i+1}", url=link))
    keyboard.add(InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subs"))

    await message.answer("Чтобы получить доступ, подпишись на всех спонсоров и нажми кнопку ниже ⬇️", reply_markup=keyboard)

# ✅ Перевірка підписки
@dp.callback_query_handler(lambda c: c.data == 'check_subs')
async def check_subscriptions(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    missed = []

    for i, channel_id in enumerate(channel_ids):
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in ['member', 'creator', 'administrator']:
                missed.append(i + 1)
        except Exception:
            missed.append(i + 1)

    if not missed:
        await bot.send_message(user_id, "✅ Ты подписан на всех спонсоров! Доступ открыт.")
    else:
        missed_str = ", ".join([f"Спонсор {i}" for i in missed])
        await bot.send_message(user_id, f"❌ Ты не подписан на: {missed_str}. Подпишись и попробуй снова.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)