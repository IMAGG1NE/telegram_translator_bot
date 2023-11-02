from aiogram import Bot, types, executor, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentTypes
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from Keyboards import Keyboards
from deep_translator import GoogleTranslator
from translate import main
from bot_token import TOKEN_API

kb = Keyboards()
lang = GoogleTranslator()  
storage = MemoryStorage()

bot = Bot(TOKEN_API)  #  put your token_here
disp = Dispatcher(bot, storage=storage)


class ClientStatesGroup(StatesGroup):
    getting_file = State()
    chosing_language = State()


class Commands:
    @disp.message_handler(commands=["start"])
    async def start_cmd(message: types.Message):
        await message.answer(text="Добро пожаловать в моего бота, введите /info для просмототра функционала бота",
                             reply_markup=kb.get_keyboard())


    @disp.message_handler(Text(equals="❌ Отмена"), state="*")
    async def cancle_cmd(message: types.Message, state: FSMContext):
        if state is None:
            return
        
        await message.answer("Ваши действия были отменены❌", reply_markup=kb.get_keyboard())
        await state.finish()


    @disp.message_handler(Text(equals="Отправить файл 💾"))
    async def instruction_to_send(message: types.Message):
        await message.answer(text="отправьте нам файл💾 формата .wav", reply_markup=kb.get_cancel_kb())
        await ClientStatesGroup.getting_file.set()


class UserInteraction:
    @disp.message_handler(state=ClientStatesGroup.getting_file, content_types=ContentTypes.AUDIO)
    async def getting_file(message: types.Message, state: FSMContext):
        if message.audio.mime_type == "audio/wav":
            
            async with state.proxy() as data:
                data["wav_file"] = message.audio.file_id
            
            await message.answer("выберите язык на который перевести(russian, english, french)")
            await ClientStatesGroup.next()
        
        else:
            await message.answer("Пожалуйста, отправьте файл💾 с расширением .wav")       


    @disp.message_handler(state=ClientStatesGroup.chosing_language)
    async def chosing_language(message: types.Message, state: FSMContext):
        if lang.is_language_supported(message.text.lower()):
            async with state.proxy() as data:
                data["language"] = message.text 
            

            await message.answer("Пожалуйста ожидайте результата программы", reply_markup=kb.get_keyboard())
            file_processing = FileProcessing(message, state)
            await file_processing.file_processing()
            await state.finish()
        
        else:
            await message.answer("пожалуйста введите язык корректно на английском языке(russian, english, french)")
            
class FileProcessing():
    def __init__(self,message: types.Message, state: FSMContext) -> None:
        self.message = message
        self.state = state
        
    async def file_processing(self):
        async with self.state.proxy() as data:
            audio_file = data.get("wav_file")
            target_language = data.get("language")
            
        file_info = await bot.get_file(audio_file)
        file_path = file_info.file_path
        audio_file = await bot.download_file(file_path=file_path)
        main(audio_file, target_language)
        
        with open("result.txt", "rb") as result_file:
            await self.message.answer_document(result_file)
            
        with open("translated.txt", "rb") as translated_file:
            await self.message.answer_document(translated_file)
        
        
if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)