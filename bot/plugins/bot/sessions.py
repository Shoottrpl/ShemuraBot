from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from ..Generalbuttons import gen_inline_keyboard, start_button
from ..KeyboardButtons import session_keyboard
from bot.functions.crypt import encrypt_data, save_encrypted_data
from . import BotHelp, Config, ShemuraBot, LOGS

@ShemuraBot.bot.on_message(filters.command("session") & filters.private)
async def session_menu(_, message: Message):
    await message.reply_text("Chose option:", reply_markup=session_keyboard())


@ShemuraBot.bot.on_message(filters.regex(r"New") & filters.private)
async def new_session(_, message: Message):
    await message.reply_text("Setup new session", reply_markup=ReplyKeyboardRemove())

    phone_number = await ShemuraBot.ask(
        message.chat.id,
        "Enter your account phone number to add session:",
        timeout=120,
    )

    if phone_number.text == "/cancel":
        return await message.reply_text("Cancel progress")
    elif not phone_number.text.startswith("+") and not phone_number.text[1:].isdigit():
        return await message.reply_text("Phone number must be digits and contain country code")

    try:
        client = Client(
            name="SheMura 1.0",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            in_memory=True,
        )
        await client.connect()

        code = await client.send_code(phone_number.text)
        ask_otp = await ShemuraBot.ask(
            message.chat.id,
            "Enter OTP sent to your telegram account",
            timeout=300,
        )

        if ask_otp.text == "/cancel":
            return await message.reply_text("Cancel progress")
        otp = ask_otp.text.replace(" ", "")

        try:
            await client.sign_in(phone_number.text, code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            two_step_pass = await ShemuraBot.ask(
                message.chat.id,
                "Enter two step verification password:",
                timeout=120,
            )

            if   two_step_pass.text == "/cancel":
                return await message.reply_text("Cancel progress")

            await client.check_password(two_step_pass.text)

            session_string = await client.export_session_string()
            encrypt_session_string = encrypt_data(session_string, Config.CRYPT_KEY)
            save_encrypted_data(encrypt_session_string, Config.SESSIONS_FILE, index="sessions")
            LOGS.info(f"{encrypt_session_string}")
            await message.reply_text("Success session string generated and save in Json.")

    except TimeoutError:
        await message.reply_text("You took longer than excepted to complete process")

    except Exception as e:
        LOGS.info(f"{encrypt_session_string}")
        LOGS.info(f"{session_string}")
        LOGS.error(f"{e}")





