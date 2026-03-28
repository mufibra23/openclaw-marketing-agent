"""
Stripe MPP Commerce Server — Capability 8 of OpenClaw Marketing Agent (P10).

Simulates the Machine Payments Protocol (MPP) HTTP 402 payment challenge
pattern using standard Stripe PaymentIntents. External AI agents hit paid
endpoints, receive a 402 with a Stripe PaymentIntent client_secret, pay,
then retry with the confirmation to unlock the data.

Usage:
    python -m uvicorn scripts.mpp_server:app --host 0.0.0.0 --port 8001
"""

import sys
import os
import json
import time
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Load .env manually (avoid hard dependency on python-dotenv at import time)
_env_file = PROJECT_ROOT / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
# A real Stripe key is 30+ chars; reject obvious placeholders
_stripe_live = (
    STRIPE_SECRET_KEY.startswith(("sk_test_", "sk_live_"))
    and len(STRIPE_SECRET_KEY) > 30
    and "your_" not in STRIPE_SECRET_KEY
)

stripe = None
if _stripe_live:
    import stripe as _stripe
    _stripe.api_key = STRIPE_SECRET_KEY
    stripe = _stripe

# ---------------------------------------------------------------------------
# Endpoint pricing (cents)
# ---------------------------------------------------------------------------

PRICING = {
    "/api/v1/metrics/daily": {"amount": 1, "currency": "usd", "desc": "Daily marketing metrics"},
    "/api/v1/predict/attribution": {"amount": 5, "currency": "usd", "desc": "Attribution prediction"},
    "/api/v1/competitive/latest": {"amount": 2, "currency": "usd", "desc": "Latest competitive scan"},
}

# In-memory confirmation store: confirmation_id -> {path, paid_at, payment_intent}
_confirmations: dict[str, dict] = {}

# ---------------------------------------------------------------------------
# Data loaders — reuse cached output from existing capabilities
# ---------------------------------------------------------------------------

def _load_json(filename: str) -> dict | list | None:
    """Load a JSON file from the data/ directory."""
    path = DATA_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _get_daily_metrics() -> dict:
    """Return daily marketing metrics from briefing history or sample."""
    hist = _load_json("briefing_history.json")
    if hist and hist.get("briefings"):
        latest = hist["briefings"][-1]
        return {
            "source": "briefing_pipeline",
            "generated_at": latest.get("timestamp", datetime.now().isoformat()),
            "metrics": latest.get("metrics_summary", {}),
            "anomaly_count": latest.get("anomaly_count", 0),
        }
    # Fallback sample
    return {
        "source": "sample",
        "generated_at": datetime.now().isoformat(),
        "metrics": {
            "total_sessions": 34420,
            "total_users": 27180,
            "total_page_views": 112650,
            "total_purchases": 486,
            "total_revenue": 18743.50,
            "avg_daily_revenue": 604.63,
            "avg_conversion_rate": 1.41,
            "best_revenue_day": "2021-01-22",
            "worst_revenue_day": "2021-01-03",
        },
        "anomaly_count": 1,
    }


def _get_attribution_prediction() -> dict:
    """Return attribution prediction from history or sample."""
    hist = _load_json("attribution_history.json")
    if hist and hist.get("queries"):
        latest = hist["queries"][-1]
        return {
            "source": "attribution_pipeline",
            "generated_at": latest.get("timestamp", datetime.now().isoformat()),
            "top_channel": latest.get("top_channel", {}),
            "model_agreement": latest.get("model_agreement", {}),
            "recommendations": latest.get("recommendations", []),
        }
    return {
        "source": "sample",
        "generated_at": datetime.now().isoformat(),
        "top_channel": {
            "name": "Organic Search",
            "confidence": "high",
            "models_agreeing": 6,
        },
        "model_agreement": {"score": 82.5, "level": "moderate"},
        "recommendations": [
            {"channel": "Organic Search", "action": "increase", "reason": "Highest cross-model attribution"},
            {"channel": "Paid Search", "action": "maintain", "reason": "Strong last-click performance"},
            {"channel": "Direct", "action": "review", "reason": "May include untagged campaigns"},
        ],
    }


def _get_competitive_latest() -> dict:
    """Return latest competitive scan from history or sample."""
    hist = _load_json("competitive_history.json")
    if hist and hist.get("scans"):
        latest = hist["scans"][-1]
        return {
            "source": "competitive_pipeline",
            "generated_at": latest.get("timestamp", datetime.now().isoformat()),
            "competitors": latest.get("results", {}),
            "overall_severity": latest.get("overall_severity", "minor"),
        }
    return {
        "source": "sample",
        "generated_at": datetime.now().isoformat(),
        "competitors": {
            "shopify": {"share_of_voice": 33.3, "sentiment_score": 0.33, "total_citations": 9},
            "woocommerce": {"share_of_voice": 40.7, "sentiment_score": 0.18, "total_citations": 11},
            "bigcommerce": {"share_of_voice": 25.9, "sentiment_score": 0.43, "total_citations": 7},
        },
        "overall_severity": "minor",
    }


