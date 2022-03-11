from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import  types
from config import ADMIN_ID
from aiogram.utils.callback_data import CallbackData
import db_handler as db

class Navigation(StatesGroup):
    main = State()  # Will be represented in storage as 'Navigation:main'
    settings = State()  # Will be represented in storage as 'Navigation:settings'
    admin = State()  # Will be represented in storage as 'Navigation:settings'



def load_main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("🔊 Historial", "⚙️ Configuración")
    if db.is_admin(message['from']['id']):
        markup.add("🔰 Admin")
    return markup  

def load_settings(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("🔙Atrás")
    return markup  
 
def load_admin(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("👥Usuarios", "🔙Atrás")
    return markup   



async def go_to(view, message, text):            
    if view == 'main':
        await Navigation.main.set()
        markup = load_main(message)
        await message.answer(text, reply_markup=markup, parse_mode=types.ParseMode.HTML)  
    elif view == 'settings':
        await Navigation.settings.set()
        markup = load_settings(message)
        await message.answer(text, reply_markup=markup, parse_mode=types.ParseMode.HTML) 
    elif view == 'admin':
        await Navigation.admin.set()
        markup = load_admin(message)
        await message.answer(text, reply_markup=markup, parse_mode=types.ParseMode.HTML) 