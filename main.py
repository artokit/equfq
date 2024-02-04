import random
import time
from aiogram import Bot, Dispatcher, F
import asyncio
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import db_api
import keyboards

TOKEN = '6882754666:AAH2CF3HLwL8SWWuOF8FyYFPgKlne46NUjM'
COOLDOWN = 4 * 60 * 60
bot = Bot(TOKEN)
dp = Dispatcher()
PLAYERS_WAIT = set()


@dp.message(Command('start'))
async def start(message: Message):
    db_api.add_user(message.chat.id)
    await message.answer(
        "BOT ISHKA TAYYOR✅\n\n"

        "Bot shartlari:\n"
        "1. Sizdab boshqa telefon ishlata omidi⚠️\n"
        "2. Topkan pulizdan menga - 20% bermasez, bot ochiriladi\n"
        "3. Hamma narsada menga quloq soling( masalan: stop desam BOT ishlatmisiz, chunki hatosi bolishi mumkin, keyin START deganda ishlurasiz)\n"
        "4. Oyiga ishlamay, shunkani bot olip oshlamasez( menga beradigan 20%dan - 40.000.000 somdan kam bolsa, bot ochiriladi, menga 40mln bolsa demak 200mln daromad qlishiz kerak, siz ozizga 160 qoldirasiz,BU MINIMAL shart)\n\n"
        
        "🔹Bot sizga aniq koefficient beradi, pulingizni o'z vaqtida oling.\n"
        "🔹 Hamma shart bajarishka tayyor bolsez ⬇️ bosing",
        reply_markup=keyboards.start()
    )


@dp.callback_query(F.data == 'next')
async def next_step(call: CallbackQuery):
    await call.message.answer(
        "Minimal boshlash - HISOBIZDA 100.000 som shart✅\n\n"
        "Aniq KF olishka tayyor bolsez, START bosing⤵️",
        reply_markup=keyboards.get_signal()
    )


@dp.callback_query(F.data == 'get_signal')
async def get_signal(call: CallbackQuery):
    if call.message.chat.id in PLAYERS_WAIT:
        return

    user = db_api.get_user(call.message.chat.id)
    if (user[1] >= 20) and (time.time() - user[2] < COOLDOWN):
        return await call.message.answer(
            '⚠️The CASINO system, noticed suspicious!⚠️\n\n'
            '🛑Signals are limited to 4 hours!🛑\n\n'
            '🟢Make a deposit 400 rupees to continue receiving signals!🟢\n\n'
            'Or wait for 4 hours - the bot will restore the work, so as not to arouse suspicion of CASINO⚠️',
            reply_markup=keyboards.get_me()
        )

    tries = user[1]
    if tries >= 20:
        db_api.update_tries(call.message.chat.id, 0)
        tries = 0

    PLAYERS_WAIT.add(call.message.chat.id)
    await call.message.answer('Checking bets🚀')
    await asyncio.sleep(random.randint(1, 3))
    name = call.message.chat.username or ''
    name = name.replace("_", "\_")

    await call.message.answer(
        f'PLAYER: @{name}\n'
        f'*CASHOUT: %.2f ✅*' % round(random.randint(100, 250)/100, 2),
        parse_mode='markdown',
        reply_markup=keyboards.get_next_signals()
    )

    PLAYERS_WAIT.remove(call.message.chat.id)
    db_api.update_timestamp_user(call.message.chat.id)
    db_api.update_tries(call.message.chat.id, tries+1)


asyncio.run(dp.start_polling(bot))
