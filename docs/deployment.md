# 🚀 Deployment Guide

## 📋 Table of Contents

- [✅ Prerequisites](#-prerequisites)
- [📦 Step-by-Step Deployment](#-step-by-step-deployment)
- [🐳 Container Image](#-container-image)
- [🔄 CI/CD with Cloud Build](#-cicd-with-cloud-build)
- [🌐 Custom Domain](#-custom-domain)
- [📊 Monitoring & Logging](#-monitoring--logging)
- [⚙️ Scaling](#️-scaling)
- [🔒 Security](#-security)
- [↩️ Rollback](#️-rollback)
- [✅ Post-Deployment Verification](#-post-deployment-verification)
- [🐛 Troubleshooting](#-troubleshooting)
- [💰 Cost Optimization](#-cost-optimization)

---

## ✅ Prerequisites

| Requirement | Details |
|---|---|
| **Google Cloud account** | Active billing account |
| **Google Cloud SDK** | Latest (`gcloud --version`) |
| **Git** | 2.x or higher |
| **Python** | 3.9 or higher |
| **Gemini API key** | From [Google AI Studio](https://aistudio.google.com/apikey) — must have access to `gemini-3.1-flash`, `nano-banana-pro-preview`, and `gemini-3.1-flash-image-preview` |
| **Project ID** | Your Google Cloud Project ID |

---

## 📦 Step-by-Step Deployment

**Total time: ~5–10 minutes**

### 1. Clone the repository

```bash
git clone https://github.com/RobinaMirbahar/Comic-Studio-Ai.git
cd Comic-Studio-Ai
```

### 2. Set up Google Cloud

```bash
gcloud auth login

export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

gcloud services enable \
    run.googleapis.com \
    secretmanager.googleapis.com \
    cloudbuild.googleapis.com \
    aiplatform.googleapis.com
```

### 3. Store the API key in Secret Manager

```bash
echo -n "YOUR_GEMINI_API_KEY" | \
    gcloud secrets create gemini-api-key \
    --data-file=- \
    --replication-policy="automatic"

export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### 4. Deploy to Cloud Run

```bash
gcloud run deploy comic-studio-ai \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --concurrency 80 \
    --min-instances 1 \
    --max-instances 10 \
    --set-secrets=GEMINI_API_KEY=gemini-api-key:latest
```

After deployment, you'll receive a live URL:

```
https://comic-studio-ai-xxxxx-uc.a.run.app
```

---

## 🐳 Container Image

The application image is available at:

```
gcr.io/cloud-champion-innovator/comic-studio
```

```bash
# Pull and run locally
docker pull gcr.io/cloud-champion-innovator/comic-studio
docker run -p 8080:8080 -e GEMINI_API_KEY=your_key gcr.io/cloud-champion-innovator/comic-studio
```

This image is built and pushed automatically by Cloud Build on each deployment.

---

## 🔄 CI/CD with Cloud Build

### `cloudbuild.yaml`

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/comic-studio-ai', '.']
    id: 'build-image'

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/comic-studio-ai']
    id: 'push-image'

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - run
      - deploy
      - comic-studio-ai
      - --image
      - gcr.io/$PROJECT_ID/comic-studio-ai
      - --region
      - us-central1
      - --platform
      - managed
      - --allow-unauthenticated
      - --memory
      - 2Gi
      - --cpu
      - '2'
      - --timeout
      - '300'
      - --concurrency
      - '80'
      - --min-instances
      - '1'
      - --max-instances
      - '10'
      - --set-secrets
      - GEMINI_API_KEY=gemini-api-key:latest
    id: 'deploy-to-cloud-run'

images:
  - 'gcr.io/$PROJECT_ID/comic-studio-ai'
timeout: 1800s
```

### Create a build trigger

```bash
gcloud builds triggers create github \
    --name="comic-studio-ai-trigger" \
    --repository="https://github.com/RobinaMirbahar/Comic-Studio-Ai" \
    --branch="main" \
    --build-config="cloudbuild.yaml"
```

Once set up, every push to `main` builds and deploys automatically.

---

## 🌐 Custom Domain

```bash
# Verify domain ownership
gcloud domains verify yourdomain.com

# Map to Cloud Run service
gcloud beta run domain-mappings create \
    --service comic-studio-ai \
    --domain comic.yourdomain.com \
    --region us-central1
```

---

## 📊 Monitoring & Logging

```bash
# View recent logs
gcloud logging read \
    "resource.type=cloud_run_revision AND resource.labels.service_name=comic-studio-ai" \
    --limit 50

# Stream logs in real time
gcloud logging tail \
    "resource.type=cloud_run_revision AND resource.labels.service_name=comic-studio-ai"
```

---

## ⚙️ Scaling

```bash
gcloud run services update comic-studio-ai \
    --region us-central1 \
    --min-instances 1 \
    --max-instances 20 \
    --concurrency 100
```

---

## 🔒 Security

The Gemini API key is stored in Secret Manager and injected as an environment variable at runtime — it is never committed to the repository.

**Rotating the API key:**

```bash
gcloud secrets versions add gemini-api-key --data-file=new-key.txt
gcloud secrets versions disable gemini-api-key --version=1
```

---

## ↩️ Rollback

```bash
# List available revisions
gcloud run revisions list --service comic-studio-ai --region us-central1

# Route all traffic to a specific revision
gcloud run services update-traffic comic-studio-ai \
    --to-revisions=comic-studio-ai-00001=100 \
    --region us-central1
```

---

## ✅ Post-Deployment Verification

```bash
export SERVICE_URL=$(gcloud run services describe comic-studio-ai \
    --region us-central1 \
    --format='value(status.url)')

# Check the UI is served
curl $SERVICE_URL | head -20

# Test story generation
curl -X POST $SERVICE_URL/generate-story \
    -H "Content-Type: application/json" \
    -d '{"topic": "mouse on road", "language": "en", "panels": 4}'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| **Deployment fails** | Check quota — `gcloud quotas list` |
| **Secret not found** | Verify the secret exists and IAM binding is correct |
| **API key invalid** | Regenerate at [Google AI Studio](https://aistudio.google.com/apikey) |
| **Memory limit exceeded** | Increase memory — `--memory 4Gi` |
| **Slow cold starts** | Set `--min-instances=1` to keep an instance warm |

---

## 💰 Cost Optimization

Set `--min-instances=0` during development to avoid paying for idle instances:

```bash
gcloud run services update comic-studio-ai \
    --region us-central1 \
    --min-instances 0
```

Switch back to `--min-instances=1` before going to production to eliminate cold starts.

---

## 📝 Environment Variables

| Variable | Description | Required | Stored in Secret Manager |
|---|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ | ✅ |
| `PROJECT_ID` | Google Cloud Project ID | ✅ | — |

---

## Related Documentation

- [Usage Guide](usage.md) — Creating comics step by step
- [API Documentation](api.md) — Full endpoint reference
- [Architecture Overview](architecture.md) — Multi-agent system and data flow

---

<div align="center">

*Comic Studio AI v2.0.0 · March 2026 · Gemini Live Agent Challenge*

</div>
