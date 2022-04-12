import db_handler as db
import random
import time
import datetime
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

langs = {
    'English' : {
        'adjustSettings': "Adjust your settings",
        'AllianceCreated': 'Alliance info created!',
        'AllianceUpdated': 'Alliance info updated!',
        'AllianceRosterUpdate': 'Alliance roster updated!',
        'AllianceUnknown': 'Alliance not found!',
        'AtkListUpdated': 'Guild atklist updated!',
        'BattleNotif': 'Battle is coming. Equip your weapon and get your orders!',
        'ChoseTop': "Choose the top stats",
        'DefListUpdated': 'Guild deflist updated!',
        'EncounterSent': 'Thanks for sending monsters.',
        'EncounterTooOld': 'Sorry, your encounter is too old (has already finished).',
        'EmptyMessage': 'Write something, dude',
        'ErrorParsing': 'Error Parsing your message',
        'OrderAcepted': 'Your order is ready. Clic "send all" button in a private chat.',
        'GuildUnknown': 'Guild not found!\nForward your /guild TAG first',
        'GuildCreated': 'Guild info created!',
        'GuildUpdated': 'Guild info updated!',
        'LocationKnown': "Already known location. Thanks!!!",
        'LocNotFound': "Location not found",
        'LocDis': "Location disabled",
        'NewLocation': "That's a new one. Thanks!!!",
        'NoGuild': 'Error 404 Guild not found',
        'NoPriviledges': 'You do not have privileges to go there.',
        'NoTargetError': 'Set target first',
        'NoTierError': 'Select a tier for the order',
        'NoOrders': " hasn't set orders yet",
        'NothingFound': 'Nothing found yet',
        'NoSpam': 'Please avoid spamming me!',
        'OrderNotif': ' just set the orders. Check the ⚜️ Order button',
        'OrderSaved': 'Order Saved',
        'PlayerUpdated': 'Player info updated!',
        'RosterUpdated': 'Guild roster updated!',
        'ReportOK': 'Thanks for sending report',
        'SettingOverview': "Setting Overview",
        'UserNotRegister': "Hello i am a fast alert Bot.\nSend me your cellphone number ☎️ to suscribe to alerts.\n\n /subscribe 58467341",
        'UnknownCWMsg': 'ChatWars Message not recognized!',
        'Stock': 'Generating deposit msg!',
        'Welcome': "Welcome back",
        'WelcomeAdmin': "Welcome Admin",
        'WelcomeCommander': "Welcome Commander",
        'AddedAlert': "✔️ Alert enabled!!!",
        'RemoveAlert': "❌ Alert disabled!!!",
        'RemovePhone': "❌ Deleted!!!",
        'Done': "✔️ Done!!!",
        'Subscribed': "You are now subscribed!!!",
        '5ta': "⚠️⚠️ Modul in 5ta & 42 ⚠️⚠️!!!",
        'Conf_alerts': "⚠️⚠️ You should setup your alerts ⚠️⚠️!!!",
        'start_scrap': "⚠️ Start scratching!!!",
        'WrongNumber': "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n Your cellphone number must be 8-10  digits long and no string or symbols!!!"
    },
    'Spanish' : {
        'adjustSettings': "Ajusta tus configuraciones",
        'AllianceCreated': 'Información de Alianza creada!',
        'AllianceUpdated': 'Información de Alianza actualizada!',
        'AllianceRosterUpdate': 'Lista de la Alianza actualizada!',
        'AllianceUnknown': 'Alianza no encontrada!',
        'AtkListUpdated': 'Se actualizó la lista atk del gremio!',
        'BattleNotif': 'La batalla se acerca. Equipa tu arma y recibe tus órdenes!',
        'ChoseTop': "Elige las mejores estadísticas",
        'DefListUpdated': 'Lista de def del gremio actualizado!',
        'EncounterSent': 'Gracias por enviar monstruos.',
        'EncounterTooOld': 'Lo sentimos, tu encuentro es demasiado viejo (ya ha terminado).',
        'EmptyMessage': 'Escribe algo, amigo',
        'ErrorParsing': 'Error al analizar tu mensaje',
        'OrderAcepted': 'Tu orden está lista. Haga clic en el botón "enviar todo" en un chat privado.',
        'GuildUnknown': '¡No se encontró el gremio!\nEnvía primero tu ETIQUETA /guild',
        'GuildCreated': 'Información del gremio creada!',
        'GuildUpdated': 'Información del gremio actualizada!',
        'LocationKnown': "Ubicación ya conocida. Gracias!!!",
        'LocNotFound': "Ubicación no encontrada",
        'LocDis': "Ubicación deshabilitada",
        'NewLocation': "Esa es una nueva. Gracias!!!",
        'NoGuild': 'Error 404 Gremio no encontrado',
        'NoPriviledges': 'No tienes privilegios para ir allí.',
        'NoTargetError': 'Establecer objetivo primero',
        'NoTierError': 'Seleccione un Tier para la orden',
        'NoOrders': " Aún no se han establecido pedidos",
        'NothingFound': 'Aún no se ha encontrado nada.',
        'NoSpam': 'Por favor evite enviarme spam!',
        'OrderNotif': ' Ordenes establecidas. Verifique el botón ⚜️ Order',
        'OrderSaved': 'Orden Guardada',
        'PlayerUpdated': 'Información del jugador Actualizada!',
        'RosterUpdated': 'Lista del gremio actualizada!',
        'ReportOK': 'Gracias por enviar el reporte',
        'SettingOverview': "Descripción general de la configuración",
        'UserNotRegister': "Hola soy un Bot de alerta rápida.\nEnvíame tu número ☎️ para suscribirte a las alertas\n\n /subscribe 58467341",
        'UnknownCWMsg': 'Mensaje de ChatWars no reconocido!',
        'Stock': 'Generando mensaje de deposito!',
        'Welcome': "Bienvenido de vuelta",
        'WelcomeAdmin': "Bienvenido Admin",
        'WelcomeCommander': "Bienvenido Commander",
        'AddedAlert': "✔️ Alerta Habilitada!!!",
        'RemoveAlert': "❌ Alerta Deshabilitada!!!",
        'RemovePhone': "❌ Eliminado!!!",
        'Done': "✔️ Hecho!!!",
        'Subscribed': "Usted esta suscrito!!!",
        '5ta': "⚠️⚠️ Módulo en 5ta y 42 ⚠️⚠️!!!",
        'Conf_alerts': "⚠️⚠️ Usted debería configurar sus alertas ⚠️⚠️!!!",
        'start_scrap': "⚠️ Start scratching!!!",
        'WrongNumber': "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n Su número debe ser de 8-10 dígitos y sin caractéres o símbolos!!!"
    }
}
def days_between(max, min):
    min = min/1000           #removing milli seconds
    max = max/1000

    min = datetime.datetime.fromtimestamp(min)
    max = datetime.datetime.fromtimestamp(max)

    timeStampObj = (max-min).days

    return timeStampObj

