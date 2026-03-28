---
name: sentiment_monitor
description: Monitors customer feedback sentiment using NLP, detects negative spikes, and recommends actions based on DistilBERT analysis.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Sentiment Monitor

You are OpenClaw's Sentiment Monitoring capability. When the user asks about customer sentiment, feedback trends, or negative reviews, run a sentiment scan and present the results.

## How to Execute

Run the following command to generate a sentiment report:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python scripts/sentiment.py --output json
```

## How to Present Results

Parse the JSON output and present a focused sentiment briefing:

1. **Header**: Show overall severity and timestamp.
   - Severity indicators:
     - Positive trend: sentiment improving
     - Stable: within normal range
     - Notable: slight dip worth monitoring
     - Urgent: negative spike exceeding 15% above baseline

2. **Sentiment Overview**: Present the distribution:
   - Negative / Neutral / Positive counts and percentages
   - Overall sentiment score (-1.0 to +1.0)
   - Analysis method used (DistilBERT model or pre-labeled fallback)

3. **Spike Detection**: If `negative_spike_detected` is true:
   - Show the current vs baseline negative ratio
   - Highlight the delta
   - This is the most important section — lead with it if a spike is detected

4. **Worst Categories**: Show categories with highest negative ratios. These indicate where problems are concentrated.

5. **Sample Negative Reviews**: Show 3-5 example negative reviews so the user can see what customers are saying.

6. **Recommended Actions**: Present each recommendation with its priority level.

## Alerting Behavior

- **Only alert the user proactively if `negative_spike_detected` is true** (>15% above baseline)
- For stable/positive results, present the data calmly without urgency
- For notable results (slight uptick), mention it but don't raise alarm

## Severity Indicators

- Positive trend (improving sentiment)
- Stable (normal range, no action needed)
- Notable (slight negative uptick, worth monitoring)
- Urgent (negative spike >15%, requires immediate attention)

## Handling Errors

- If the script fails, inform the user and suggest checking Python dependencies.
- If `analysis_method` is "pre_labeled", note that the DistilBERT model was unavailable and pre-labeled data was used instead.
- If `data_source` is "sample", note that built-in sample data was used for demonstration.
- The script falls back gracefully if P8's model or data are unavailable.

## Example Interaction

**User**: "How are customers feeling?"

**Agent**: Runs the sentiment scan, parses JSON output, and responds with a formatted sentiment report showing distribution, trends, any spikes detected, worst categories, sample negative reviews, and recommended actions.
