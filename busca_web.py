# -*-coding:utf8;-*-
# Junior Obom
# 11/09/2019


import urllib.request
from unicodedata import normalize

import urllib.parse
import urllib.request
import wikipedia


class busca_web(object):
    def __init__(self):
        pass

    def gerarUrl(self, chave, site):  # Recebe uma palavara ou frase chave e a prepara para busca
        texto_busca = chave.replace(" ",
                                    "-")  # No lugar dos espaços vamos colocar sinais de adição "-" pois é assim que essa url de busca deve ser montada

        url = str(site + texto_busca)
        return url

    def busca(self, url):  # Faz uma busca com a URL (link) e devolve o código HTML da página
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
                   'Accept-Charset': 'ascii'}

        req = urllib.request.Request(url, headers=headers)
        retorno = str(urllib.request.urlopen(req).read()).encode("utf-8")
        retorno = retorno.decode("unicode-escape")
        # Os passo de "encode" e "decode" acima garatem que caracteres acentuados possam ser reconhecidos

        return retorno.replace("\n", " ")  # Retirada das quebras de linha (opcional)

    def buscaAscii(self, url):  # Faz uma busca com a URL (link) e devolve o código HTML da página
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
                   'Accept-Charset': 'ascii'}

        req = urllib.request.Request(url, headers=headers)
        retorno = urllib.request.urlopen(req).read()
        retorno = str(retorno.decode('utf8','ignore'))
        # Os passo de "encode" e "decode" acima garatem que caracteres acentuados possam ser reconhecidos

        return retorno.replace("\n", " ")  # Retirada das quebras de linha (opcional)

    def remover_acentos(self,txt, codif='utf-8'):
        txt=txt.encode('utf-8') # Para usar o "decode" em uma str é preciso fazer isso antes
        semAce = str(normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore'))   
        semAce=semAce[2:len(semAce)-1] # Tirando os dois primeiros caracteres para que a string seja correspondente com a original
        print(semAce) 
        return semAce

    def responder(self, html):
        cod_tipos = ["""class="sinonimo">""",
                     """<p class="text-justify">""",
                      """<em class='translation'>""", """<h2 class="bNg8Rb">Descrição</h2><span>""" ,"""class="Z0LcW">""",
            """data-dobid="dfn"><span>""",
            """class="vk_gy vk_sh">""",
                      
            """class="ILfuVd yZ8quc c3biWd">""", # Essa ordem é importante
            """class="ILfuVd yZ8quc">""",

  

            """class="center">""",
            """class="floatnone">""",
            """class="image">""",

            """div class="im_message_text">""",
            """dir="auto">""",

            """div class="im_message_text" dir="auto">""",
            """class="im_message_text">""",
            """dir="auto">""",
            
            """div class="tagline">""",
            
            """class="tagline">""",
            ]
            
        tipos = ["sinônimo",
                 "significado",
                 "tradução","quem é ou data de",
            "significado",
            "que dia é",
            "descobrimento 2",
            "descobriento 1",
                
            "dolar",
            "calcular",
            "tradução"]

        ct2 = " "
        resposta = []

        tipo_corte = None
        for ct in cod_tipos:
            if ct in html:
                ct2 = ct
                break

        if ct2 == " ":
            resposta = ["nenhum resultado"]
            return resposta

        try:
            i = 0
            while i != html.count(ct2):
                html = html[(html.index(ct2) + len(ct2)):len(html)]  # Tudo que vier antes
                resposta_temporaria = html[0:(html.index("<"))].replace("                 ", "")

                resposta.append(resposta_temporaria)
                print(resposta_temporaria)

                i += 1

        finally:  # Caso haja algum possível erro na busca

            return resposta

    def start(self, busca, site, busca_padrao = True):
        try:
            cb = busca_web()
            url = cb.gerarUrl((cb.remover_acentos(busca)), site)

            if(busca_padrao):
                resultado = cb.responder(cb.busca(url))
            else:
                resultado = cb.responder(cb.buscaAscii(url))

            if resultado == "nenhum resultado":
                return resultado, False
            else:
                resultado = str(resultado)
                return resultado, True
        except:
            resultado = "não foi possivel concluir a busca"
            return resultado, False


