# Turnos Prenotami - Revisión automática

Este proyecto es un script en Python que utiliza Playwright para conectarse a [prenotami.esteri.it](https://prenotami.esteri.it/), hacer login y revisar la disponibilidad de turnos para "reconstrucción de ciudadanía". Cuando hay turnos disponibles, te envía una notificación por Telegram.

## Requisitos

- Python 3.9+ instalado  
- Cuenta en prenotami.esteri.it  
- Bot de Telegram y chat ID para recibir notificaciones (opcional pero recomendado)  


## Instalación

Clonar el repositorio con `git clone https://github.com/max-gs/turnos.git` 

y entrar en la carpeta con `cd turnos`. C

rear un entorno virtual (opcional pero recomendado) con `python -m venv venv` 

y activarlo (`source venv/bin/activate` en Linux/macOS o `venv\Scripts\activate` en Windows). 

Instalar las dependencias con `pip install -r requirements.txt`.

Luego instalar los navegadores para Playwright (solo la primera vez): `playwright install`


## Configuración

Crear un archivo `.env` en la raíz del proyecto con las variables de entorno:

```
  USERNAME=tu_usuario_en_prenotami
  PASSWORD=tu_contraseña_en_prenotami
  TELEGRAM_TOKEN=token_de_tu_bot_telegram
  TELEGRAM_CHAT_ID=tu_chat_id_telegram
```

Si no querés usar Telegram, podés dejar vacíos `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID` y el script solo mostrará mensajes en consola.

## Uso

Ejecutar el script con `python main.py`. El script revisará la disponibilidad de turnos en intervalos aleatorios entre 8 y 20 minutos para simular un comportamiento humano y te avisará por Telegram cuando haya turnos disponibles.

## Despliegue en Render (opcional)

Podés automatizar la ejecución creando un **Cron Job** en Render configurado para ejecutarse cada 10 minutos (o el intervalo que prefieras). Subí tu repositorio a GitHub y conéctalo a Render. Configurá las variables de entorno en Render igual que en tu archivo `.env`. Así el script se ejecutará automáticamente en la nube y te avisará cuando detecte turnos disponibles.

## Seguridad

No subas tu archivo `.env` con credenciales reales al repositorio. Usá un `.env.example` para compartir configuración sin datos sensibles.

## Contribuciones

¡Bienvenidas! Abrí un issue o PR si querés mejorar algo.

## Licencia
MIT License

Copialo así nomás a tu archivo README.md y debería verse perfecto. ¿Querés que te ayude a hacer el commit directo desde acá?
