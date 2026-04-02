<div align="center">

<img src="img/logo.png" alt="CompareBot Logo" width="350">

# Compare-Bot

**IL TUO BOT DI FIDUCIA PER FARE IL MONELLO CON I VIDEO!**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Powered-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](#cicd)

Mini progetto realizzato per il corso di **Quality Development UNICT DMI 2025/2026 - Docente Borzì S.**

Bot Telegram per il download di contenuti multimediali (video e audio) da piattaforme come YouTube, Instagram, TikTok e molte altre.

</div>

---

## Indice

- [Panoramica](#panoramica)
- [Comandi](#comandi)
- [Funzionalità](#funzionalità)
  - [Download multimediale](#download-multimediale)
  - [Beauty of the Day](#beauty-of-the-day)
  - [Internazionalizzazione (i18n)](#internazionalizzazione-i18n)
- [Architettura](#architettura)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Variabili d'ambiente](#variabili-dambiente)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Team](#team)

---

## Panoramica

CompareBot è un bot Telegram asincrono che permette di scaricare contenuti multimediali da oltre 1000 piattaforme supportate da yt-dlp. Offre supporto multilingua (italiano e inglese), un sistema di pulsanti inline per la selezione del formato e della risoluzione, e una funzionalità giornaliera di ispirazione visiva tramite l'API Pixabay.

---

## Comandi

| Comando | Descrizione                                                             |
| :--- |:------------------------------------------------------------------------|
| `/start` | Messaggio di benvenuto personalizzato con il nome dell'utente           |
| `/download <url>` | Scarica audio (MP3) o video (MP4) da un URL supportato                  |
| `/beauty` | Invia la "beauty of the day" — un'immagine casuale di una bella ragazza |
| `/service` | Mostra l'elenco dei servizi disponibili                                 |
| `/about` | Informazioni sul progetto e sul team                                    |
| `/lang <it\|en>` | Cambia la lingua dell'interfaccia del bot                               |

---

## Funzionalità

### Download multimediale

Il comando `/download <url>` avvia il flusso di download:

1. **Validazione URL** — l'URL viene verificato tramite la libreria `validators`
2. **Scelta del formato** — l'utente seleziona tramite pulsanti inline:
   - **Audio (MP3)** — estrae l'audio alla migliore qualita disponibile
   - **Video (MP4)** — presenta un secondo menù per la scelta della risoluzione
3. **Scelta della risoluzione** (solo video) — 360p, 480p o 720p
4. **Download** — il file viene scaricato in modo asincrono tramite yt-dlp con merge audio/video via ffmpeg
5. **Invio e pulizia** — il file viene inviato all'utente su Telegram e rimosso automaticamente dal server

Vincoli:
- Limite dimensione file Telegram: **50 MB**
- I file temporanei vengono salvati con prefisso UUID univoco

### Beauty of the Day

Il comando `/beauty` invia un'immagine casuale dalla Pixabay API:

- Query di ricerca: `woman,models,real,beauty,pose`
- **Cache giornaliera**: l'immagine viene scaricata una sola volta al giorno
- **Lock di concorrenza**: previene download multipli simultanei
- 150 immagini per chiamata API per massimizzare la varietà

### Internazionalizzazione (i18n)

Il bot supporta **italiano** e **inglese**:

- I file di traduzione si trovano in `lang/it.json` e `lang/en.json`
- La preferenza linguistica dell'utente viene salvata in `users.json`
- Gli ID utente vengono hashati con **SHA-256 + salt** prima dello storage per proteggere la privacy
- Lingua di default: **inglese**
- Fallback: se una chiave di traduzione manca, viene restituita la chiave stessa

---

## Architettura

```
CompareBot/
├── main.py                  # Entry point — polling con 256 update concorrenti
├── src/
│   ├── handlers.py          # Gestione comandi (/start, /download, /about, /service, /beauty, /lang)
│   ├── buttons.py           # Menu inline, selezione formato/risoluzione, logica di download
│   ├── messages.py          # Recupero stringhe localizzate
│   ├── logo.py              # Logo ASCII art
│   └── core/
│       ├── downloader.py    # Wrapper yt-dlp + ffmpeg per estrazione audio/video
│       ├── beauty.py        # Integrazione API Pixabay con cache giornaliera
│       └── i18n.py          # Sistema di internazionalizzazione e gestione preferenze utente
├── lang/
│   ├── en.json              # Traduzioni inglese
│   └── it.json              # Traduzioni italiano
├── tests/
│   ├── test_handlers.py     # Test dei command handler
│   ├── test_buttons.py      # Test pulsanti inline e logica download
│   ├── test_messages.py     # Test recupero messaggi
│   └── core/
│       ├── test_downloader.py   # Test funzionalita downloader
│       ├── test_beauty.py       # Test feature beauty
│       └── test_i18n.py         # Test sistema i18n
├── img/
│   └── logo.png             # Logo del progetto
├── .github/workflows/
│   ├── lint.yml             # Pipeline di linting
│   └── test.yml             # Pipeline di testing
├── requirements.txt         # Dipendenze di produzione
├── requirements_dev.txt     # Dipendenze di sviluppo
├── pyproject.toml           # Configurazione tool (isort, mypy, pytest, coverage)
├── .flake8                  # Configurazione Flake8
├── .pylintrc                # Configurazione Pylint
├── .env.example             # Template variabili d'ambiente
└── localTest.sh             # Script per test locali
```

---

## Tech Stack

### Dipendenze di produzione

| Pacchetto | Ruolo |
| :--- | :--- |
| `python-telegram-bot[job-queue]` | Framework bot Telegram asincrono con job queue |
| `yt-dlp` | Downloader universale per video/audio (1000+ piattaforme) |
| `python-dotenv` | Gestione variabili d'ambiente da file `.env` |
| `requests` | Chiamate HTTP (API Pixabay) |
| `validators` | Validazione URL |
| **ffmpeg** (sistema) | Encoding e merge audio/video — richiesto nel PATH |

### Dipendenze di sviluppo

| Pacchetto | Ruolo |
| :--- | :--- |
| `pytest` + `pytest-asyncio` | Framework di testing con supporto async |
| `pytest-mock` + `pytest-cov` | Mocking e report di copertura |
| `black` | Formattatore di codice |
| `flake8` | Linter |
| `isort` | Ordinamento import |
| `mypy` | Type checker statico |
| `pylint` | Analisi statica avanzata |
| `types-requests`, `types-yt-dlp` | Type stub per librerie esterne |

---

## Setup

> **Prerequisiti:** Git, Python 3.10+, `ffmpeg` installato nel sistema.

**1. Clona il repository**

```bash
git clone git@github.com:sean8819/CompareBot.git
cd CompareBot
```

**2. Crea e attiva il virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Installa le dipendenze**

```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt   # opzionale, per sviluppo
```

**4. Configura le variabili d'ambiente**

```bash
cp .env.example .env
# Modifica .env con i tuoi token
```

**5. Avvia il bot**

```bash
python main.py
```

---

## Variabili d'ambiente

| Variabile | Obbligatoria | Descrizione |
| :--- | :---: | :--- |
| `BOT_TOKEN` | Si | Token del bot Telegram (da [BotFather](https://t.me/BotFather)) |
| `PIXABAY_TOKEN` | Si | Chiave API [Pixabay](https://pixabay.com/api/docs/) |
| `HASH_SALT` | No | Salt per l'hashing degli ID utente (default: `fallback_salt`) |

---

## Testing

Il progetto include **55+ test unitari** con copertura su tutti i moduli:

| File di test | Focus |
| :--- | :--- |
| `test_handlers.py` | Command handler, validazione parametri, contesto utente |
| `test_buttons.py` | Generazione menu, gestione pulsanti, logica download, errori |
| `test_downloader.py` | Opzioni yt-dlp, download media, validazione dimensione file |
| `test_beauty.py` | Cache immagini, verifica freschezza, integrazione downloader |
| `test_i18n.py` | Funzioni hash, database utenti, recupero lingua, fallback |
| `test_messages.py` | Funzioni di recupero messaggi |

**Eseguire i test:**

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Eseguire tutti i controlli locali** (lint + type check + test):

```bash
bash localTest.sh
```

Lo script esegue in sequenza: black, mypy, pylint, flake8, isort e pytest con coverage.

---

## CI/CD

Il progetto utilizza **GitHub Actions** con due pipeline attivate su push e pull request verso `main`:

### Pipeline di Linting

- **Pylint** — analisi statica del codice
- **Flake8** — controllo errori di sintassi e complessità ciclomatica
- **MyPy** — type checking statico
- **Black** — verifica formattazione codice
- **isort** — verifica ordinamento import

### Pipeline di Testing

- **pytest** con report di copertura sul modulo `src/`


---

## Team

|          | Nome        | GitHub |
|:---------|:------------| :--- |
| Studente | Giovanni G. | [@sean8819](https://github.com/sean8819) |
| Studente | Marce       | [@Marss08](https://github.com/Marss08) |
| Studente | Vincenzo B. | [@buggenzo](https://github.com/buggenzo) |