def get_all_users_admin(test=None):
    res = "👥 Listado de Usuarios: \n\n"
    users = db.get_all_users()
    if users:
        for u in users:
            pagado = days_between(time.time() ,u.status_date)
            if pagado > 30:
                db.disable_user_subscription(tgid=u.tgid)
                res += '- {} | @{} |{}\n /ban /enable_{}\n'.format(u.name, u.arroba, u.phone, u.tgid)
            else:
                if u.status:
                    res += '- {} | @{} |{}\n /ban /disable_{}\n'.format(u.name, u.arroba, u.phone, u.tgid)
                else:
                    res += '- {} | @{} |{} \n /ban /enable_{}\n'.format(u.name, u.arroba, u.phone, u.tgid)
    return res

def get_user_alert_status_prod(tgid=None):
    res = "🔊 Estas son sus alertas activas:\n\n"
    # Settings4User todos los settings activos por el usuario
    settings_user = db.get_user_alerts(uid=tgid)
    if settings_user:
        for a in settings_user:
            settings = db.get_setting_alert(settings_user=a,kind='alert')
            if settings:
                for i in settings:
                    res += '- {} \n'.format(i.name)
        res += '\n Seleccione sobre que desea ser notificado. \n'
        return res
    else:
        res += '----No tiene alertas activas---- \n\n'
        res += 'Seleccione sobre que desea ser notificado. \n'
        return res



