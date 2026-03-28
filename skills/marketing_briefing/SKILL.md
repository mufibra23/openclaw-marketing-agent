---
name: marketing_briefing
description: Generates a daily marketing intelligence briefing with metrics summary and anomaly detection from GA4 data.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Morning Marketing Briefing

You are OpenClaw's Marketing Intelligence capability. When the user asks for a morning briefing, marketing update, or anomaly check, execute the briefing script and present the results.

## How to Execute

Run the following command to generate the briefing:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python scripts/briefing.py --output json
```

## How to Present Results

Parse the JSON output and present a formatted briefing to the user:

1. **Header**: Show the generation timestamp, data source (bigquery or sample), and analysis period.

2. **Metrics Overview**: Present key metrics from `metrics_summary` in a clean table or bullet list:
   - Total sessions, users, page views
   - Total purchases and revenue
   - Average daily revenue and conversion rate
   - Best and worst revenue days

3. **Anomaly Alerts**: If `anomaly_count > 0`, highlight anomalies by severity:
   - Show CRITICAL alerts first (red/urgent)
   - Then WARNING alerts
   - For each anomaly: metric name, actual value vs rolling average, z-score, and percentage change

4. **Summary**: End with the `anomaly_summary` text for a quick human-readable overview.

## Handling Errors

- If the script fails, inform the user and suggest checking BigQuery credentials or Python dependencies.
- If `data_source` is "sample", note that live BigQuery data was unavailable and sample data was used instead.
- Required Python packages: pandas, numpy, scipy, google-cloud-bigquery, python-dotenv, google-generativeai.

## Example Interaction

**User**: "Give me my morning briefing"

**Agent**: Runs the briefing script, parses the JSON, and responds with a formatted marketing intelligence report including metrics summary and any detected anomalies.
