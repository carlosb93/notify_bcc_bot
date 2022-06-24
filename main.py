import time
import logging
import asyncio
import requests
# import Thread

# import tasks
import db_handler as db
import bot_message as bm

from os import system
from datetime import datetime
from urllib.parse import urlparse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import SchedulerEvent, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from navigation import Navigation, go_to
from config import TOKEN, REQUEST_KWARGS

scheduler = AsyncIOScheduler()
bgscheduler = BackgroundScheduler()

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, ChatType, ContentTypes, Contact


logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


if REQUEST_KWARGS == '':
    bot = Bot(token=TOKEN)
else:
    bot = Bot(token=TOKEN, proxy=REQUEST_KWARGS)
    
    
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

broadcast_target = {}

async def process_main(message: types.Message):
    if db.is_registered(message['from']['id']):
        
        if message.text == "🔊 Historial":
            u = db.get_user(uid=message['from']['id'])
            rply = bm.get_user_notifications(u.phone)
            await message.answer(text=rply, disable_notification=False, parse_mode=types.ParseMode.HTML)

        elif message.text == "⚙️ Configuración":
            u = db.get_user(uid=message['from']['id'])
            rply = bm.get_user_alert_status_prod(u.tgid)
            rply_inline_btn = bm.get_alert_options_btn_prod(u.tgid)
            await message.answer(text=rply, disable_notification=False,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)

        elif message.text == "🔰 Admin" and db.is_admin(message['from']['id']):
            await go_to('admin', message, bm.get_static_message('WelcomeAdmin'))    
    else:
        db.create_user(name=message['from']['first_name'],arroba=message['from']['username'],tgid=message['from']['id'])
        db.enable_conf_user(tgid=message['from']['id'], name='notificaciones')
        await message.reply(text='Hola soy un Bot de alerta rápida.\nEnvíame tu número ☎️ para suscribirte a las alertas\n\n', reply_markup=bm.get_registration_btn(message['from']['id']),parse_mode=types.ParseMode.HTML)
        
async def process_settings(message: types.Message):
    if db.is_registered(message['from']['id']):
            
        if message.text == "🔙Atrás":
            broadcast_target[message['from']['id']] = []
            await go_to('main', message, '..')

        # elif message.text == "👥Users" and db.is_admin(message['from']['id']):
        #     await message.answer(text=bm.get_all_users_admin(), parse_mode=types.ParseMode.HTML)     
    else:
        await message.reply(bm.get_static_message('NoPriviledges'))
        
async def process_admin(message: types.Message):
    if db.is_admin(message['from']['id']):
            
        if message.text == "🔙Atrás":
            broadcast_target[message['from']['id']] = []
            await go_to('main', message, '..')

        elif message.text == "👥Usuarios" and db.is_admin(message['from']['id']):
            await message.answer(text=bm.get_all_users_admin(), parse_mode=types.ParseMode.HTML)     
    else:
        await message.reply(bm.get_static_message('NoPriviledges'))
        
