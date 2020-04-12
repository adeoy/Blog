# El uso de User Agents al Scrapear datos

## Situación actual (no listar, solo intro).

Usar User Agent es una práctica poco utilizada o utilizada sin pensar por muchos desarrolladores de scrapers y crawlers. Pero es importante conocer que utilizar el User Agent correcto puede ayudar y facilitar el la tarea de scraping de muchos sitios web.

## ¿Qué es un User Agent?

El User Agent o Agente de Usuario es una cadena de texto que el cliente envía a traves de los headers de una solicitud, y sirve como identificador del tipo de dispositivo, sistema operativo y navegador que estamos utilizando. Esta información le dice al servidor que, por ejemplo, usamos un navegador Google Chrome 80 y equipo con Windows 10. Y por o tanto el servidor prepara una respuesta pensada en esa clase de dispositivo.

No es la misma respuesta que nos envía Facebook, Twitter o Google cuando ingresamos con un smarthphone con Android o iOS que cuando ingresamos con un equipo con Windows, Mac OS o Linux. Y esto lo sabe a través del User Agent.

Debido a que el User Agent es una cadena en texto plano es fácil manipularlo y de esta manera "engañar" al servidor web para que crea que lo visitamos de un dipositivo diferente.

## ¿Porqué no usar User Agent es mala idea?

No configurar un User Agent en nuestras solicitudes hará que nuestras herramientas utilicen uno por defecto que en muchas ocasiones es uno que anuncia nuestra precencia como un Bot, lo cual en muchos sitios no esta permitido y por lo tanto es posible que nos baneen.

Lo recomendado es siempre utilizar un User Agent popular, para que pueda pasar desapercido. El siguiente sitio web contiene una enorme base de datos de User Agent, pero en mi recomendación es mas sencillo utilizar el de nuestro navegador favorito y para tu caso particular lo puedes ver aqui:

```
TU USER AGENT
```

## Ejemplo práctico.

Veamos por ejemplo la respuesta que nos devuelve Twitter al ingresar con el User Agent de un navegador Google Chrome con Windows 10.

```
GOOGLE CHROME WITH WINDOWS 10
```

Como podemos ver en el contenido de la respuesta en HTML, Twitter detecta que somos un navegador moderno pero no podemos ejecutar Javascript, esto es porque requests solo obtiene el HTML tal y como lo envía el servidor, y el navegador se encarga de ejecutar Javascript y realizar las solicitudes necesarias para cargar el contenido.

Para solucionar esto utilizaremos un User Agent en el que emulemos un viejo teléfono en el que no se soportaba Javascript. Tomemos en cuenta que no todos los sitios web tienen esta función, pero Twitter, Facebook y Google la tienen debido a la popularidad de las plataformas y a que su infraestructura paso por todas estas tecnologias.

Ahora probemos con este navegador Opera Mini en un teléfono Nokia s40.

```
OPERA MINI WITH NOKIA S40
```

Ahora si, Twitter nos devolvió un formulario de acceso en el cual podemos emular nuestra siguiente solicitud.

Te recomendamos ver nuestro post Manejo de Sesiones y Cookies con Python Requests en el que utilizamos este User Agent asi como sesiones para ingresar a Twitter y realizar scraping para obtener los twitts de usuarios.