# Map endpoint paths to their data functions
_DATA_FNS = {
    "/api/v1/metrics/daily": _get_daily_metrics,
    "/api/v1/predict/attribution": _get_attribution_prediction,
    "/api/v1/competitive/latest": _get_competitive_latest,
}

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="OpenClaw MPP Commerce Server",
    description=(
        "Simulated Stripe Machine Payments Protocol (MPP) server. "
        "AI agents pay per-call via HTTP 402 payment challenges to access "
        "marketing intelligence endpoints."
    ),
    version="0.1.0",
)


def _build_402_response(path: str, mock: bool = False) -> JSONResponse:
    """Build an HTTP 402 Payment Required response with Stripe PaymentIntent."""
    pricing = PRICING[path]

    if stripe and not mock:
        # Create a real Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=pricing["amount"],
            currency=pricing["currency"],
            description=f"OpenClaw MPP: {pricing['desc']}",
            metadata={"endpoint": path, "mpp_version": "0.1"},
        )
        client_secret = intent.client_secret
        payment_intent_id = intent.id
    else:
        # Mock mode — show what the flow looks like without a live key
        payment_intent_id = f"pi_mock_{uuid.uuid4().hex[:16]}"
        client_secret = f"{payment_intent_id}_secret_mock_{uuid.uuid4().hex[:8]}"

    confirmation_id = f"mpp_{uuid.uuid4().hex[:12]}"

    body = {
        "error": "payment_required",
        "mpp_version": "0.1",
        "message": f"This endpoint requires payment. Amount: ${pricing['amount'] / 100:.2f} {pricing['currency'].upper()}",
        "payment": {
            "provider": "stripe",
            "payment_intent_id": payment_intent_id,
            "client_secret": client_secret,
            "amount": pricing["amount"],
            "currency": pricing["currency"],
            "description": pricing["desc"],
        },
        "instructions": {
            "step_1": "Confirm the PaymentIntent using the client_secret via Stripe.js or the Stripe API",
            "step_2": f"Retry this endpoint with header: X-Payment-Confirmation: {confirmation_id}",
        },
        "confirmation_id": confirmation_id,
        "mock_mode": not _stripe_live,
    }

    # Store confirmation so the retry can be validated
    _confirmations[confirmation_id] = {
        "path": path,
        "payment_intent_id": payment_intent_id,
        "created_at": datetime.now().isoformat(),
        "paid": not _stripe_live,  # In mock mode, auto-approve
    }

    return JSONResponse(status_code=402, content=body)


def _validate_confirmation(confirmation_id: str, path: str) -> str | None:
    """Validate a payment confirmation. Returns error message or None if valid."""
    record = _confirmations.get(confirmation_id)
    if not record:
        return "Unknown confirmation_id. Request a new payment challenge."
    if record["path"] != path:
        return f"Confirmation was issued for {record['path']}, not {path}."

    if stripe and _stripe_live and not record.get("paid"):
        # Verify the PaymentIntent was actually paid
        try:
            intent = stripe.PaymentIntent.retrieve(record["payment_intent_id"])
            if intent.status == "succeeded":
                record["paid"] = True
            else:
                return f"Payment not completed. PaymentIntent status: {intent.status}"
        except Exception as e:
            return f"Could not verify payment: {e}"
    return None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/v1/health")
async def health():
    """Free health check — no payment required."""
    return {
        "status": "healthy",
        "service": "openclaw-mpp-commerce",
        "version": "0.1.0",
        "stripe_mode": "live" if _stripe_live else "mock",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            path: {"price": f"${p['amount'] / 100:.2f}", "description": p["desc"]}
            for path, p in PRICING.items()
        },
    }


async def _handle_paid_endpoint(request: Request, path: str):
    """Common handler for all paid endpoints — implements the 402 challenge flow."""
    confirmation = request.headers.get("x-payment-confirmation")

    if not confirmation:
        return _build_402_response(path)

    # Validate the confirmation
    error = _validate_confirmation(confirmation, path)
    if error:
        return JSONResponse(status_code=403, content={"error": "payment_invalid", "message": error})

    # Payment confirmed — return the data
    data_fn = _DATA_FNS[path]
    result = data_fn()

    # Clean up used confirmation
    _confirmations.pop(confirmation, None)

    return {
        "status": "success",
        "payment_confirmed": True,
        "endpoint": path,
        "price_charged": f"${PRICING[path]['amount'] / 100:.2f}",
        "data": result,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/metrics/daily")
async def metrics_daily(request: Request):
    """Daily marketing metrics — $0.01 per call."""
    return await _handle_paid_endpoint(request, "/api/v1/metrics/daily")


@app.post("/api/v1/predict/attribution")
async def predict_attribution(request: Request):
    """Attribution prediction — $0.05 per call."""
    return await _handle_paid_endpoint(request, "/api/v1/predict/attribution")


@app.get("/api/v1/competitive/latest")
async def competitive_latest(request: Request):
    """Latest competitive scan — $0.02 per call."""
    return await _handle_paid_endpoint(request, "/api/v1/competitive/latest")
