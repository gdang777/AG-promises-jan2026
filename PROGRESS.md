# Project Progress

This file tracks the ongoing development progress of the Promises project.

---

## Project Overview

**Name:** Promises  
**Framework:** Django 4.2.0  
**Database:** PostgreSQL  
**Storage:** Azure Media Storage  

---

## Current Status

🟢 **Active Development**

Last Updated: 2026-01-27

---

## Completed Tasks

### January 2026

- [x] **Dependency Updates (2026-01-27)**
  - Updated Django from 3.1.4 to 4.2.0
  - Updated Pillow to >=11.0.0
  - Updated asgiref to 3.6.0
  - Updated psycopg2-binary to >=2.9.9

- [x] **Repository Migration (2026-01-27)**
  - Changed remote origin to new repository: `AG-promises-jan2026`

- [x] **Trailers Section Restoration (2026-01-27)**
  - Fixed broken single-video display by implementing functional Carousel
  - Restored custom video player controls (Rewind/Forward)
  - Fixed broken thumbnails by implementing fallback logic (Azure vs Local)

- [x] **Documentation & Polish (2026-01-27)**
  - Created `README.md` with project overview and setup
  - Created `DEPLOYMENT.md` with Google Cloud & Azure guides
  - Added `Dockerfile` for containerization
  - Updated Banner Year to 2026



---

## In Progress

- [ ] (Add current work items here)

---

## Planned / Backlog

- [ ] (Add future planned features here)

---

## Project Structure

```
promises/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── start.sh / stop.sh     # Server control scripts
├── promises/              # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── web_app/               # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # App URLs
│   └── admin.py           # Admin configuration
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded media
└── staticfiles/           # Collected static files
```

---

## Models

| Model | Purpose |
|-------|---------|
| `Connect` | Contact form submissions |
| `VideoLink` | Video content with Azure storage |
| `SponsoredBlockTwo` | Sponsored content block |
| `SponsoredBlockThree` | Sponsored content block |
| `SponsoredBlockFour` | Sponsored content block |
| `TabOne` | BTS Kelowna content |
| `TabTwo` | BTS Aldergrove content |
| `TabThree` | BTS Maple Ridge content |

---

## How to Update This File

1. When starting new work, add an item under **In Progress** with `- [ ]`
2. When completing work, move it to **Completed Tasks** with `- [x]` and add the date
3. For future planned work, add items under **Planned / Backlog**
