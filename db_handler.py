import os
import json
import sqlite3
import time
import contextlib
from data.db_map import Base, Mensajes, User, Settings, Settings4User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from config import DB_FILENAME, DB_LOCATION, ADMIN_ID

db_empty = False

if not DB_FILENAME in os.listdir(DB_LOCATION):
    print('Not db found, creating one')
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///'+ DB_LOCATION + '//' + DB_FILENAME)
    
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    db_empty = True
else:
    engine = create_engine('sqlite:///'+ DB_LOCATION + '//' + DB_FILENAME)
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine


 
DBSession = sessionmaker(bind=engine)
Session = scoped_session(DBSession)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. 
s = Session()

def is_registered(uid):
    user = get_user(uid=uid)
    if user:
        return True
    return False
    
def user_exists(phone):
    user = get_user(phone=phone)
    if user:
        return True
    return False

def is_admin(uid):
    if uid in ADMIN_ID:
        return True
    return False

def is_kind_prod(data=None):
    qry = s.query(Settings).filter(Settings.name == data).one()
    s.close()
    if qry.setting_type == 'alert':
        return True
    else:
        return False

def is_kind_url(data=None):
    qry = s.query(Settings).filter(Settings.name == data).one()
    s.close()
    if qry.setting_type == 'url':
        return True
    else:
        return False

def kick_from_alliance(guild):
    guild.alliance_id = 'Unknown Alliance'
    s.add(guild)
    s.commit() 
    s.close()
    
def on_user_setting(uid, sett):
    user = get_user(uid=uid)
    if user:
        try:
            status = s.query(Settings4User).filter(Settings4User.setting == sett)
            status = status.filter(Settings4User.user == user.name).one()
            status.value = 1
            s.add(status)
        except sqlalchemy.orm.exc.NoResultFound:
            s.add(Settings4User(setting=sett, user=user.name, value=1))    
        s.commit()
        s.close()

def off_user_setting(uid, sett):
    user = get_user(uid=uid)
    if user:
        try:
            status = s.query(Settings4User).filter(Settings4User.setting == sett)
            status = status.filter(Settings4User.user == user.name).one()
            status.value = 0
            s.add(status)
        except sqlalchemy.orm.exc.NoResultFound:
            s.add(Settings4User(setting=sett, user=user.name, value=0)) 
        s.commit() 
        s.close()
        
# Settings
    

def disable_conf_user(tgid=None, name=None):# ❌
    setting = s.query(Settings).filter(Settings.name == name).one()
    s.close()
    if setting:
        del_user_alert(uid=tgid,setting_id=setting.name)
        
        

def enable_conf_user(tgid=None, name=None): # ✔️
    setting = s.query(Settings).filter(Settings.name == name).one()
    s.close()
    if setting:
        add_user_alert(uid=tgid,setting_id=setting.name)

#Mensajes
# tipo
# phone
# texto
# status
def unset_msg(id=None):
    mensaje = s.query(Mensajes)
    if mensaje:
        try:
            mensaje = mensaje.filter(Mensajes.id == id)
            mensaje = mensaje.one()
            
            mensaje.status = False
            s.add(mensaje)
            s.commit()
            s.close()
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def set_msg(type=None,phone=None,text=None,bank=None,status=None):
    mensaje = s.query(Mensajes)
    if mensaje:
        try:
            mensaje = mensaje.filter(Mensajes.text == text)
            mensaje = mensaje.one()
            
            mensaje.type = type
            mensaje.phone = phone
            mensaje.text = text
            mensaje.bank = bank
            mensaje.status = True
            mensaje.created_at = time.time()
            s.add(mensaje)
            s.commit()
            s.close()
            
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
            
        
def add_msg(type=None,phone=None,text=None,bank=None,status=None):
    s.add(Mensajes(type=type, phone=phone, text=text, bank=bank, status=True, created_at=time.time()))
    s.commit()
    s.close()
    
    

def get_msg(phone=None):
    mensaje = s.query(Mensajes).filter(Mensajes.phone == phone).order_by(Mensajes.id.desc()).limit(5)
    if mensaje:
        try:
            mensaje = mensaje.all()
            s.close()
            return mensaje
            
        
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def get_msg_all():
    mensaje = s.query(Mensajes).filter(Mensajes.status == True)
    if mensaje:
        try:
            mensaje = mensaje.all()
            s.close()
            return mensaje
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass


 
# User
def create_user(name=None,lang=None, arroba=None, tgid=None):
    s.add(User(name=name,lang=lang, arroba=arroba, tgid=tgid, status=True, status_date=time.time()))
    s.commit()
    s.close()
    return 'New User Created'



