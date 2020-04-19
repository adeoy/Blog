import requests # Importar requests
from bs4 import BeautifulSoup # Importar BeautifulSoup4


def get_response_by_user_agent(user_agent):
    headers = { 'User-Agent': user_agent}

    url_twitter = 'https://twitter.com/billgates'
    resp = requests.get(url_twitter, headers=headers)  # Enviar solicitud

    code = resp.status_code  # Código HTTP de respuesta
    if code != 200:
        print(f'Error al cargar Twitter: {code}')
        return
    soup = BeautifulSoup(resp.text, 'lxml')  # Parsea el HTML
    print(soup.prettify())



def main():
    # Windows 10 con Google Chrome
    user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    # Android 9 con Google Chrome
    user_agent_smartphone = 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'
    # Nokia 5310 con UC Browser
    user_agent_old_phone = 'Nokia5310XpressMusic_CMCC/2.0 (10.10) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; Nokia5310XpressMusic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile'

    get_response_by_user_agent(user_agent_old_phone)

if __name__ == '__main__':
    main()