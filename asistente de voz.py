import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import webbrowser
import pyjokes
import wikipedia
import datetime
import pyaudio
import locale


# opciones de voz / idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# Escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # almacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print('Ya puedes hablar')

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-ar")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprendio el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("ups, no entendi")

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:

            # prueba de que no comprendio el audio
            print("ups, algo ha salido mal")

            # devolver error
            return "sigo esperando"


# funcion para que el asistente sea escuchado
def hablar(mensaje):
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de hoy

# toma la locación del sistema, en este caso me dará los resultados en Español
locale.setlocale(locale.LC_TIME, '')


def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.datetime.now()

    # crear variable para el día de la semana
    dia_semana = dia.strftime('%A')

    hablar(f'Hoy es {dia_semana}')



def pedir_hora():

    # crear una variable con los datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento querido Facundo son las {hora.hour} horas ' \
           f'con {hora.minute} minutos y {hora.second} segundos.'
    print(hora)

    # decir la hora

    hablar(hora)


def saludo_inicial():

    # Crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen Día'
    else:
        momento = 'Buenas Tardes'

    # Decir saludo inicial
    hablar(f'{momento}, soy Cristiano Ronaldo, tu asistente personal. En que te puedo ayudar bro?')


# funcion central del asistente
def pedir_cosas():

    # activar saludos inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube. Aguantá un cachito')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, en un toque estaras googleando pavadas')
            webbrowser.open('https://www.google.com')
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Por supuesto gilipollas, abriendo wiki')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('ok, pero sera la ultima vez ya estoy cansada')
            pedido = pedido.replace('busca en internet','')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado en la gran web')
            continue
        elif 'que día es hoy' in pedido:
            pedir_dia()
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'reproducir' in pedido:
            hablar('uf, que bajón eres. ok, sino queda otra.')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera [accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón pero no la he encontrado, sorry')
                continue
        elif 'adiós' in pedido:
            hablar("yo me tomo el palo amigo. nos vimos")
            break

pedir_cosas()