def update_user_phone(phone=None, tgid=None):
    user = s.query(User)
    user = user.filter(User.tgid == tgid).one()
    if user:
        user.phone = phone
    s.add(user)
    s.commit()
    s.close()
    return 'User Subscribed'

def del_user_phone(tgid=None):
    user = s.query(User)
    user = user.filter(User.tgid == tgid).one()
    if user:
        user.phone = ' '
        user.status = False
    s.add(user)
    s.commit()
    s.close()
    return 'Succesfully'

def disable_user_subscription(tgid=None):
    user = s.query(User)
    user = user.filter(User.tgid == tgid).one()
    if user:
        user.status = False
    s.add(user)
    s.commit()
    s.close()
    return 'Succesfully'

def enable_user_subscription(tgid=None):
    user = s.query(User)
    user = user.filter(User.tgid == tgid).one()
    if user:
        user.status = True
        user.status_date = time.time()
    s.add(user)
    s.commit()
    s.close()
    return 'Succesfully'
    
def get_user(uid=None, name=None, phone=None):
    user = s.query(User)
    if uid:
        qry = user.filter(User.tgid == uid)
    elif name:
        qry = user.filter(User.name == name)
    elif phone:
        qry = user.filter(User.phone == phone)
    if qry:
        try:
            qry = qry.one()
            s.close()
            return qry
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def get_all_users():
    user = s.query(User)
    if user:
        try:
            user = user.all()
            s.close()
            return user
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def get_user_alerts(uid=None):
    setting = s.query(Settings4User)
    if uid:
        setting = setting.filter(Settings4User.user_id == uid)
    if setting:
        try:
            setting = setting.all()
            s.close()
            return setting
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def get_alerta_activa(uid=None,setting_id=None):
    setting = s.query(Settings4User)
    if setting:
        setting = setting.filter(Settings4User.user_id == uid)
        setting = setting.filter(Settings4User.setting_id == setting_id)
        try:
            setting = setting.all()
            s.close()
            return setting
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def get_user_alert(uid=None, setting_id=None):
    setting = s.query(Settings4User)
    if uid:
        setting = setting.filter(Settings4User.user_id == uid)
        setting = setting.filter(Settings4User.setting_id == setting_id)
    if setting:
        try:
            setting = setting.one()
            s.close()
            return setting
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def del_user_alert(uid=None, setting_id=None):
    setting = s.query(Settings4User)
    if uid:
        setting = setting.filter(Settings4User.user_id == uid)
        setting = setting.filter(Settings4User.setting_id == setting_id)
    if setting:
        try:
            setting.delete()
            s.commit()
            s.close()
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def add_user_alert(uid=None, setting_id=None):
    try:
        s.add(Settings4User(setting_id=setting_id,user_id=uid))
        s.commit()
        s.close()
    except sqlalchemy.orm.exc.NoResultFound:
        s.close()
        pass
    
def ban_user(tgid=None):
    usuario = s.query(User)
    if tgid:
        usuario = usuario.filter(User.tgid == tgid)
    if usuario:
        try:
            usuario.delete()
            s.commit()
            s.close()
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
        
def get_url():
    setting = s.query(Settings)
    if setting:
        setting = setting.filter(Settings.setting_type == 'url')
        try:
            setting = setting.all()
            s.close()
            return setting
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def get_setting_alert(settings_user=None, kind=None):
    setting = s.query(Settings)
    if kind != 'all':
        
        if settings_user:
            setting = setting.filter(Settings.name == settings_user.setting_id)
            setting = setting.filter(Settings.setting_type == kind)
        else:
            setting = setting.filter(Settings.setting_type == kind)
    else:
        if settings_user:
            setting = setting.filter(Settings.name == settings_user.setting_id)
        
    if setting:
        try:
            setting = setting.all()
            s.close()
            return setting
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        
def get_setting_alert_left(settings_user=None, kind=None):
    setting = s.query(Settings)
    if kind != 'all':
        
        if settings_user:
            for i in settings_user:
                setting = setting.filter(Settings.name != i.setting_id)
            
            setting = setting.filter(Settings.setting_type == kind)
        else:
            setting = setting.filter(Settings.setting_type == kind)
    else:
        if settings_user:
            for i in settings_user:
                setting = setting.filter(Settings.name != i.setting_id)
        
    if setting:
        try:
            setting = setting.all()
            s.close()
            return setting
        except sqlalchemy.orm.exc.NoResultFound:
            s.close()
            pass
        




