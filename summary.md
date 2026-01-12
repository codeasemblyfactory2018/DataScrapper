# Project Summary: Cat Food Price Tracker

## Current Status
- **Project Initialized:** Directory `cat_food_application_project` created.
- **Architecture Defined:** `architect.md` completed.

## Architecture Highlights
- **Hybrid Cloud Model:**
    - **Local Infrastructure:** Proxmox/Kubernetes cluster on a Mini PC handles data scraping and processing.
    - **Public Frontend:** Next.js (React) hosted on Cloudflare Pages for sub-second performance and 2M+ request capacity at near-zero cost.
- **Data Pipeline:**
    - **Scraper:** Python-based using a **Strategy Pattern** (Playwright for dynamic sites like Allegro, BeautifulSoup for static sites).
    - **Configuration:** Selectors are stored in YAML/DB to allow UI updates without code changes.
    - **Persistence:** Supabase (PostgreSQL) for structured data; Cloudflare R2 for assets.
- **Sync Method:** Local scrapers "push" data to Supabase and trigger a Cloudflare Deploy Hook for Daily Static Site Generation (SSG).

## Key Features Planned
- **MVP:** Healthy cat food ranking, price comparison tables (Ceneo, Allegro, etc.), donation module.
- **Future:** User registration, AI-generated fairy tales (PDF/Audio), and cat adoption section.

## Next Steps
- Implement the Backend Scraper core (Manager and Strategy workers).
- Define the initial `selectors.yaml`.
- Set up the Supabase database schema.
