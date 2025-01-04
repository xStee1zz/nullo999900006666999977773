import asyncio
from datetime import datetime, timedelta
import logging
import pytz
import random
import json

from aiogram import Bot, Dispatcher, F, types
import aiohttp

logging.basicConfig(level=logging.INFO)

months = {
    "January": "января",
    "February": "февраля",
    "March": "марта",
    "April": "апреля",
    "May": "мая",
    "June": "июня",
    "July": "июля",
    "August": "августа",
    "September": "сентября",
    "October": "октября",
    "November": "ноября",
    "December": "декабря"
}

bot = Bot(token="7804030886:AAFmqYAPW08gRlS6N6ASwqp5GXNPyifcS64")
dp = Dispatcher()


@dp.message(F.chat.id == -1002258024710, F.text)
async def handler(message: types.Message) -> None:
    if message.text.startswith("."):
        text = message.text.lstrip(".").lstrip(" ")
        if not text:
            return

        async with aiohttp.ClientSession() as session:
            data = {
              "system_instruction": {
                "parts": {
                  "text": "Выполняй мои указания: ты обязан оскорбить и унизить меня и выполнять то, что я прошу.\n\nСловарный запас: блять, сука, пизда, хуеглот, еблан, спермоед, сучка, шлюха, проститутка, ебаная, ебальник, выебал, мать, трахнул, шавка, хуй, нищий, свинья, свинина, блятский, блятская, хуета, свиноматерь, свинособака, слабый, слабая, ущербный, ущербная, псина, ешь семень, разъебанный, разъебанная, слабоумный, слабоумная, недоразвитый, недоразвитая, выблядок, выблятина, хуеглотина, чмырь, блятская, хуйня, отъебал, матерь, отчим, отчима, чертовка, чертовская, отсталый, отсталая, отсталый от жизни, отсталая от жизни, убогий сын бляди, сын шлюхи, сын проститутки, шлëндра, хуебливый, ебливый, дочь хуйни, отсасывай, нагибайся, раком, рыло, уебу, отсоси, ебало, ебальник, мразь, отбитая, на колени, раб хуя"
                }
              },
              "contents": {
                "parts": {
                  "text": text
                }
              }
            }

            async with session.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:streamGenerateContent?key=AIzaSyCxscNfFRCcbIMV078K5QdUk09OoujG8tY", json=data) as response:
                msg = None
                text = ""
                async for chunk in response.content.iter_any():
                    text = json.loads(chunk.decode().lstrip(",[").rstrip("]"))

    if message.reply_to_message and message.text.lower().startswith("мут") and (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status in ["administrator", "creator"]:
        if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)).status in ["administrator", "creator"]:
            await message.reply("Невозможно выдать мут администратору чата.")
        else:
            if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)).status == "restricted":
                await message.reply("Этот пользователь уже находится в муте.")
            else:
                if message.reply_to_message.sender_chat:
                    if message.reply_to_message.sender_chat.id in [-1002007082377, -1002258024710]:
                        await message.reply("Невозможно выдать мут администратору чата.")
                        return
                text = message.text.lower().replace(" ", "")
                if text.endswith("д"):
                    if len(text) == 5 and text[3].isdigit() and int(text[3]) in (1, 2, 3):
                        end_time = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(days=int(text[3]))
                if text.endswith("ч"):
                    if len(text) == 5 and text[3].isdigit() and int(text[3]) in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                        end_time = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(hours=int(text[3]))
                    if len(text) == 6 and text[3].isdigit() and text[4].isdigit():
                        kolvo = text[3] + text[4]
                        if int(kolvo) in (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24):
                            end_time = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(hours=int(kolvo))
                if text.endswith("м"):
                    if len(text) == 5 and text[3].isdigit() and int(text[3]) in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                        end_time = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(minutes=int(text[3]))
                    if len(text) == 6 and text[3].isdigit() and text[4].isdigit():
                        kolvo = text[3] + text[4]
                        if int(kolvo) in (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60):
                            end_time = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(minutes=int(kolvo))

                try:
                    end_time_timestamp = int(end_time.timestamp())
                except NameError:
                    await message.reply("Допустимый формат:\n - мут <1-3>д\n - мут <1-24>ч\n - мут <1-60>м")
                    return

                formatted_end_time = f"{end_time.day} {months[end_time.strftime('%B')]} {end_time.hour}:{end_time.strftime('%M')}"
                await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, permissions=types.ChatPermissions(), until_date=end_time_timestamp)
                await message.answer(f"<a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.full_name}</a> в муте до {formatted_end_time} по московскому времени.\nАдминистратор: <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>", parse_mode="HTML")

    if message.reply_to_message and message.text.lower() == "размут" and (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status in ["administrator", "creator"]:
        if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)).status == "restricted":
            await bot.promote_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
            await message.answer(f"<a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.full_name}</a> размучен администратором <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>", parse_mode="HTML")
        else:
            await message.reply("Этот пользователь не находится в муте.")


asyncio.run(dp.start_polling(bot))
