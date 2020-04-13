import requests # Importar requests
from bs4 import BeautifulSoup # Importar BeautifulSoup4
import pickle  # Importamos pickle


def without_cookies():
    ses = requests.session() # Instanciar una variable de requests para manejar la sesión

    # User Agent para hacer creer al servidor web que somos un Teléfono Nokia s40 usando Opera Mini para que nos devuelva una versión sin Javascript de Twitter.
    headers = {
        'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10'
    }

    url_login = 'https://mobile.twitter.com/session/new'  # URL del "Login" de Twitter móvil.
    resp = ses.get(url_login, headers=headers) # Enviar solicitud

    code = resp.status_code # Código HTTP de respuesta
    if code != 200:
        print(f'Error al cargar Twitter: {code}')
        return
    print('Todo Ok, se cargó Twitter')

    soup = BeautifulSoup(resp.text, 'lxml')
    # authenticity_token = soup.find(attrs={'name': 'authenticity_token'}).get("value", None)
    authenticity_token = soup.select_one('input[name="authenticity_token"]').get("value", None)
    if authenticity_token is None:
        print(f'Error al obtener Token')
        return
    print(f'Token para acceso a Twitter: {authenticity_token}')

    url_login_post = 'https://mobile.twitter.com/sessions' # URL que dispará Twitter al presionar el botón de "Login"
    email = 'eecuart4@gmail.com'  # Tu email o usuario de Twitter.
    password = 'E48863e4e#'  # Tu contraseña de Twitter
    # FormData enviado por a través de POST para efectuar el acceso
    data = {
        'authenticity_token': authenticity_token,
        'session[username_or_email]': email,
        'session[password]': password,
        'remember_me': 1,
        'wfa': 1,
        'commit': 'Log in',
        'ui_metrics': ''
    }
    headers['origin'] = 'https://mobile.twitter.com'
    headers['referer'] = 'https://mobile.twitter.com/login'

    resp = ses.post(url_login_post, headers=headers, data=data)  # Enviar solicitud

    code = resp.status_code  # Código HTTP de respuesta
    if code != 200:
        print(f'Error al cargar Twitter: {code}')
        return
    print("Ingresamos a Twitter!")

    soup = BeautifulSoup(resp.text, 'lxml')  # Parsea el HTML
    tweets = soup.select('.timeline > .tweet')  # Buscar los tweets con sintaxis de CSS Selectors.
    idx = 1
    for tweet in tweets:  # Recorremos cada post y obtener el usuario, imagen y tweet.
        user = tweet.select_one('.fullname').get_text()
        image = tweet.select_one('.avatar img').get('src', '')
        desc = tweet.select_one('div.dir-ltr').get_text()
        print(f'Tweet #{idx}:')
        print(f'Username: {user}')
        print(f'Image: {image}')
        print(f'Description: \n{desc}')
        idx += 1

    cookies = ses.cookies  # Obtenemos las cookies que se generaron en nuestra sesión
    f = open('cookies-twitter.cki', 'wb')  # Creamos un archivo y le damos un nombre para almacenar las cookies
    pickle.dump(cookies, f) # Guardamos las cookies


def with_cookies():
    f = open('cookies-twitter.cki', 'rb')  # Archivo de cookies
    cookies = pickle.load(f) # Cargar cookies
    ses = requests.session() # Instanciar una variable de requests para manejar la sesión
    ses.cookies = cookies # Colocar cookies en sesión de requests

    # User Agent para hacer creer al servidor web que somos un Teléfono Nokia s40 usando Opera Mini para que nos devuelva una versión sin Javascript de Twitter.
    headers = {
        'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10',
        'referer': 'https://mobile.twitter.com/'
    }

    url_perfil = 'https://mobile.twitter.com/BillGates'  # URL del Perfil de BillGates.
    resp = ses.get(url_perfil, headers=headers)  # Enviar solicitud

    code = resp.status_code  # Código HTTP de respuesta
    if code != 200:
        print(f'Error al cargar Twitter: {code}')
        return
    print('Todo Ok, se cargó el perfil de Bill Gates')

    soup = BeautifulSoup(resp.text, 'lxml')  # Parsea el HTML
    tweets = soup.select('.timeline > .tweet')  # Buscar los tweets con sintaxis de CSS Selectors.

    user = soup.select_one('.profile-details .fullname').get_text()
    image = soup.select_one('.profile-details .avatar img').get('src', '')
    print(f'Username: {user}')
    print(f'Image: {image}')

    idx = 1
    for tweet in tweets:  # Recorremos cada post y obtener el tweet y el timestamp.
        timestamp = tweet.select_one('.timestamp a').get_text()
        desc = tweet.select_one('.tweet-text .dir-ltr').get_text()
        print(f'Tweet #{idx}:')
        print(f'Timestamp: {timestamp}')
        print(f'Description: \n{desc}')
        idx += 1


if __name__ == '__main__':
    without_cookies()
    # with_cookies()