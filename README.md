# OpenClaw Marketing Intelligence Agent

**P10 (Capstone) | AI Marketing Analytics Portfolio**

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3-orange.svg)](https://openclaw.ai)
[![Claude Opus 4.6](https://img.shields.io/badge/LLM-Claude%20Opus%204.6-blueviolet.svg)](https://anthropic.com)
[![Telegram](https://img.shields.io/badge/Channel-Telegram-26A5E4.svg)](https://telegram.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A 24/7 autonomous marketing intelligence agent that wraps 9 prior portfolio projects into a single always-on system. Built on [OpenClaw](https://openclaw.ai) with Claude Opus 4.6, it monitors marketing data, detects anomalies, scores leads, tracks competitors, and delivers alerts via Telegram on a cron schedule.

---

## The Problem

Marketing teams drown in dashboards. GA4, CRM, support tickets, attribution reports, competitive intel -- each lives in a separate tool, checked manually, with insights arriving too late. A spike in negative sentiment goes unnoticed for days. Budget keeps flowing to underperforming channels because no one ran the attribution model this week.

## The Solution

One agent. Always running. It pulls data from every source on a schedule, applies ML models (XGBoost, DistilBERT, Markov chains, LSTM), detects what matters, and only pings you on Telegram when something needs attention. No dashboard-checking. No morning routine. Just alerts when they count.

---

## Architecture

```
                          +---------------------+
                          |     Telegram Bot     |
                          | @Fariz_OpenClaw_on_  |
                          |      Dell_Bot        |
                          +---------+-----------+
                                    |
                                    | alerts
                                    v
+------------------+      +---------------------+      +-------------------+
|   Cron Scheduler |----->|   OpenClaw Gateway   |----->|  Claude Opus 4.6  |
|  (6 scheduled    |      |   localhost:18789    |      |  (Anthropic API)  |
|   jobs)          |      +---------------------+      +-------------------+
+------------------+                |
                                    | invokes skills
                                    v
        +-----------------------------------------------------------+
        |                     8 Agent Skills                         |
        |                                                           |
        |  marketing_briefing  |  competitive_intel  |  sentiment   |
        |  attribution_agent   |  lead_scoring       |  segments    |
        |  pipeline_health     |  mpp_commerce                     |
        +-----------------------------------------------------------+
                                    |
                                    | runs scripts
                                    v
        +-----------------------------------------------------------+
        |                   Python Scripts                           |
        |                                                           |
        |  briefing.py    competitive.py    sentiment.py            |
        |  attribution.py lead_scoring.py   segmentation.py         |
        |  pipeline_health.py               mpp_server.py           |
        +-----------------------------------------------------------+
                    |                   |                   |
                    v                   v                   v
          +--------------+   +------------------+   +--------------+
          |   BigQuery   |   |  P1-P9 Project   |   |   Stripe     |
          |  GA4 Dataset |   |  Data & Models   |   | (simulated)  |
          +--------------+   +------------------+   +--------------+
```

---

## 8 Capabilities

### 1. Morning Marketing Briefing (wraps P1)
Daily metrics summary from GA4 BigQuery data with z-score anomaly detection. Flags unusual spikes in sessions, revenue, or conversion rates.

### 2. Competitive Intelligence (wraps P2)
Scans competitor mentions across AI platforms, calculates share of voice, sentiment scores, and citation quality. Detects positioning shifts.

### 3. Sentiment Monitoring (wraps P8)
Runs DistilBERT inference on customer support tickets. Detects negative sentiment spikes (>15% above rolling baseline) and identifies worst categories.

### 4. Attribution Agent (wraps P6 + P7)
8-model attribution pipeline: first-click, last-click, linear, time-decay, position-based, Markov chain, Shapley value, and LSTM deep learning. Measures cross-model agreement via Spearman rank correlation and generates budget recommendations.

### 5. Lead Scoring (wraps P4)
XGBoost classifier scoring leads by conversion probability (97.8% ROC-AUC). SHAP-based explanations for each hot lead. Categorizes into hot/warm/cold tiers.

### 6. Segment-Triggered Campaigns (wraps P5 + P9)
K-means customer clustering with RFM analysis and BG/NBD lifetime value prediction. Detects segment migration (growing dormant segments, shrinking VIP) and triggers campaign recommendations.

### 7. Pipeline Health (wraps P7)
Monitors the marketing data pipeline: FastAPI endpoint health, BigQuery connectivity, ETL component integrity, and data freshness (24h/72h thresholds).

### 8. Stripe MPP Commerce (new in P10)
Simulated Machine Payments Protocol server. External AI agents can pay per-call ($0.01-$0.05) for marketing data access via HTTP 402 payment challenges backed by Stripe PaymentIntents.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Gateway | OpenClaw 2026.3 (self-hosted, localhost:18789) |
| LLM | Claude Opus 4.6 (Anthropic) / Gemini 3.1 Pro (Google) |
| Language | Python 3.13 |
| ML/Stats | XGBoost, scikit-learn, DistilBERT, LSTM (TensorFlow), SHAP, scipy |
| Data | pandas, numpy, BigQuery (GA4 public dataset) |
| API | FastAPI, uvicorn, Stripe SDK |
| Messaging | Telegram Bot API |
| Cloud | GCP (project: `galvanic-smoke-489914-u7`) |
| Scheduling | OpenClaw cron (6 jobs, Telegram delivery) |

---

## Cron Schedule

| Job | Schedule | Telegram Alert |
|-----|----------|---------------|
| Morning Briefing | Daily 07:00 WIB | Always |
| Competitive Scan | Every 6 hours | Only if severity is `notable` or `urgent` |
| Sentiment Check | Every 2 hours | Only if negative spike detected |
| Lead Score Refresh | Every 4 hours | Always (summary only) |
| Pipeline Health | Every 30 minutes | Only if `degraded` or `down` |
| Weekly Marketing Intel | Monday 07:30 | Always |

---

## Project Structure

```
openclaw-marketing-agent/
├── scripts/
│   ├── __init__.py
│   ├── briefing.py           # Cap 1: GA4 metrics + anomaly detection (228 LOC)
│   ├── competitive.py        # Cap 2: Competitor scanning + change detection (362 LOC)
│   ├── sentiment.py          # Cap 3: DistilBERT sentiment + spike detection (542 LOC)
│   ├── attribution.py        # Cap 4: 8-model attribution pipeline (604 LOC)
│   ├── lead_scoring.py       # Cap 5: XGBoost lead scoring + SHAP (521 LOC)
│   ├── segmentation.py       # Cap 6: K-means segments + CLV + campaigns (569 LOC)
│   ├── pipeline_health.py    # Cap 7: ETL monitoring + data freshness (452 LOC)
│   └── mpp_server.py         # Cap 8: Stripe MPP commerce server (326 LOC)
├── skills/
│   ├── marketing_briefing/SKILL.md
│   ├── competitive_intel/SKILL.md
│   ├── sentiment_monitor/SKILL.md
│   ├── attribution_agent/SKILL.md
│   ├── lead_scoring/SKILL.md
│   ├── segment_campaigns/SKILL.md
│   ├── pipeline_health/SKILL.md
│   └── mpp_commerce/SKILL.md
├── data/
│   ├── attribution_history.json
│   ├── competitive_history.json
│   ├── lead_scoring_history.json
│   ├── pipeline_health_history.json
│   ├── segmentation_history.json
│   └── sentiment_history.json
├── tests/
├── .env                      # Stripe keys (not committed)
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites
- Python 3.13+
- [OpenClaw](https://openclaw.ai) installed and configured
- Telegram bot token (for alert delivery)

### Setup

```bash
# Clone
git clone https://github.com/mufibra23/openclaw-marketing-agent.git
cd openclaw-marketing-agent

# Python environment
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux

# Dependencies
pip install pandas numpy scipy scikit-learn xgboost shap
pip install fastapi uvicorn stripe
pip install google-cloud-bigquery python-dotenv google-generativeai

# Environment variables
cp .env.example .env
# Edit .env with your Stripe test keys (optional)
```

### Register Skills with OpenClaw

In `~/.openclaw/openclaw.json`, add the skills directory:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["C:\\path\\to\\openclaw-marketing-agent\\skills"]
    }
  }
}
```

### Run Individual Capabilities

```bash
# Morning briefing
python scripts/briefing.py --output json

# Competitive scan
python scripts/competitive.py --competitors "shopify,woocommerce,bigcommerce" --output json

# Sentiment analysis
python scripts/sentiment.py --output json

# Attribution (with natural language query)
python scripts/attribution.py --query "Where should we spend our budget?" --output json

# Lead scoring
python scripts/lead_scoring.py --output json

# Customer segmentation
python scripts/segmentation.py --output json

# Pipeline health
python scripts/pipeline_health.py --output json

# MPP Commerce server
python -m uvicorn scripts.mpp_server:app --host 0.0.0.0 --port 8001
```

### Test MPP Payment Flow

```bash
# 1. Hit a paid endpoint (get 402 challenge)
curl http://localhost:8001/api/v1/metrics/daily

# 2. Copy the confirmation_id from the response

# 3. Retry with payment confirmation
curl -H "X-Payment-Confirmation: mpp_xxxx" http://localhost:8001/api/v1/metrics/daily
```

---

## Portfolio Integration

This capstone project integrates 9 prior projects:

| Project | Repository | What P10 Uses |
|---------|-----------|---------------|
| P1 | [marketing-intelligence-agent](https://github.com/mufibra23/marketing-intelligence-agent) | BigQuery GA4 pipeline, anomaly detection |
| P2 | [ai-competitive-intel](https://github.com/mufibra23/ai-competitive-intel) | Citation analysis, brand sentiment |
| P4 | [lead-scoring-system](https://github.com/mufibra23/lead-scoring-system) | XGBoost model, SHAP explainability |
| P5 | [customer-segmentation-clv](https://github.com/mufibra23/customer-segmentation-clv) | K-means clusters, CLV predictions |
| P6 | [marketing-attribution-agent](https://github.com/mufibra23/marketing-attribution-agent) | 8 attribution models, LSTM |
| P7 | [marketing-data-pipeline](https://github.com/mufibra23/marketing-data-pipeline) | FastAPI, ETL, BigQuery integration |
| P8 | [nlp-customer-intelligence](https://github.com/mufibra23/nlp-customer-intelligence) | DistilBERT sentiment, BERTopic |
| P9 | [unified-marketing-intelligence](https://github.com/mufibra23/unified-marketing-intelligence) | Campaign trigger logic |

---

## Data Sources

This project uses **sample and demonstration data** for portfolio purposes:

- **GA4 data**: Google's public BigQuery dataset (`bigquery-public-data.ga4_obfuscated_sample_ecommerce`), with built-in sample fallback
- **Support tickets**: Synthetic dataset generated in P8
- **Lead data**: Synthetic CRM data from P4
- **Customer segments**: Pre-computed from P5's RFM + CLV pipeline
- **Attribution**: Pre-computed results from P6's 8-model pipeline
- **Competitive intel**: Simulated AI citation data

All scripts fall back gracefully to built-in sample data when upstream project data or credentials are unavailable.

---

## Screenshots

> Screenshots of the Telegram bot delivering alerts, the MPP 402 flow, and the OpenClaw dashboard will be added here.

---

## Freelance Service Value

The system this agent automates -- daily monitoring, anomaly detection, attribution analysis, lead scoring, competitive tracking, and pipeline health -- typically requires a dedicated marketing analyst or a managed analytics retainer.

**Comparable market rate**: $10,000-25,000 setup + $500-1,500/mo recurring.

---

## License

MIT