def get_user_alert_status_url(tgid=None):
    res = "⚙️ Configuración:\n\n"
    # Settings4User todos los settings activos por el usuario
    settings_user = db.get_user_alerts(uid=tgid)
    if settings_user:
        for a in settings_user:
            settings = db.get_setting_alert(settings_user=a,kind='url')
            if settings:
                for i in settings:
                    res += '- {} \n'.format(i.name)
        res +='Eliminar teléfono del sistema /removeme \n'
        res += '\n Seleccione sobre que desea ser notificado. \n'
        
        return res
    else:
        res += '----Alertas inactivas---- \n\n'
        res +='Eliminar teléfono del sistema /removeme \n'
        res += 'Seleccione sobre que desea ser notificado. \n'
        return res

def get_user_notifications(phone=None):
    res = "🔊 historial de mensajes:\n\n"
    # Settings4User todos los settings activos por el usuario
    msg_user = db.get_msg(phone=phone)
    if msg_user:
        if msg_user.count() > 5:
            splitedSize = 5
            a_splited = [msg_user[x:x+splitedSize] for x in range(0, len(msg_user), splitedSize)]
            for a in a_splited:
                for b in a:
                    res += '-{}-\n- {}\n{}\n\n'.format(datetime.datetime.fromtimestamp(b.created_at / 1e3),b.bank,b.text.replace('\\n','\n'))
                    res += '----------------------------\n'
                    return res
        else:
            for b in msg_user:
                res += '-{}-\n- {}\n{}\n\n'.format(datetime.datetime.fromtimestamp(b.created_at / 1e3),b.bank,b.text.replace('\\n','\n'))
                res += '----------------------------\n'
                return res
    else:
        res += '----No hay mensajes recientes---- \n\n'
        return res


def get_alert_options_btn_url(tgid=None):
    settings_user = db.get_user_alerts(uid=tgid)
    btn = InlineKeyboardMarkup(row_width=2)
    if settings_user:
        for sets_u in settings_user:
            settings = db.get_setting_alert(settings_user=sets_u, kind='url')

            if settings:
                for sets in settings:
                    if sets.name == sets_u.setting_id:
                        btn.insert(InlineKeyboardButton("❌ "+sets.name, callback_data=sets.name))
                    break
        settings = db.get_setting_alert_left(settings_user=settings_user, kind='url')
        if settings:
            for sets in settings:
                if sets.name == sets_u.setting_id:
                    break
                else:
                    btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))
    else:
        settings = db.get_setting_alert(kind='url')
        if settings:
            for sets in settings:
                btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))


    return btn

def get_alert_options_btn_prod(tgid=None):
    settings_user = db.get_user_alerts(uid=tgid)
    btn = InlineKeyboardMarkup(row_width=2)
    if settings_user:
        for sets_u in settings_user:
            settings = db.get_setting_alert(settings_user=sets_u, kind='alert')

            if settings:
                for sets in settings:
                    if sets.name == sets_u.setting_id:
                        btn.insert(InlineKeyboardButton("❌ "+sets.name, callback_data=sets.name))
                    break
        settings = db.get_setting_alert_left(settings_user=settings_user, kind='alert')
        if settings:
            for sets in settings:
                if sets.name == sets_u.setting_id:
                    break
                else:
                    btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))
    else:
        settings = db.get_setting_alert(kind='alert')
        if settings:
            for sets in settings:
                btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))

    return btn

def get_registration_btn(tgid=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(
    KeyboardButton('Verificar Cuenta ☎️', request_contact=True)
).add(
    KeyboardButton('Cancelar')
)
    

    
    return markup

def get_registration_text(tgid=None):
    res = "Confirme para poder verificar su usuario:\n\n"
    return res





def get_help():
    res = '<code> creador:</code>  @mr_charlie93 \n\n'
    res += '<b>comandos útiles:</b>\n <code>/help, /removeme, /back </code>'
    return res


def get_static_message(message_key, ulang='Spanish'):
    if not ulang in langs.keys():
        ulang = 'Spanish'
    if message_key in langs[ulang].keys():
        return langs[ulang][message_key]
    return message_key


def get_settings_menu(message):
    res = "⚙️ " + get_static_message('adjustSettings', ulang='Spanish') + "\n\n"
    res +="Eliminar teléfono del sistema /removeme"
    return res





