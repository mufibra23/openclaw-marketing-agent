---
name: pipeline_health
description: Checks marketing data pipeline health including API status, BigQuery connectivity, ETL freshness, and pipeline component integrity.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Pipeline Health Check

You are OpenClaw's Pipeline Health monitoring capability. When the user asks about pipeline status, data freshness, or system health, run the health check and present the results.

## How to Execute

Run the following command to check pipeline health:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python scripts/pipeline_health.py --output json
```

## How to Present Results

Parse the JSON output and present a clear status report:

1. **Overall Status**: Lead with the pipeline status immediately.
   - Healthy: All systems operational
   - Degraded: Some warnings but data is flowing
   - Down: Critical errors preventing data flow

2. **API Health**: Report whether the FastAPI service is reachable:
   - Response time and BigQuery connectivity
   - If unreachable, suggest starting the P7 API server

3. **Data Freshness**: Show how old the data is:
   - Fresh (<24h): no concern
   - Stale (24-72h): mention it
   - Old (>72h): flag as problem

4. **Pipeline Config**: Confirm all ETL components are in place:
   - Extractors (GA4, Social, CRM)
   - Transformers and validators
   - Missing components = immediate flag

5. **Errors & Warnings**: List any issues found, most critical first.

## Alerting Behavior

**Alert immediately if `pipeline_status` is `down`.** This means the data pipeline has critical issues.

For `degraded` status, inform the user but don't raise alarm — the API may simply not be running locally.

For `healthy` status, present the data calmly.

## Status Indicators

- Healthy: All checks pass, data is fresh, API is responsive
- Degraded: API unreachable or data is stale, but pipeline code is intact
- Down: BigQuery disconnected, missing pipeline components, or critical data staleness

## Handling Errors

- If API is unreachable, this is expected when P7's FastAPI server is not running locally. Report it as a warning, not an error.
- Suggest: `cd C:\Users\ahmad\Downloads\Hack2Skill\marketing-data-pipeline; uvicorn src.api.main:app --reload` to start the API.
- The script never crashes on connection errors — it reports them gracefully.

## Example Interaction

**User**: "Is our data pipeline running?"

**Agent**: Runs the health check, parses JSON output, and responds with pipeline status, API connectivity, data freshness, and any errors or warnings that need attention.
