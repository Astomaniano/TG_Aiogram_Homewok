import asyncio
from googletrans import Translator
from config import TOKEN
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram .types import Message, FSInputFile
import os
from gtts import gTTS

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\nЭто бот который переводит текст на английский язык!") #обращение к пользователю, можно full_name

@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.answer('Фото получено!')

@dp.message()
async def user_input(message: Message):
    print(message.text)
    translated = translator.translate(message.text, dest='en')
    await message.answer(translated.text)

    tts = gTTS(text=translated.text, lang='en')
    tts.save('translated.ogg')
    voice_answer = FSInputFile('translated.ogg')
    await message.answer_voice(voice_answer)
    os.remove('translated.ogg')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())