#commands
async def general_commands(message: types.Message):
    if db.is_registered(message['from']['id']):

        if message.text.startswith('/help'):
            await message.answer(bm.get_help(), parse_mode=types.ParseMode.HTML)
            
        if message.text.startswith('/removeme'):
            db.del_user_phone(tgid=message['from']['id'])
            await message.answer(bm.get_static_message('RemovePhone',ulang='Spanish'), parse_mode=types.ParseMode.HTML)
        if db.is_admin(message['from']['id']):
            
            if message.text.startswith('/enable_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[8:].strip()
                else:
                    tgid = command[8:].strip()
                
                db.enable_user_subscription(tgid=tgid)
                await message.answer(bm.get_static_message('Done',ulang='Spanish'), parse_mode=types.ParseMode.HTML)
            
            if message.text.startswith('/disable_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[9:].strip()
                else:
                    tgid = command[9:].strip()
                    
                db.disable_user_subscription(tgid=tgid)
                await message.answer(bm.get_static_message('Done',ulang='Spanish'), parse_mode=types.ParseMode.HTML)
            
            if message.text.startswith('/ban_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[5:].strip()
                else:
                    tgid = command[5:].strip()
                    
            if message.text.startswith('/back'):
                await go_to('main', message, '..')
                 
            if message.text.startswith('/users'):
                rply = bm.get_all_users_admin()
                await message.answer(text=rply, parse_mode=types.ParseMode.HTML)  
            
        if message.text.startswith('/subscribe'):    
            command = message.text
            print(command)
            if '#' in command:
                await go_to('main', message, bm.get_static_message('WrongNumber',ulang='Spanish'))
            else:
                if '@' in command:
                    command = command.split('@')[0]
                phone = command[10:].strip()
                db.update_user_phone(phone=phone,tgid=message['from']['id'])   
                         
                await message.answer(bm.get_static_message('Subscribed',ulang='Spanish'),parse_mode=types.ParseMode.HTML)
 

async def check_db_alert(bot):
    print('check db alert')
    mensajes = db.get_msg_all()
    if mensajes:
        for mensaje in mensajes:
          
            if mensaje.status:
                db.unset_msg(id=mensaje.id)
                await alerta_telegram(type=mensaje.type,phone=mensaje.phone,text=mensaje.text,bank=mensaje.bank,status=mensaje.status,created_at=mensaje.created_at)
            
           
    
async def alerta_telegram(type=None,phone=None,text=None,bank=None,status=None,created_at=None):
    users = db.get_all_users()
    formated = '⚠️⚠️⚠️ Alerta  ⚠️⚠️⚠️\n'
    for u in users:
        if u.phone == phone:
            settings_user = db.get_user_alerts(uid=u.tgid)
            if settings_user:
                for a in settings_user:
                    settings = db.get_setting_alert(settings_user=a,kind='alert')
                    formated +="<b>{}</b>\n\n".format(bank)
                    formated += "{}\n\n".format(text.replace('\\n','\n'))
                    formated += "-------------------------\n"
                    formated += "Fecha {}\n".format(created_at)
                    if settings:
                        await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                    else:
                        await bot.send_message(u.tgid, bm.get_static_message('Conf_alerts',ulang='Spanish'), disable_notification=True, parse_mode=types.ParseMode.HTML)
        
                          


@dp.callback_query_handler(state='*')
async def process_callback_button(callback_query: types.CallbackQuery):

    data = callback_query.data
    settings = db.get_setting_alert(kind='all')
  
    if settings:
        
        alerta_activa = db.get_alerta_activa(uid=callback_query.from_user.id,setting_id=data)
        if alerta_activa:            
            
            db.disable_conf_user(tgid=callback_query.from_user.id, name=data)# ❌ 
            
            if db.is_kind_prod(data):
                rply = bm.get_user_alert_status_prod(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_prod(callback_query.from_user.id)
            else:
                rply = bm.get_user_alert_status_url(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_url(callback_query.from_user.id)
            
            await bot.answer_callback_query(callback_query.id, bm.get_static_message('RemoveAlert',ulang='Spanish'))
            await bot.edit_message_text(text=rply,chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)        
        else:
            
            db.enable_conf_user(tgid=callback_query.from_user.id, name=data) # ✅
            
            if db.is_kind_prod(data):
                rply = bm.get_user_alert_status_prod(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_prod(callback_query.from_user.id)
            else:
                rply = bm.get_user_alert_status_url(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_url(callback_query.from_user.id)
                
            await bot.answer_callback_query(callback_query.id, bm.get_static_message('AddedAlert',ulang='Spanish'))            
            await bot.edit_message_text(text=rply,chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)
    else:
        
        db.enable_conf_user(tgid=callback_query.from_user.id, name=data) # ✅
        
        if db.is_kind_prod(data):
            rply = bm.get_user_alert_status_prod(callback_query.from_user.id)
            rply_inline_btn = bm.get_alert_options_btn_prod(callback_query.from_user.id)
        else:
            rply = bm.get_user_alert_status_url(callback_query.from_user.id)
            rply_inline_btn = bm.get_alert_options_btn_url(callback_query.from_user.id)
            
        await bot.send_message(callback_query.from_user.id, bm.get_static_message('AddedAlert',ulang='Spanish'))
        await bot.edit_message_text(text=rply,chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)


@dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
async def handle_contact(message: types.Message, state: FSMContext):
    if message['contact']:
        if message['contact']['user_id'] == message['from']['id']:
            db.update_user_phone(phone=message['contact']['phone_number'].replace('+',''),tgid=message['contact']['user_id'])   
            # await bot.send_message(message['from']['id'], bm.get_static_message('Subscribed',ulang='Spanish'), disable_notification=True, parse_mode=types.ParseMode.HTML)         
            await go_to('main', message, bm.get_static_message('Subscribed',ulang='Spanish'))
            # await message.answer(bm.get_static_message('Subscribed',ulang='Spanish'),parse_mode=types.ParseMode.HTML)
    else:
        if message.is_command():
            await general_commands(message)
        if message['chat']['type'] == 'private':
            current_state = await state.get_state()
            if current_state is None:
                await go_to('main', message, bm.get_static_message('Welcome',ulang='Spanish'))
                await process_main(message)
            elif current_state == Navigation.main.state:
                await process_main(message)
            elif current_state == Navigation.settings.state:
                await process_settings(message)
            elif current_state == Navigation.admin.state:
                await process_admin(message)
    
    

# @dp.message_handler(state='*')
# async def router(message: types.Message, state: FSMContext):
#     # if message.forward_from or message.forward_from_chat:
#     #     # await forwards(message)
#     print(message)
#     if message.is_command():
#         await general_commands(message)
#     if message['chat']['type'] == 'private':
#         current_state = await state.get_state()
#         if current_state is None:
#             await go_to('main', message, bm.get_static_message('Welcome',ulang='Spanish'))
#             await process_main(message)
#         elif current_state == Navigation.main.state:
#             await process_main(message)
#         elif current_state == Navigation.settings.state:
#             await process_settings(message)
#         elif current_state == Navigation.admin.state:
#             await process_admin(message)

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')
        job = bgscheduler.get_job(event.job_id)
        if job.name == 'start_api':
            print('Running check_db_alert')
            # lookup the second job (assuming it's a scheduled job)
            jobs = scheduler.get_jobs()
            second_job = next((j for j in jobs if j.name == 'db_check'), None)
            if second_job:
                # run the second job immediately
                second_job.modify(next_run_time=datetime.now())
            else:
                # job not scheduled, add it and run now
                scheduler.add_job(check_db_alert, 'interval', minutes=1,name='db_check', kwargs={'bot': bot})
                
           

def schedule_all_tasks():
    bgscheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    bgscheduler.start()
    # scheduler.add_job(run, name='tasks')   
    scheduler.add_job(check_db_alert, 'interval', seconds=30, name='db_check', kwargs={'bot': bot})   
    scheduler.start()     
    

if __name__ == '__main__':
    target=schedule_all_tasks()
    executor.start_polling(dp, skip_updates=True)
    
    
