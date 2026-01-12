# Cat Food Scraper Deployment Guide

This guide describes how to configure, build, and deploy your scraper to your local Kubernetes cluster (Proxmox) and connect it to your Cloud infrastructure.

## 1. Required Accounts & Infrastructure

Before starting, ensure you have the following:

| Service | Purpose | Action Required |
| :--- | :--- | :--- |
| **Supabase** | Database (PostgreSQL) | Create a new project. Save the **Project URL** and **Service Role Key** (found in Project Settings > API). |
| **Docker Hub** (or GHCR) | Container Registry | Create an account to host your Docker image (e.g., `hub.docker.com`). |
| **Cloudflare Pages** | Frontend Hosting | Connect your GitHub repo. Go to Settings > Deploy Hooks and create a hook (e.g., "Daily Update"). |
| **Proxmox/K8s** | Local Infrastructure | Ensure you have `kubectl` access to your cluster. |

---

## 2. Configuration Variables (Checklist)

You need to replace specific placeholders in your code and configuration files.

### A. Kubernetes Secrets (`k8s/secrets-template.yaml`)
*Rename this file to `k8s/secrets.yaml` before editing to avoid committing secrets to git.*

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `SUPABASE_URL` | Your database API endpoint | `https://xyzproject.supabase.co` |
| `SUPABASE_KEY` | **Critical:** Use the **SERVICE_ROLE** key, not the Anon key, to allow writing data. | `eyJhbGciOiJIUzI1Ni...` |
| `CLOUDFLARE_DEPLOY_HOOK` | Webhook to trigger frontend rebuild | `https://api.cloudflare.com/client/v4/pages/webhooks/...` |

### B. Kubernetes CronJob (`k8s/scraper-cronjob.yaml`)

| Variable | Location | Description |
| :--- | :--- | :--- |
| `image` | Line 16 | The address of the Docker image you will build. |
| **Example** | `image: your-username/cat-food-scraper:latest` | |

### C. Backend Logic (`backend/main.py`)
*Note: Currently, the main script prints to console. You will need to uncomment/add the Supabase insertion logic using the variables above.*

---

## 3. Step-by-Step Deployment

### Step 1: Database Setup
1.  Log in to Supabase.
2.  Go to the **SQL Editor**.
3.  Open `backend/schema.sql` from this project.
4.  Copy the content and run it in the SQL Editor to create the tables.

### Step 2: Build & Push Docker Image
Run these commands from the `cat_food_application_project` root directory.

```bash
# 1. Login to Docker Hub
docker login

# 2. Build the image (replace 'your-username' with your actual Docker Hub user)
docker build -t your-username/cat-food-scraper:latest -f backend/Dockerfile backend/

# 3. Push to the registry
docker push your-username/cat-food-scraper:latest
```

### Step 3: Configure Kubernetes
1.  Edit `k8s/scraper-cronjob.yaml`:
    ```yaml
    # Change this line:
    image: your-registry/cat-food-scraper:latest
    # To:
    image: your-username/cat-food-scraper:latest
    ```
2.  Create the secrets file:
    ```bash
    cp k8s/secrets-template.yaml k8s/secrets.yaml
    nano k8s/secrets.yaml
    # Paste your real Supabase keys here
    ```

### Step 4: Deploy to Cluster
```bash
# Apply secrets
kubectl apply -f k8s/secrets.yaml

# Apply the CronJob
kubectl apply -f k8s/scraper-cronjob.yaml
```

### Step 5: Validation
To test if it works without waiting for 3:00 AM:

```bash
# Manually trigger the job
kubectl create job --from=cronjob/cat-food-scraper manual-test-01

# Check if pods started
kubectl get pods

# View logs to see the scraping process
kubectl logs job/manual-test-01
```

## 4. Troubleshooting

- **"Temporary failure in name resolution":**
  - Verify your K8s cluster DNS settings (CoreDNS).
  - Ensure your Proxmox VM allows outgoing traffic on port 443.
- **"Playwright not found":**
  - Ensure you didn't change the `Dockerfile`. It specifically installs the heavy dependencies required for headless browsers.
- **Data not showing in Supabase:**
  - Check the logs. If `main.py` finishes without error but no data appears, ensure the `Supabase` client code is actually calling `.insert()`. (See `backend/src/utils/db.py` if implemented).
