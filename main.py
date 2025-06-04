import os
import time
import random
import asyncio
from playwright.async_api import async_playwright
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL_LOGIN = "https://prenotami.esteri.it/"

async def revisar_turnos():
    print("Iniciando revisión de turnos...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(URL_LOGIN)
            await page.click('text=Accedi')

            # Iniciar sesión
            await page.fill('input[name="email"]', USERNAME)
            await page.fill('input[name="password"]', PASSWORD)
            await page.click('button[type="submit"]')

            await page.wait_for_timeout(3000)

            # Navegar a turnos
            await page.goto("https://prenotami.esteri.it/Services")
            await page.wait_for_timeout(3000)

            # Buscar el servicio específico
            servicios = await page.locator("div.card-body").all()
            encontrado = False

            for servicio in servicios:
                titulo = await servicio.locator("h5").inner_text()
                if "Ricostruzione cittadinanza" in titulo:
                    encontrado = True
                    botones = await servicio.locator("a.btn").all()
                    for boton in botones:
                        texto = await boton.inner_text()
                        if "Prenota" in texto:
                            print("🟢 ¡Turno disponible!")
                            await enviar_telegram("🟢 ¡Hay turno disponible para Ricostruzione cittadinanza!")
                            break
                    break

            if not encontrado:
                print("⚠️ No se encontró el servicio de Ricostruzione cittadinanza.")

        except Exception as e:
            print(f"❌ Error: {e}")

        await browser.close()

async def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    try:
        response = requests.post(url, data=data)
        print("📨 Mensaje enviado a Telegram")
    except Exception as e:
        print(f"❌ Error al enviar Telegram: {e}")

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(revisar_turnos())
        except Exception as e:
            print(f"❌ Error general: {e}")
        espera = random.randint(500, 1200)  # espera entre 8 y 20 minutos
        print(f"⏳ Esperando {espera // 60} minutos...\n")
        time.sleep(espera)
