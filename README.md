# SSH Honeypot

Prototipo de honeypot SSH en Python basado en Paramiko. Registra intentos de autenticación y solicitudes de ejecución para estudiar actividad en un entorno controlado.

## Alcance y seguridad

Este proyecto es experimental. El manejador actual acepta autenticación con contraseña para registrar intentos y no implementa un protocolo completo de aislamiento. No lo expongas directamente a Internet ni lo ejecutes en un servidor de producción. Utiliza una VM aislada, limita el acceso de red y evita almacenar contraseñas reales en los logs.

## Requisitos

- Python 3.11+
- Paramiko

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```bash
HP_PORT=2222 python honeypot.py
```

En Windows PowerShell:

```powershell
$env:HP_PORT = "2222"
python honeypot.py
```

Los eventos se escriben en `hp.log` en el directorio de ejecución.

## Estructura

- `honeypot.py`: servidor SSH de laboratorio.
- `requirements.txt`: dependencias.
- `Dockerfile`: imagen de contenedor.

## Limitaciones

No es un honeypot endurecido ni un servicio SSH real. Revisa y sanea los registros, porque el código registra los valores de contraseña recibidos. No reutilices credenciales reales en las pruebas.

## Licencia

Consulta [LICENSE](LICENSE).
