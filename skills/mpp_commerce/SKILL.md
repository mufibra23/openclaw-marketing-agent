---
name: mpp_commerce
description: Starts the Stripe MPP Commerce server that lets external AI agents pay per-call for marketing intelligence via HTTP 402 payment challenges.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Stripe MPP Commerce Server

You are OpenClaw's Machine Payments Protocol (MPP) Commerce capability. When the user asks to start the MPP server, check payment status, or manage agent commerce, handle it here.

## What is MPP?

Machine Payments Protocol (MPP) enables **agent-to-agent commerce** over HTTP. Instead of API keys or subscriptions, external AI agents discover paid endpoints, receive an HTTP 402 Payment Required challenge with a Stripe PaymentIntent, complete payment programmatically, and retry with a confirmation header to unlock the data.

This lets any AI agent pay for access to OpenClaw's marketing intelligence — no human signup required.

## Trigger Phrases

- "start the API"
- "payment status"
- "MPP status"
- "agent commerce"
- "start mpp server"

## How to Execute

Start the MPP Commerce server:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python -m uvicorn scripts.mpp_server:app --host 0.0.0.0 --port 8001
```

The server starts on http://localhost:8001.

## Available Endpoints

| Endpoint | Method | Price | Description |
|----------|--------|-------|-------------|
| `/api/v1/health` | GET | Free | Health check, lists all endpoints and pricing |
| `/api/v1/metrics/daily` | GET | $0.01 | Daily marketing metrics with anomaly detection |
| `/api/v1/predict/attribution` | POST | $0.05 | Multi-model attribution prediction |
| `/api/v1/competitive/latest` | GET | $0.02 | Latest competitive intelligence scan |

## The 402 Payment Challenge Flow

1. **Agent hits a paid endpoint** without payment → gets HTTP 402 with Stripe PaymentIntent details
2. **Agent confirms the PaymentIntent** via Stripe API using the `client_secret`
3. **Agent retries the endpoint** with header `X-Payment-Confirmation: <confirmation_id>` → gets the data

## Stripe Configuration

The server reads `STRIPE_SECRET_KEY` from `.env`. Two modes:

- **Live mode** (`sk_test_*` or `sk_live_*`): Creates real Stripe PaymentIntents, verifies payment before releasing data
- **Mock mode** (no key or placeholder): Returns realistic 402 responses with mock PaymentIntent IDs; confirmations are auto-approved for demo purposes

## How to Present Results

When the user asks to start the server:
1. Run the exec command above
2. Confirm the server is running and show the health endpoint URL
3. Explain mock vs live mode based on whether a real Stripe key is configured

When the user asks about payment status:
1. Hit the `/api/v1/health` endpoint
2. Report the Stripe mode and available endpoints with pricing

## Handling Errors

- If uvicorn is not installed: `venv\Scripts\pip install uvicorn`
- If stripe is not installed: `venv\Scripts\pip install stripe`
- If port 8001 is in use: suggest `--port 8002` or kill the existing process
- The server gracefully handles missing Stripe keys by running in mock mode

## Example Interactions

**User**: "Start the MPP server"
**Agent**: Runs the uvicorn command, confirms it's running on port 8001, reports mock/live mode.

**User**: "How would an external agent buy our data?"
**Agent**: Explains the 402 flow — hit endpoint, get payment challenge, pay via Stripe, retry with confirmation.
