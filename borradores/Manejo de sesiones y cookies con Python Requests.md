# Manejo de Sesiones y Cookies con Python Requests

## Situación actual (no listar, solo intro).

En la actualidad, el uso de sesiones al "scrapear" un sitio web es una función poco utilizada debido a que se desconoce que existe o se desconocen las posibles consecuencias de no utilizarla.

En la gran mayoría de casos, sobre todo cuando se realizan pruebas de scraping a sitios web, no es necesario utilizar una sesión. Sin embargo, el uso de las sesiones debería formar parte de la configuración basica de cualquier scraper o crawler que pretendamos crear de manera sería y profesional.

## ¿Qué es una sesión?

La sesión tiende a ser un conjunto de variables que los servidores web acostumbrán a almacenar a través de las cookies del navegador y que los mismos utilizán para reconocer a los usuarios que visitan los sitios web. 

## El uso de cookies para almacenar la sesión.

Las cookies son la forma preferida por los desarrolladores de servidores web (backend) para almacenar la sesión de un usuario en su sitio, debido a que las cookies son almacenadas en el navegador de forma persistente, se les puede colocar una fecha de vigencia y otros datos utiles.

Es por esto que debemos almacenar las cookies como si fuesemos un navegador por usarlas después y así hacer creer al servidor que continuamos navegando donde lo dejamos. Esto es util cuando utilizamos multiples funciones en diversas partes de nuestro código que requieren de ingresar al mismo sitio web.

## Ejemplo práctico: Ingresar a un sitio con usuario y contraseña.

Librerias necesarias:
- `requests`
- `BeautifulSoup4`
- `lxml`

Instalar aquí:
```
pip install requests BeautifulSoup4 lxml
```

Para este caso veremos un ejemplo del uso de sesión para scrapear los datos de un perfil de Twitter ingresando con usuario y contraseña.

Lo primero es manejar la sesión en una variable.

```python
import requests # Importar requests

ses = requests.session() # Instanciar una variable de requests para manejar la sesión
```

Para ingresar a Twitter con requests es necesario que los servidores de Twitter crean que somos un teléfono antiguo (tipo Nokia s40), esto lo logremos con un User Agent. Para conocer mas sobre esto te enviamos a leer nuestro post sobre los User Agent:

```python
# User Agent para hacer creer al servidor web que somos un Teléfono Nokia s40 usando Opera Mini para que nos devuelva una versión sin Javascript de Twitter.
headers = {
    'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10'
}
```

Lo siguiente es ingresar al sitio web de inicio de Twitter para que el servidor nos envíe por primera vez las cookies de sesión como si un usuario estuviese llegando por primera vez. Utilizaremos la variable de sesión que creamos con anterioridad, el método `GET` y también los `headers` que continen el User Agent para poder ingresa a Twitter.

```python
url_login = 'https://mobile.twitter.com/session/new'  # URL del "Login" de Twitter móvil.
resp = ses.get(url_home, headers=headers) # Enviar solicitud

code = resp.status_code # Código HTTP de respuesta
if code != 200:
    print(f'Error al cargar Twitter: {code}')
    return
print('Todo Ok, se cargó Twitter')
```

Lo siguiente es capturar un Token que Twitter envía a esta página de acceso, utilizaremos BeautifulSoup para parsear la respuesta en HTML y poder obtener el token de un input oculto.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(resp.text, 'lxml')
authenticity_token = soup.select_one('input[name="authenticity_token"]').get("value", None)
if authenticity_token is None:
    print(f'Error al obtener Token')
    return
print(f'Token para acceso a Twitter: {authenticity_token}')
```

Lo siguiente es enviar el formulario con los datos de acceso y otras variables que maneja la versión móvil de Twitter para ingresar al sitio. Utilizaremos el método `POST`, y la URL de acceso a Twitter para lograrlo.

```python
url_login_post = 'https://mobile.twitter.com/sessions'  # URL que dispará Twitter al presionar el botón de "Login"
email = 'eecuart4@gmail.com' # Tu email o usuario de Twitter.
password = 'E48863e4e#' # Tu contraseña de Twitter
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
headers['origin'] = 'https://mobile.twitter.com',
headers['referer'] = 'https://mobile.twitter.com/login'

