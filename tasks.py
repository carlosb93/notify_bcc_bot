import time
import sys
import logging
import requests
from datetime import datetime
from urllib.parse import urlparse
import db_handler as db
import logging
import asyncio
import threading
from flask import Flask, request, Response
from config import TOKEN, REQUEST_KWARGS, API_TOKEN

app = Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', methods=['GET'])
def home():
    return "<h1>API Telegram Bot</h1><p>This site is a prototype API for telegram bot notifications for BCC.</p>"

@app.route('/newalert', methods=['POST'])
def update_msg():
    headers= request.headers
    if not headers.get('Authorization'):
        return Response('Debe enviar los headers requeridos',400)
    else:
        if headers.get('Authorization') == 'Bearer {}'.format(API_TOKEN):

            try:
                type = request.form.get('type')
                bank = request.form.get('bank')
                phone = request.form.get('phone')
                text = request.form.get('text')
                if db.user_exists(phone=phone):
                    db.add_msg(type=type,phone=phone,text=text,bank=bank)
                    mensaje = '''
                              <h1>Alerta enviada</h1>
                              <h1>The Tipo value is: {}</h1>
                              <h1>The Banco value is: {}</h1>
                              <h1>The Telefono value is: {}</h1>
                              <h1>The Texto value is: {}</h1>'''.format(type,bank,phone,text)

                    return Response(mensaje,200)
                else:
                    return Response('El usuario con telefono: {} no existe en la BD'.format(phone),201)
            except:
                return Response('Error',500)
        else:
            return Response('El token es invalido',400)

 
app.run()


                        

