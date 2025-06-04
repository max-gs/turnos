import os
import smtplib
from email.message import EmailMessage
from playwright.sync_api import sync_playwright

# Credenciales y destinatario desde variables de entorno
EMAIL_ADDRESS = os.environ.get("GMAIL_USER")
EMAIL_PASSWORD = os.environ.get("GMAIL_PASS")
TO_EMAIL = os.environ.get("ALERT_EMAIL")
PRENOTAMI_USER = os.environ.get("PRENOTAMI_USER")
PRENOTAMI_PASS = os.environ.get("PRENOTAMI_PASS")

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

        # Iniciar sesión
        page.click("text=Accedi")
        page.fill("#login-email", PRENOTAMI_USER)
        page.fill("#login-password", PRENOTAMI_PASS)
        page.click("button[type=submit]")
        page.wait_for_timeout(3000)  # esperar un poco

        # Ir a /Services/Booking/224
        page.goto("https://prenotami.esteri.it/Services/Booking/224")
        page.wait_for_timeout(3000)

        # Verificar si hay turnos disponibles
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

if __name__ == "__main__":
    revisar_turnos()