resp = ses.post(url_login_post, headers=headers, data=data)  # Enviar solicitud

code = resp.status_code  # Código HTTP de respuesta
if code != 200:
    print(f'Error al cargar Twitter: {code}')
    return
print("Ingresamos a Twitter!")
```

Para este punto ya nos encontramos en nuestro Feed de Twitts. Vamos a obternerlos para comprobar el funcionamiento de la sesión. Para esto utilizaremos la librería `BeautifulSoup` y `lxml` para parsear la respuesta en HTML de Twitter. Utilizamos sintaxis de CSS Selectors para consultar en el contenido HTML, en caso de no conocer esta sintaxis te recomendamos ver nuestro post Uso de CSS Selectors para extraer información de HTML en BeautifulSoup, Selenium y Scrapy.

```python
soup = BeautifulSoup(resp.text, 'lxml') # Parsea el HTML
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
```

Ahora veremos el uso de las cookies para almacenar la sesión y poder utilizar después en nuestro programa. Para esto utilizaremos la libreria
`pickle` para almacenar las cookies en un archivo en nuestro equipo, y despues poder cargarlas nuevamente.

```python
import pickle # Importamos pickle

cookies = ses.cookies  # Obtenemos las cookies que se generaron en nuestra sesión
f = open('cookies-twitter.cki', 'wb')  # Creamos un archivo y le damos un nombre para almacenar las cookies
pickle.dump(cookies, f) # Guardamos las cookies
```

Ahora digamos que la función termina y ahora abrimos otra donde también requerimos utilizar la sesión, en este ejemplo ver los Tweets de otra cuenta, para esto recuperaremos las cookies que ya contienen la sesión.

```python
f = open('cookies-twitter.cki', 'rb')  # Archivo de cookies
cookies = pickle.load(f) # Cargar cookies
ses = requests.session() # Instanciar una variable de requests para manejar la sesión
ses.cookies = cookies # Colocar cookies en sesión de requests
```

Utilizaremos el perfil de Bill Gates.

```python
# User Agent para hacer creer al servidor web que somos un Teléfono Nokia s40 usando Opera Mini para que nos devuelva una versión sin Javascript de Twitter.
headers = {
    'User-Agent': 'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10',
    'referer': 'https://mobile.twitter.com/'
}

url_perfil = 'https://mobile.twitter.com/BillGates'  # URL del Perfil de BillGates.
resp = ses.get(url_perfil, headers=headers)  # Enviar solicitud

code = resp.status_code  # Código HTTP de respuesta
if code != 200:
    print(f'Error al cargar el perfil: {code}')
    return
print('Todo Ok, se cargó el perfil de Bill Gates')
```

Ahora mostraremos sus Tweets.

```python
soup = BeautifulSoup(resp.text, 'lxml')  # Parsea el HTML
tweets = soup.select('.timeline > .tweet')  # Buscar los tweets con sintaxis de CSS Selectors.

user = soup.select_one('.profile-details .fullname').get_text()
image = soup.select_one('.profile-details .avatar img').get('src', '')
print(f'Username: {user}')
print(f'Image: {image}')

idx = 1
for tweet in tweets:  # Recorremos cada post y obtener el tweet.
    timestamp = tweet.select_one('.timestamp a').get_text()
    desc = tweet.select_one('.tweet-text .dir-ltr').get_text()
    print(f'Tweet #{idx}:')
    print(f'Timestamp: {timestamp}')
    print(f'Description: \n{desc}')
    idx += 1
```

## En resumen.

Para generalizar los pasos:
- Creamos una variable de sesión con `requests.session()`.
- Ingresamos al Home sitio web para que nos envie las cookies de sesión.
- Las guardamos con ayuda de `pickle` en un archivo.
- Cuando sea necesario utilizarlas, las cargamos nuevamente con pickle.
- Y finalmente se las colocamos a la variable de sesión.

## Ideas finales.

El uso de sesiones en sitios que requieren acceso es lo más comun en lo que podemos utilizarlas. Pero también puede usarse para demostrar un comportamiento mas "humano" al scrapear un sitio web y evitar ser baneado.

Espero esta guía te haya servido para manejar tus sesiones en los proyectos en los que estes trabajando, un saludo!