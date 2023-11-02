from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class Keyboards:
    def get_keyboard(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        
        b1 = KeyboardButton("Отправить файл 💾")
        kb.add(b1)
        
        return kb
        
    
    def get_cancel_kb(self):
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("❌ Отмена"))

