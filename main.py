import os
import time
import random
import asyncio
from playwright.async_api import async_playwright
import requests

# Variables desde entorno
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# URL base
BASE_URL = "https://prenotami.esteri.it"

async def enviar_mensaje_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("No hay configuración de Telegram.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        resp = requests.post(url, data=data)
        if resp.status_code == 200:
            print("Mensaje enviado por Telegram.")
        else:
            print(f"Error enviando Telegram: {resp.text}")
    except Exception as e:
        print(f"Exception enviando Telegram: {e}")

async def check_turnos():
    print("Iniciando Playwright para revisar turnos...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless para no mostrar ventana
        context = await browser.new_context()
        page = await context.new_page()

        # Ir a la página principal
        await page.goto(BASE_URL)

        # Click en botón "Accedi" para login
        await page.click("text=Accedi")

        # Completar formulario login
        await page.fill('input[name="username"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button[type="submit"]')

        # Esperar que cargue la página principal del usuario (quizás check URL o elemento)
        await page.wait_for_load_state("networkidle")

        # Navegar a sección “Ricostruzione cittadinanza”
        # (Ajustar selector exacto según página real)
        await page.goto(f"{BASE_URL}/prenotami/ricostruzione")

        # Esperar que cargue el contenido
        await page.wait_for_load_state("networkidle")

        # Buscar el botón "Prenota" o "Reservar" que habilita turnos
        # IMPORTANTE: ajustá el selector según lo que veas en el HTML real
        try:
            boton = await page.query_selector("button:has-text('Prenota')")
            if boton:
                habilitado = await boton.is_enabled()
                if habilitado:
                    msg = "¡Turno disponible para reconstrucción de ciudadanía! 🟢"
                    print(msg)
                    await enviar_mensaje_telegram(msg)
                else:
                    print("No hay turnos disponibles ahora.")
            else:
                print("No se encontró el botón de reservar.")
        except Exception as e:
            print(f"Error chequeando botón: {e}")

        await browser.close()

async def main():
    while True:
        try:
            await check_turnos()
        except Exception as e:
            print(f"Error en check_turnos: {e}")

        wait_time = random.randint(8*60, 20*60)
        print(f"Esperando {wait_time // 60} minutos para el próximo chequeo...")
        time.sleep(wait_time)

if __name__ == "__main__":
    asyncio.run(main())
