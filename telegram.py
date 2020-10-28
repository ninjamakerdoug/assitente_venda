# -*- coding: utf-8 -*-

import json
from Chatbot import Chatbot
import telepot
from datetime import datetime
from time import strftime
import time

telegram = telepot.Bot("cole seu token aqui")
bot = Chatbot("bot")


def pegaHorario():
    horaAtual = datetime.now().time().hour
    minutoAtual = datetime.now().time().minute
    segundoAtual = datetime.now().time().second

    if (horaAtual == 23) and (minutoAtual == 20):
        return True    


def recebendoMsg(msg):        
    def enviaMensagem(txt):
        chatID = msg['chat']['id']
        telegram.sendMessage(chatID,txt)


    mensagem = msg['text'].lower()
    chatID = msg['chat']['id']
    tipoMsg, tipoChat, chatID = telepot.glance(msg)
        
    if mensagem == 'ia':
        url = teste
        telegram.sendPhoto(chatID, url)
        pass

    elif mensagem.find('/start') >= 0:
        nome = msg['chat']['first_name']
        telegram.sendMessage(chatID,'Olá {}')
        pass

    else:
        frase = bot.escuta(frase=mensagem)
        if frase == 'meu id':
            resp = str(chatID)

        else:
            chatID = str(chatID)
            with open('autorizados.txt','r') as autorizados:
                auto = autorizados.read()
                if chatID in auto:
                    resp = bot.pensa(frase)
                    pass

            try:
                bot.fala(resp)
                #telegram.sendMessage(chatID,'{} disse {}'.format(nome,frase))
                telegram.sendMessage(chatID,resp)
                #telegram.sendMessage(numero do celular,auto[chatID]+' '+resp)   #manda todas as mensagens para o numero
            except:# KeyError:
                pass


telegram.message_loop(recebendoMsg)

while True:
    pass




