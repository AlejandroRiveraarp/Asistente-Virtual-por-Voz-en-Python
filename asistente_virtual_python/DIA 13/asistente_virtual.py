from dataclasses import replace

import pyttsx3

import pywhatkit
import yfinance
import pyjokes
import webbrowser
import datetime
import wikipedia
import speech_recognition as sr
from playsound import playsound
import os


# escuchar nuestro microfono y devolver el audio comotexto

def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()
    # configurar el microfono
    with sr.Microphone(device_index=None) as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # infomrar que comenzo la grabacion
        print("ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-CL")

            # prueba de que pudo ingresar
            print(" Dijiste: " + pedido)

            # devolver a pedido
            return pedido

        #en caso que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("ups, no entendi")

            # devolver error
            return "sigo esperando"
        # en caso de no devoler el pedido
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print("ups, no hay servicio")

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:
            # prueba de que no comprendio el audio
            print("ups, algo ha salido mal")

            # devolver error
            return "sigo esperando"

# funcion para el asistente pueda ser escuchado
def hablar(mensaje):

    # enceder el motor de pyttsx3
    os.system("say ''") # colocar sonido
    engine = pyttsx3.init()

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# informar el dia de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear una variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario con nombres de los dias
    calendario = {0: 'Lunes',
                 1: 'Martes',
                 2: 'Miérocles',
                 3: 'Jueves',
                 4: 'Viernes',
                 5: 'Sabado',
                 6: 'Domingo'}

    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

# informar que hora es
def pedir_hora():

    # crear una variable con datos de las horas
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # decir la hora
    hablar(hora)
pedir_hora()

# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour >20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'


    #decir saludo
    hablar(f'{momento}, Soy tu asistente, en que te puedo ayudar?')

# funcion central del asistente
def pedir_cosas():
    #activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    #loop central
    while comenzar:

        #activar el micro y guardar el pedido en un strring
        pedido  = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador google' in pedido:
            hablar('Claro estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        elif 'busca por favor' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('buscando en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar(resultado)
            continue

        elif 'busca en internet' in pedido:
            hablar('ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yfinance.Tickers(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar("Perdon pero no la he encontrado")
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break






pedir_cosas()






