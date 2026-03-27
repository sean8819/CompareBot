import datetime
import os
import random
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv
from telegram import Update

DEFAULT_QUERY = "woman,models,real,beauty,pose"
DEFAULT_OUTPUT_PATH = "tmp/downloads/beauty_of_the_day.png"


async def handle_beauty(update: Update):
    path = Path(DEFAULT_OUTPUT_PATH)

    if not path.exists():
        result = download_beauty_image()
        if result is None:
            print("Errore nel download dell'immagine")
            return
        path = Path(result)
        print("non esiste ancora, la scarico")

    elif datetime.datetime.fromtimestamp(path.stat().st_ctime).day == date.today().day:
        print("già scaricata, invio l'immagine")

    else:
        result = download_beauty_image()
        if result is None:
            print("Errore nel download dell'immagine")
            return
        path = Path(result)
        print("scarico l'immagine e la invio")

    with path.open("rb") as image_file:
        message = update.message
        if message is None or message.text is None:
            return
        await message.reply_photo(photo=image_file)


def download_beauty_image(
    query: str = DEFAULT_QUERY,
    output_path: str = DEFAULT_OUTPUT_PATH,
) -> str | None:
    load_dotenv()

    api_key = os.getenv("PIXABAY_TOKEN")
    if not api_key:
        print("❌ PIXABAY_TOKEN non configurato")
        return None

    risultati = cerca_immagini_pixabay(query, api_key)
    if not risultati:
        print("❌ Nessuna immagine trovata")
        return None

    link = random.choice(risultati)
    if scarica_risorsa(link, output_path):
        return output_path

    return None


def cerca_immagini_pixabay(tag, api_key):
    url = "https://pixabay.com/api/"
    params = {
        "key": api_key,
        "q": tag,
        "image_type": "photo",
        "safesearch": "false",
        "per_page": 150,
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code == 200:
        dati = response.json()
        return [foto["webformatURL"] for foto in dati.get("hits", [])]

    print(f"Errore Pixabay: {response.status_code}")
    return []


def scarica_risorsa(url, percorso_salvataggio):
    try:
        cartella = os.path.dirname(percorso_salvataggio)
        if cartella and not os.path.exists(cartella):
            os.makedirs(cartella)

        with requests.get(url, stream=True, timeout=15) as r:
            r.raise_for_status()

            with open(percorso_salvataggio, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"✅ Scaricato con successo: {percorso_salvataggio}")
            return True

    except requests.RequestException as e:
        print(f"❌ Errore nel download: {e}")
        return False
