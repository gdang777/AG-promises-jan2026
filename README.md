# Promises Project

A Django-based web application for the "Promises" movie project, featuring mixed-media carousels, video content via Azure Blob Storage, and section-based content management (Trailers, BTS).

## 🚀 Status
**Active Development** (January 2026)

## 🛠 Tech Stack
- **Framework:** Django 4.2.0
- **Database:** PostgreSQL (`psycopg2-binary`)
- **Storage:** Azure Blob Storage (for video streaming)
- **Frontend:** Bootstrap 4, Slick Slider, custom HTML5 Video players

## ✨ Key Features
- **Trailers Carousel:** Dynamic carousel with custom video player controls (Rewind, Forward, Fullscreen).
- **Mixed Media Support:** Sections like "BTS Kelowna" support mixed content (Images, Videos, YouTube links).
- **Robust Thumbnails:** Smart fallback logic uses Azure-generated thumbnails for production media and a static placeholder (`video-thumbnail.png`) for local development or missing assets.
- **Admin Interface:** Managed via `jazzmin` for a clean, modern backend experience.

## 📦 Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- `pip`

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gdang777/AG-promises-jan2026.git
   cd AG-promises-jan2026/promises
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database:**
   Update `DATABASES` in `promises/settings.py` with your PostgreSQL credentials.

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Access the site at `http://127.0.0.1:8000/`.

## 📂 Project Structure
```
promises/
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── promises/              # Project Settings
├── web_app/               # Main Application Logic
├── templates/             # HTML Templates (index.html)
├── static/                # CSS, JS, Images
└── media/                 # User uploaded media
```

## 📝 Changelog
See [CHANGES.md](./CHANGES.md) for a detailed history of updates.