def add_user(name, lang=None, class_list=None, level=None, guild_name=None, guild_tag=None, castle=None, attack=None, defence=None, arroba=None, tgid=None, tgname=None):
    if not guild_name:        
        if guild_tag:
            guild = get_guild(tag=guild_tag)
            if guild:
                guild_name = guild.name
            else:
                guild_name = 'Unknown Guild'
        else:
            guild_name = 'Unknown Guild'
    if class_list:
        if len(class_list) == 2:
            s.add(User(name=name, lang=None, level=level, class1=class_list[0], class2=class_list[1], is_subcommander=0, guild_id=guild_name, attack=attack, defence=defence, castle=castle, arroba=arroba, tgid=tgid, tgname=tgname))
        else:
            s.add(User(name=name, lang=None, level=level, class1=class_list[0],  is_subcommander=0, guild_id=guild_name, attack=attack, defence=defence, castle=castle, arroba=arroba, tgid=tgid, tgname=tgname))
    else:
        s.add(User(name=name, lang=None, level=level, is_subcommander=0, guild_id=guild_name, attack=attack, defence=defence, castle=castle, arroba=arroba, tgid=tgid, tgname=tgname))
    s.commit()
    s.close()

def update_user(user, lang=None, class_list=None, level=None, guild_name=None, guild_tag=None, castle=None, attack=None, defence=None, arroba=None, tgid=None, tgname=None):
    if class_list:
        user.class1 = class_list[0]
        if len(class_list) == 2:
            user.class2 = class_list[1]
    if level:
        user.level = level
    if lang:
        user.lang = lang
    if guild_name:
        user.guild_id = guild_name
    elif guild_tag:
        g = get_guild(tag=guild_tag)
        if g:
            user.guild_id = g.name
        else:
            user.guild_id = 'Unknown Guild'
    else:
        user.guild_id = 'Unknown Guild'
    if castle:
        user.castle = castle
    if attack:
        user.attack = attack
    if defence:
        user.defence = defence
    if arroba:
        user.arroba = arroba
    if tgid:
        user.tgid = tgid    
    if tgname:
        user.tgname = tgname
    s.add(user)
    s.commit()
    s.close()

def add_or_update_user(name, lang=None, class_list=None, level=None, attack=None, defence=None, guild_tag=None, guild_name=None, castle=None, arroba=None, tgid=None, tgname=None):
    try:
        u = s.query(User).filter(User.name == name).one()
        s.close()
        if u.tgid == None or u.tgid == tgid or tgid == None:
            update_user(u, lang=None, class_list=class_list,level=level, attack=attack, defence=defence, guild_tag=guild_tag, guild_name=guild_name, castle=castle, arroba=arroba, tgid=tgid, tgname=tgname)
        else:
            print('User with name {} tried to log in with diferent tgids {} {}'.format(u.name, u.tgid, tgid))
    except sqlalchemy.orm.exc.NoResultFound:
        if tgid:
            try:
                u = s.query(User).filter(User.tgid == tgid).one()
                s.close()
                print('User with uid {} tried to send a new Me'.format(tgid))
                return
            except sqlalchemy.orm.exc.NoResultFound:
                pass
        # u = s.query(User).filter(User.name == name).one()
        add_user(name, lang=None, class_list=class_list,level=level, attack=attack, defence=defence, guild_tag=guild_tag, guild_name=guild_name, castle=castle, arroba=arroba, tgid=tgid, tgname=tgname)
        
# Orders


###########################################
#        Fill some default data           #
###########################################

def init_res():
    qry = open(os.path.join(DB_LOCATION, 'settings.sql'),'r').read()
    conn = sqlite3.connect(os.path.join(DB_LOCATION, DB_FILENAME) )
    c = conn.cursor()
    try:
       
        c.executescript(qry)
        conn.commit()
    except:
        c.rollback() #Rollback the changes on error
    finally:
        c.close()
        conn.close()
        

if db_empty: 
    init_res()
else:
    init_res()
 
    
    
