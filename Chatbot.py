
# -*- coding: utf-8 -*-
#Define uma clasee com várias funções, e tudo que estiver dentro da será executado quando chamarmos a funçao dentro da classe, desse exemplo; resposta()
#Comandos que serão executados quando chamar a função, captura a resposta e processa-a;


import webbrowser
import wikipedia
import requests
import numpy as np
import time
import json
import sys
import os
import subprocess as s
from time import strftime
from datetime import datetime
from BuscaWeb import BuscaWeb
from busca_web import busca_web
import random
import pyautogui as pi
from time import strftime
import time


class Chatbot():    
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json','r')
        except FileNotFoundError:        
            memoria = open(nome+'.json','w')
            memoria.write('[["Douglas","Bianca"],{"Oi":"Olá, qual o seu nome?"}]')
            memoria.close()
            memoria = open(nome+'.json','r')
        self.nome = nome
        self.conhecidos, self.frases = json.load(memoria)
        memoria.close()
        self.historico = [None,]
        
        
    def escuta(self,frase=None):
        if frase == None:
            frase = input('>: ')
        frase = str(frase)
        if 'executa ' in frase:
            return frase
        frase = frase.lower()
        return frase

    
    def pensa(self,frase):
        dataEhora = datetime.now()
        ano = str(dataEhora.year)
        mes = str(dataEhora.month)
        dia = str(dataEhora.day)
        hora = str(strftime('%H:%M'))

        def desligaBot():
            #Desativando o bot temporariamente
            if hora == '20:27':
                return True

        if desligaBot() == True:
            return 'Temporariamente desligado'        

        respostas = ['Pois não?','Em que posso ajudá- lo?','Pode falar...','Estou ouvindo','Eu...','E aí, o que manda?','Sim, estou aqui']
        ultimaFrase = self.historico[-1]

        ##############   analisando nomes e respondendo

        if frase == 'oi':
            return 'Olá, qual o seu nome?'
            
        elif ultimaFrase == 'Olá, qual o seu nome?':
            nome = self.pegaNome(frase)
            frase = self.respondeNome(nome)
            return frase

        ######################
            
        elif frase == 'adicionar ao cardapio' or frase == 'adicionar ao cardápio':
            return 'Digite o código do novo produto'
        elif ultimaFrase == 'Digite o código do novo produto':
            if frase in self.frases:
                self.codigo = frase
                return 'Este código já pertence a um produto, deseja alterá- lo?'
            else:
                self.codigo = frase
                return 'Digite o nome do produto'

        elif ultimaFrase == 'Digite o nome do produto':
            self.produto = frase
            return 'Qual o preço do produto? (Digite somente números inteiros)'

        elif ultimaFrase == 'Este código já pertence a um produto, deseja alterá- lo?':
            if frase == 's' or frase == 'sim':
                return 'Digite o nome do produto'
                #return 'Qual o preço do produto? (Digite somente números inteiros)'
            else:
                return 'Cadastro cancelado'
            
        elif ultimaFrase == 'Qual o preço do produto? (Digite somente números inteiros)':
            self.valor = frase
            return 'Confirma cadastro do produto?'

        elif ultimaFrase == 'Confirma cadastro do produto?':
            if frase == 's':
                self.frases[self.codigo] = str(self.produto+' '+self.valor)
                self.frases[self.produto] = str(self.produto+' '+self.valor)
                self.gravaMemoria()
                return 'Cadastro realizado com sucesso'
            else:
                return 'Cadastro cancelado'

        ############################nesta parte é onde ensinamos respostas ao chatbot#########################      
        elif frase == 'bot aprenda':
            return 'Qual a frase?'

        elif frase == 'registrar mesa':
            return 'Qual será o número da mesa?'

        elif ultimaFrase == 'Qual será o número da mesa?':
            if frase in self.frases and frase.isnumeric():
                return 'Esta mesa já está registrada, deseja alterá- la?'
            else:
                if frase.isnumeric(): 
                    self.chave = frase
                    return 'Confirma o registro da mesa?'
            	
        elif ultimaFrase == 'Esta mesa já está registrada, deseja alterá- la?' and frase == 's' or frase == 'sim':
            self.chave = frase
            return 'Confirma o registro da mesa?'

            
        elif ultimaFrase == 'Confirma o registro da mesa?' and frase == 's' or frase == 'sim':
            resp = 'vazio'
            self.frases[self.chave] = resp
            self.gravaMemoria()
            return 'Mesa registrada com sucesso'
	
        elif ultimaFrase == 'Confirma o registro da mesa?' or 'Esta mesa já está registrada, deseja alterá- la?' and frase == 'n' or frase == 'não':
            return 'Registro cancelado'

        elif ultimaFrase == 'Qual a frase?' and frase in self.frases:
            self.chave = frase
            return 'Esta frase já está cadastrada, deseja alterá-la?'

        elif ultimaFrase == 'Qual a frase?':
            self.chave = frase
            return 'Qual a resposta?'

        elif ultimaFrase == 'Esta frase já está cadastrada, deseja alterá-la?':
            if frase == 'sim' or frase == 's':
                return 'Qual a resposta?'
            else:
                return 'Aprendizado cancelado'

        elif ultimaFrase == 'Qual a resposta?':
            resp = frase
            self.frases[self.chave] = resp
            self.gravaMemoria()
            return 'Aprendido'
        
        #Fechando a conta  #####################################
        elif frase == 'fechar conta':
            return 'De qual mesa deseja fechar a conta?'

        elif ultimaFrase == 'De qual mesa deseja fechar a conta?':
            if frase.isnumeric and frase in self.frases:
                self.chave = frase
                if self.frases[frase] == 'vazio':
                    return 'Não ha ninguém nessa mesa'
                else:
                    return 'Confirma o fechamento?'

        elif ultimaFrase == 'Confirma o fechamento?':
            if frase == 'sim' or frase == 's':
                resp = 'vazio'
                self.frases[self.chave] = resp
                self.gravaMemoria()
                return 'Fechamento realizado com sucesso.'
            else:
                return 'Fechamento cancelado'
	

        #+++++++ CANCELA VENDAS ++++++++++
        elif frase == 'cancelar venda':
            return 'O número da mesa?'
        
        elif ultimaFrase == 'O número da mesa?':
            if frase in self.frases:
                if self.frases[frase] == 'vazio':
                    return 'Não ha ninguém nessa mesa'
                else:
                    self.chaveQuarto = frase
                    cortando = self.frases[frase].split() #cria uma lista com todos os valores da frase
                    cortando2 = str(cortando[-1].replace(',00',''))#pega o ultimo item da lista q foi cortada e substitui ",00" por "nada".
                    self.total = cortando2                
                    return 'Qual o ítem será cancelado?'

        elif ultimaFrase == 'Qual o ítem será cancelado?':
            if frase in self.frases and frase.isnumeric():
                self.item = frase
                corta = self.frases[frase].split()
                corta2 = str(corta[-1])
                self.valor = int(corta2)
                return 'Qual a quantidade?'
            else:
                return 'Este ítem não contém na lista'

        elif ultimaFrase == 'Qual a quantidade?':
            self.quantidade = frase
            if (self.quantidade).isnumeric():
                self.quantidade = int(self.quantidade)
                self.valorvenda = self.quantidade * self.valor
                self.total = int(self.total)
                self.total -= int(self.valorvenda)
                self.quantidade = str(self.quantidade)
                self.valor = str(self.valor)
                self.total = str(self.total)
                self.valorvenda = str(self.valorvenda)
                dataEhoraV = datetime.now()
                self.anoV = str(dataEhoraV.year)
                self.mesV = str(dataEhoraV.month)
                self.diaV = str(dataEhoraV.day)
                self.horaV = str(strftime('%H:%M'))
                self.frases[self.chaveQuarto] += ('\n'+'\n'+'Venda cancelada' + '\n' + 'Ítem: ' + self.item + '\n' + 'Valor por unidade: ' + 'R$ ' + self.valor + ',00' + '\n' +             'Quantidade: ' + self.quantidade + '\n' + 'Valor da venda: ' +
                                                  'R$ ' + self.valorvenda + ',00' + '\n' + 'Data e hora: ' +
                                                  self.diaV + '/' + self.mesV + '/' + self.anoV + ' > ' + self.horaV + '\n'+ '\n' + 'Total: R$ ' + self.total+',00').title()
                self.gravaMemoria()
                return 'Venda cancelada'
            else:
                return 'Valores informados inválidos'
    

        #+++++++ VENDAS ++++++     
        elif frase == 'venda':
            return 'Qual o número da mesa?'
        elif ultimaFrase == 'Qual o número da mesa?':
            if frase.isnumeric() and self.frases[frase] == 'vazio':
                return 'Não há ninguém nessa mesa'
            elif frase.isnumeric() and frase in self.frases:
                self.chaveQuarto = frase
                cortando = self.frases[frase].split()
                cortando2 = str(cortando[-1].replace(',00',''))
                self.total = cortando2
                return 'Qual o ítem?'
            else:
                if frase.isnumeric():
                    return 'Valores informados inválidos'

        #+++++++++
	
	#nesta parte é onde cadastramos pessoas nas mesas#######################
        elif frase == 'cadastrar':
            return 'Certo, digite o número da mesa.'

        elif ultimaFrase == 'Certo, digite o número da mesa.':
            if frase in self.frases:
                if self.frases[frase] == 'vazio':
                    self.chaveQuarto = frase
                    return 'Informe o nome do responsável pela mesa.'
                else:
                    self.chaveQuarto = frase
                    return 'Esta mesa já está ocupada, digite 1 para alterá- la ou 2 para vendas ou digite qualquer letra para cancelar'
            else:
                return 'Valores informados inválidos'

        elif ultimaFrase == 'Esta mesa já está ocupada, digite 1 para alterá- la ou 2 para vendas ou digite qualquer letra para cancelar' and frase == '1':
            return 'Informe o nome do responsável pela mesa.'
        elif ultimaFrase == 'Esta mesa já está ocupada, digite 1 para alterá- la ou 2 para vendas ou digite qualquer letra para cancelar' and frase == '2':
            return 'Qual o ítem?'

        #+++++++++
        elif ultimaFrase == 'Qual o ítem?':
            if frase in self.frases:
                corta = self.frases[frase].split()
                corta2 = str(corta[-1])
                corta3 = str(corta[0:-1])
                corta4 = corta3.replace("'","")
                corta5 = corta4.replace('[','')
                corta6 = corta5.replace(']','')
                corta7 = corta6.replace(',','')
                self.item = str(corta7)
                self.valor = int(corta2)
                return 'Quantidade?'
            else:
                return 'Este ítem não contém na lista'
    
        #####################                   #################
        elif ultimaFrase == 'Quantidade?':
                self.quantidade = frase
                if (self.quantidade).isnumeric():
                    self.quantidade = int(self.quantidade)
                    self.valorvenda = self.quantidade * self.valor             
                    self.total = int(self.total)
                    self.total += int(self.valorvenda)
                    self.quantidade = str(self.quantidade)
                    self.valor = str(self.valor)
                    self.total = str(self.total)
                    self.valorvenda = str(self.valorvenda)
                    dataEhoraV = datetime.now()
                    self.anoV = str(dataEhoraV.year)
                    self.mesV = str(dataEhoraV.month)
                    self.diaV = str(dataEhoraV.day)
                    self.horaV = str(strftime('%H:%M'))
                    self.frases[self.chaveQuarto] += ('\n'+'\n'+'Venda' + '\n' + 'Ítem: ' + self.item + '\n' + 'Valor por unidade: ' + 'R$ ' + self.valor + ',00' + '\n' + 'Quantidade: ' + self.quantidade + '\n' + 'Valor da venda: ' + 'R$ ' + self.valorvenda + ',00' + '\n' + 'Data e hora: ' + self.diaV + '/' + self.mesV + '/' + self.anoV + ' > ' + self.horaV + '\n'+ '\n' + 'Total: R$ ' + self.total+',00').title()        
                    return 'Confirma a venda?'
	
        ###########  
        elif ultimaFrase == 'Confirma a venda?':
            if frase == 's' or frase == 'sim':
                self.gravaMemoria()
                return 'Venda realizada com sucesso'
            else:
                return 'A venda foi cancelada'
        ############

        elif ultimaFrase == 'Informe o nome do responsável pela mesa.':
            self.chaveNome = frase
            return 'Deseja confirmar o cadastro? (Digite "s" ou "sim")'

        elif ultimaFrase == 'Deseja confirmar o cadastro? (Digite "s" ou "sim")':
            if frase == 's' or frase == 'sim':
                dataEhora = datetime.now()
                self.ano = str(dataEhora.year)
                self.mes = str(dataEhora.month)
                self.dia = str(dataEhora.day)
                self.hora = str(strftime('%H:%M'))
                self.item = ''
                self.quantidade = ''
                self.diaV = ''
                self.mesV = ''
                self.anoV = ''
                self.horaV = ''
                self.total = '0'
                self.frases[self.chaveQuarto] = ('Número da mesa: ' + self.chaveQuarto + '\n' + 'Responsável: ' + self.chaveNome + '.\n' + 'Data e hora do cadastro: ' + self.dia + '/' + self.mes + '/' + self.ano + ' > ' + self.hora + self.item +self.quantidade + self.diaV + self.mesV + self.anoV + self.horaV + '\n' + 'Total: ' + self.total).title()
                self.gravaMemoria()
                return 'Cadastro realizado com sucesso!'
            else:
                return 'Certo, o cadastro foi cancelado!'


        ### Conferir mesa ########################################
        elif frase == 'conferir mesa':
            return 'Certo, qual é a mesa?'
        elif ultimaFrase == 'Certo, qual é a mesa?':
            if frase.isnumeric() and frase in self.frases:
                return self.frases[frase]

        ###########################################     
        #Nesta parte, você pode programar ações para que o programe execute somente antes de chamá-lo pelo nome
        elif frase == 'bot':
            comandos = str(random.choice(respostas))
            return comandos

        elif ultimaFrase in respostas:
            if frase in self.frases:
                return self.frases[frase]

            elif frase == 'tchau':
                return 'tchau'
            
            else:            
                try:  #Nesta parte, se a frase digitada for uma equação numérica, o chatbot tentará resolve-la ##########
                    if ' x ' in frase:
                        frase = frase.replace(' x ','*')
                    resp = str(eval(frase))
                    return resp

                except:
                    #Caso nenhum processo anterior seja executado, o chatbot usará a api do google para te retornar uma resposta
                    #existem limitações
                    cb = BuscaWeb()
                    resultado = cb.start(frase)
                    chave = str(resultado[0])
            
                    if(chave == "nenhum resultado"):
                        if 'traduza para o inglês ' in frase:
                            frase = frase.replace('traduza para o inglês ','')
                            time.sleep(1)
                            pi.hotkey('shift','2')
                            pi.typewrite('ytranslatebot >> ' + frase)
                            pi.click(790, 416, button='left', duration=3)
                            time.sleep(1)
                            return 'pronto'
			#usa wikipedia para tentar encontrar uma resposta
                        elif 'quem é ' in frase:
                            frase2 = frase.replace('quem é ','')
                            frase3 = frase2.title()
                            
                            if ' De ' in frase3:
                                frase4 = frase3.replace(' De ',' de ')
                                frase5 = frase4.replace(' ','_')
                                novaChave = ('https://pt.wikipedia.org/wiki/'+frase5)
                                return novaChave
                            else:
                                frase4 = frase3.replace(' ','_')
                                novaChave = ('https://pt.wikipedia.org/wiki/'+frase4)
                                return novaChave

                        elif 'quem foi ' in frase:
                            frase2 = frase.replace('quem foi ','')
                            frase3 = frase2.title()

                            if ' De ' in frase3:
                                frase4 = frase3.replace(' De ',' de ')
                                frase5 = frase4.replace(' ','_')
                                novaChave = ('https://pt.wikipedia.org/wiki/'+frase5)
                                return novaChave
                            else:
                                frase4 = frase3.replace(' ','_')
                                novaChave = ('https://pt.wikipedia.org/wiki/'+frase4)
                                return novaChave


                        elif 'o que é ' in frase:
                            frase2 = frase.replace('o que é ','')
                            frase3 = frase2.replace(' ','_')
                            novaChave = ('https://pt.wikipedia.org/wiki/'+frase3)
                            return novaChave


                        #verificando se é uma música que deseja tocar, procurando no youtube ##################
                        elif 'tocar ' in frase:
                            frase = frase.replace('tocar ','')
                            try:
                                mixer.init()
                                mixer.music.load('/home/doug/Música/'+frase+'.mp3')
                                mixer.music.play()
                                return 'pronto'
                                
                            except:
                                return 'não encontrei nenhum audio ou música com esse nome'
			
			#retorna uma frase caso nada tenha sido encontrado
                        else:
                            respostas1 = ['Não encontrei nada em minhas fontes...','Desculpe, não achei nada relativo...','Acho que essa eu não vou conseguir te responder.',]
                            respostas2 = str(random.choice(respostas1))
                            return (respostas2)
                
                    else:   #retorna pesquisa do google
                        return(resultado[0])

        else:            
            #Nesta parte, se a frase digitada for uma equação numérica, o chatbot tentará resolve-la ##########
            try:
                if ' x ' in frase:
                    frase = frase.replace(' x ','*')
                resp = str(eval(frase))
                return resp
            except:
                if frase in self.frases:
                    return self.frases[frase]
                else:
                    return 'Comando não reconhecido'



    def pegaNome(self,nome):
        if 'o meu nome é ' in nome:
            nome = nome[500:]
        nome = nome.title()
        return nome


    def respondeNome(self,nome):
        if nome in self.conhecidos:
            frase = 'Oi '
        else:
            frase = 'Muito prazer '
            self.conhecidos.append(nome)
            self.gravaMemoria()
        return frase+nome


    def gravaMemoria(self):
        memoria = open(self.nome+'.json','w')
        json.dump([self.conhecidos,self.frases],memoria)
        memoria.close()
                       
		
    def fala(self,frase):
        if 'executa ' in frase:
            plataforma = sys.platform
            comando = frase.replace('executa ','')
            if 'win' in plataforma:
                os.startfile(comando)
            if 'linux' in plataforma:
                try:
                    s.Popen(comando)
                except FileNotFoundError:
                    s.Popen(['xdg-open',comando])
            
        else:
            pass
            #print(frase)
        self.historico.append(frase)
       
