# Turnos Prenotami - Revisión automática

Este proyecto es un script en Python que utiliza Playwright para conectarse a [prenotami.esteri.it](https://prenotami.esteri.it/), hacer login y revisar la disponibilidad de turnos para "reconstrucción de ciudadanía". Cuando hay turnos disponibles, te envía una notificación por Telegram.

---

## Requisitos

- Python 3.9+ instalado
- Cuenta en prenotami.esteri.it
- Bot de Telegram y chat ID para recibir notificaciones (opcional pero recomendado)

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/max-gs/turnos.git
cd turnos

2. Crear un entorno virtual (opcional pero recomendado):

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


3. Instalar dependencias:

pip install -r requirements.txt


4. Instalar navegadores para Playwright (solo la primera vez):

playwright install

---

## Configuración

Crear un archivo .env en la raíz con las siguientes variables:

USERNAME=tu_usuario_en_prenotami
PASSWORD=tu_contraseña_en_prenotami
TELEGRAM_TOKEN=token_de_tu_bot_telegram
TELEGRAM_CHAT_ID=tu_chat_id_telegram

Si no querés usar Telegram, podés dejar vacíos los valores TELEGRAM_TOKEN y TELEGRAM_CHAT_ID y el script solo imprimirá mensajes en consola.

---

## Uso
Ejecutar el script:

python main.py
El script hará chequeos periódicos en intervalos aleatorios (entre 8 y 20 minutos) para no parecer un bot y notificará cuando haya disponibilidad de turnos.

---

## Despliegue en Render (opcional)
Para automatizar y dejar corriendo el script en la nube:

Crear un nuevo Cron Job en Render configurado para ejecutarse cada 10 minutos (o el intervalo que prefieras).

Subir este repositorio a GitHub y conectarlo a Render.

Configurar las variables de entorno en Render (igual que en .env).

Render ejecutará el script automáticamente y te avisará si detecta turnos disponibles.

---

## Seguridad
No subir el archivo .env con credenciales reales al repositorio.

Usar .env.example como plantilla para compartir configuración sin datos sensibles.

---

## Contribuciones
Bienvenidas! Abrí un issue o PR si querés mejorar algo.
