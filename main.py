import os
import smtplib
from email.message import EmailMessage
from playwright.sync_api import sync_playwright
import time
import threading
from flask import Flask

# Variables de entorno
EMAIL_ADDRESS = os.environ.get("GMAIL_USER")
EMAIL_PASSWORD = os.environ.get("GMAIL_PASS")
TO_EMAIL = os.environ.get("ALERT_EMAIL")
PRENOTAMI_USER = os.environ.get("PRENOTAMI_USER")
PRENOTAMI_PASS = os.environ.get("PRENOTAMI_PASS")

app = Flask(__name__)

def enviar_alerta():
    msg = EmailMessage()
    msg.set_content("¡Hay turnos disponibles para Ricostruzione Cittadinanza en Prenotami!")
    msg['Subject'] = "🚨 Turno disponible en Prenotami"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def revisar_turnos():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://prenotami.esteri.it/")
        page.click("text=Accedi")
        page.fill("#login-email", PRENOTAMI_USER)
        page.fill("#login-password", PRENOTAMI_PASS)
        page.click("button[type=submit]")
        page.wait_for_timeout(3000)

        page.goto("https://prenotami.esteri.it/Services/Booking/224")
        page.wait_for_timeout(3000)

        texto_pagina = page.content()
        if any(msg in texto_pagina for msg in [
            "Stante l'elevata richiesta",
            "All appointments for this service are currently booked",
            "Please check again tomorrow"
        ]):
            print("No hay turnos disponibles.")
        else:
            print("¡Hay turnos disponibles!")
            enviar_alerta()

        browser.close()

def tarea_periodica():
    while True:
        print("🔁 Revisión iniciada")
        try:
            revisar_turnos()
        except Exception as e:
            print(f"⚠️ Error durante la ejecución: {e}")
        print("⏳ Esperando 17 minutos para la próxima revisión...")
        time.sleep(17 * 60)

@app.route("/")
def home():
    return "El servicio está corriendo."

if __name__ == "__main__":
    # Lanzar la tarea periódica en un hilo aparte
    hilo = threading.Thread(target=tarea_periodica, daemon=True)
    hilo.start()

    # Iniciar el servidor Flask en el puerto asignado por Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
