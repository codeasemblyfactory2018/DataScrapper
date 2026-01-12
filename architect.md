# Application Architecture: Cat Food Price Tracker & Community Hub

## 1. Executive Summary
A high-performance, low-cost web application designed to help Polish cat owners find the lowest prices for high-quality cat food. The system employs a **Hybrid Cloud Architecture**: data aggregation is performed on **local private infrastructure** (Proxmox/Kubernetes), while the public-facing application is served via a **Global CDN** (Cloudflare) using Static Site Generation (SSG). This ensures data privacy/control during scraping while maintaining ability to handle 2 million+ requests on the frontend.

## 2. Technical Constraints & Goals
- **Traffic Capacity:** Support bursts of up to 2 million requests.
- **Cost:** Near-zero cloud maintenance cost (leveraging existing local hardware).
- **Infrastructure:**
  - *Backend/Scraper:* Local Mini PC (Proxmox -> Kubernetes Cluster).
  - *Frontend:* Cloudflare Pages.
- **Freshness:** Data updated once every 24 hours.
- **Performance:** Static HTML delivery for sub-second load times.

## 3. Tech Stack Selection

### Frontend (The "Head" - Public Cloud)
- **Framework:** **Next.js** (React).
  - *Why:* Best-in-class support for SSG. Builds HTML pages at compile time using data fetched from the cloud store.
- **Styling:** **Tailwind CSS**.
- **Hosting/CDN:** **Cloudflare Pages**.
  - *Why:* Unmetered bandwidth, global edge caching, and easy integration with deploy webhooks.

### Backend / Data Pipeline (The "Brain" - Local Private Cloud)
- **Infrastructure:** **Local Kubernetes Cluster** (k3s or MicroK8s on Proxmox).
- **Orchestration:** **Kubernetes CronJob**.
- **Language:** **Python 3.11+**.
- **Scraping Engine:** **Hybrid Strategy Pattern**.
  - *Playwright:* For complex, dynamic SPAs (Single Page Applications) like Allegro that require JavaScript rendering.
  - *BeautifulSoup/HTTPX:* For static, lightweight pages (speed optimized).
  - *Configuration:* Selectors stored in external config (YAML/DB) to allow updates without code redeployment ("Config-over-Code").
- **Data Transport:** **Supabase (PostgreSQL)** + **Cloudflare R2**.

## 4. System Architecture Diagram

```mermaid
graph TD
    subgraph "Local Infrastructure (Proxmox/K8s)"
        Cron[K8s CronJob (03:00 AM)] -->|Spawns| Scraper[Python Scraper Pod]
        Scraper -->|Scrapes Data| External(Ceneo / Allegro)
        Scraper -->|1. Push Clean Data| CloudDB[(Supabase DB / S3)]
        Scraper -->|2. Trigger Rebuild| Webhook[Cloudflare Deploy Hook]
    end

    subgraph "Public Cloud (Cloudflare)"
        Webhook -->|Starts Build| Builder[Next.js Builder]
        Builder -->|Fetch Data| CloudDB
        Builder -->|Generate HTML| CDN[Cloudflare CDN]
    end

    subgraph "Users"
        User((User)) -->|HTTP Request| CDN
    end
```

## 5. Core Features (MVP)
1.  **Product Ranking Page:**
    - Static list generated from the latest database sync.
2.  **Product Detail View:**
    - Historical price charts (data sourced from DB during build).
3.  **Donation Module:**
    - Direct payment links.
    - "Request to Donate" section.

## 6. Scraper Architecture & Data Sync
The scraping system handles the complexity of diverse e-commerce sites via a **Strategy Pattern**.

### A. The Scraper Engine (Local)
1.  **Scraper Manager:**
    - Receives a list of target URLs.
    - Detects domain (e.g., `allegro.pl` vs `zooplus.pl`).
    - Dispatches the task to the appropriate **Worker Strategy**.
2.  **Worker Strategies:**
    - **DynamicWorker (Playwright):** Handles JavaScript-heavy sites, manages cookies, and renders DOM.
    - **StaticWorker (BS4):** High-speed HTTP scraping for simple HTML sites.
3.  **Config-Driven Selectors:**
    - CSS/XPath selectors are NOT hardcoded. They are loaded from a `selectors.yaml` file or the Database.
    - *Benefit:* If a shop changes its layout, we update the config, not the code.
4.  **Health Monitoring:**
    - If a scraper yields 0 results or high error rates, it flags the domain as "Broken" in the admin dashboard for manual review.

### B. Data Sync Flow
1.  **Push:** Scraper Pod pushes clean/normalized data to **Supabase** (Postgres).
2.  **Assets:** Product images are optimized and uploaded to **Cloudflare R2**.
3.  **Trigger:** Once the batch job completes, the scraper sends a `POST` request to the Cloudflare Pages Deploy Hook.

## 7. Future Modules (Microservices Strategy)

### Phase 2: Engagement (Fairy Tales & Spotify)
- **Architecture:** Serverless Functions (Cloudflare Workers or Supabase Edge Functions).
- **Flow:**
    1. User registers (Supabase Auth).
    2. Event triggers Edge Function.
    3. Function calls OpenAI API to generate story.
    4. Function generates PDF and Uploads to S3.
    5. Email sent to user with link.

### Phase 3: Adoption Section
- **Local Scraper Expansion:** Add a new K8s CronJob specifically for scraping shelter websites.

## 8. Project Structure

```
/cat_food_application_project
├── k8s/                    # Kubernetes manifests (CronJobs, Secrets)
│   ├── scraper-cron.yaml
│   └── secrets.yaml
├── backend/                # Python Logic
│   ├── scraper/
│   ├── analysis/
│   └── Dockerfile          # For building the K8s image
├── frontend/               # Next.js Application
│   ├── src/
│   └── lib/                # Database clients
└── architect.md
```
