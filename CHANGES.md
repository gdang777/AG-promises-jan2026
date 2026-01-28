# Changelog

All notable changes to the Promises project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Changed
- (Future changes will be logged here)

---

## [2026-01-27] - Trailers & Frontend Fixes

### Fixed
- **Trailers Section:** Replaced static single-video display with a functional Bootstrap carousel iterating over all 4 trailer videos.
- **Thumbnails:** Fixed broken thumbnails by adding logic to fall back to a static placeholder (`video-thumbnail.png`) when Azure `background_url` is missing (resolving local data issues).
- **Video Player:** Restored missing custom controls (Rewind, Forward, Fullscreen) to the video player.

### Changed
- Standardized carousel indicator logic in `index.html`.
- Updated Home Banner text to "Sikh Heritage Month 2026".

### Added
- `README.md`: Comprehensive project documentation.
- `DEPLOYMENT.md`: Detailed deployment guides for GCP and Azure.
- `Dockerfile`: Production-ready container configuration.



## [2026-01-27] - Dependency Updates

### Changed
- Updated `psycopg2-binary` from `2.8.6` to `>=2.9.9`
- Updated `asgiref` from `3.3.1` to `3.6.0`
- Updated `Django` from `3.1.4` to `4.2.0`
- Updated `Pillow` from `8.1.0` to `>=11.0.0`

---

## [Earlier Changes]

### Added
- Initial project setup with Django framework
- PostgreSQL database integration
- Azure Media Storage support for video uploads
- Models: `Connect`, `VideoLink`, `SponsoredBlockTwo/Three/Four`, `TabOne/Two/Three`
- BTS (Behind The Scenes) content sections for Kelowna, Aldergrove, and Maple Ridge

---

## How to Log Changes

When making changes to this project, add a new entry under `[Unreleased]` with the following format:

```markdown
### Added
- New feature description

### Changed
- Description of what was modified

### Fixed
- Bug fix description

### Removed
- Removed feature description
```

Once changes are released, move them to a dated section.
