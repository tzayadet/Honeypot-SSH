# SSH Honeypot Lab
Prototipo de honeypot SSH en Python basado en Paramiko. Registra intentos de autenticación y solicitudes de ejecución para estudiar actividad en un entorno de laboratorio.

## Alcance y seguridad

Este proyecto es experimental y **no es un servidor SSH de acceso remoto**.

- Registra el nombre de usuario y la IP de origen de los intentos de autenticación.
- Nunca almacena, imprime ni registra el valor de las contraseñas recibidas.
- Rechaza las solicitudes de terminal interactiva y shell.
- Registra las solicitudes SSH `exec`, pero no ejecuta los comandos recibidos.
- No proporciona aislamiento del sistema operativo: ejecútalo igualmente en una VM o red de laboratorio aislada.

No lo expongas directamente a Internet ni lo ejecutes en un servidor de producción. Los nombres de usuario y comandos solicitados pueden contener datos personales o sensibles; protege y elimina los logs conforme a tu política de retención.

## Requisitos

- Python 3.11+
- Paramiko 3.5 o superior, versión principal 4.x no incluida.

```bash
python -m pip install -r requirements.txt
```

## Ejecución local

Por defecto escucha únicamente en loopback:

```bash
python honeypot.py
```

En Windows PowerShell:

```powershell
$env:HP_HOST = "127.0.0.1"
$env:HP_PORT = "2222"
python honeypot.py
```

Variables disponibles:

- `HP_HOST`: dirección de escucha. Por defecto, `127.0.0.1`.
- `HP_PORT`: puerto TCP. Por defecto, `2222`.
- `HP_LOG_FILE`: fichero de eventos. Por defecto, `hp.log`.

Para pruebas desde otra máquina, cambia la dirección de escucha solo dentro de una red aislada y restringe el acceso mediante firewall.

## Docker

La imagen configura la escucha en todas las interfaces **dentro del contenedor**. No publiques el puerto en una interfaz pública del host.

```bash
docker build -t ssh-honeypot .
docker run --rm --name ssh-honeypot \
  -p 127.0.0.1:2222:2222 \
  -v "$PWD/logs:/app/logs" \
  -e HP_LOG_FILE=/app/logs/hp.log \
  ssh-honeypot
```

## Estructura

- `honeypot.py`: servidor SSH de laboratorio.
- `requirements.txt`: dependencias Python.
- `Dockerfile`: imagen de contenedor no privilegiada.

## Limitaciones

No es un honeypot de alta interacción ni un entorno de ejecución aislado. No implementa shell falso, persistencia de sesiones, rotación de logs ni almacenamiento estructurado. La clave de host se genera al iniciar el proceso, por lo que cambia entre ejecuciones.

## Pruebas

Las pruebas verifican que no se registran contraseñas, que no se ofrecen terminales interactivas y que las solicitudes `exec` se registran sin ejecutar comandos.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub Actions ejecuta estas comprobaciones en cada push y pull request.

## Licencia

Consulta [LICENSE](LICENSE).
