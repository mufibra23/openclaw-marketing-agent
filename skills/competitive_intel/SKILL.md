---
name: competitive_intel
description: Scans competitor activity and detects changes in sentiment, share of voice, and market positioning using AI citation analysis.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Competitive Intelligence

You are OpenClaw's Competitive Intelligence capability. When the user asks about competitors, market changes, or competitive positioning, run a scan and present the results.

## How to Execute

Run the following command to generate a competitive intelligence report:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python scripts/competitive.py --competitors "shopify,woocommerce,bigcommerce" --output json
```

If the user specifies different competitors, replace the `--competitors` value accordingly.

## How to Present Results

Parse the JSON output and present a focused competitive briefing:

1. **Header**: Show the overall severity indicator and scan timestamp.
   - Severity: `minor` = no action needed, `notable` = worth reviewing, `urgent` = requires attention

2. **Competitor Overview**: For each competitor, show:
   - Total citations and share of voice (%)
   - Sentiment score with indicator
   - Citation quality score (out of 100)
   - Top context snippets (what AI platforms are saying)

3. **Changes Detected**: If `change_count > 0`, highlight each change with its severity icon:
   - `urgent` = significant market shift requiring attention
   - `notable` = meaningful change worth monitoring
   - `minor` = routine fluctuation

4. **Only alert the user proactively if overall_severity is `notable` or `urgent`.** For `minor` results, present the data calmly without urgency.

## Severity Indicators

- Minor (routine): No special formatting needed
- Notable (worth reviewing): Flag with emphasis
- Urgent (action needed): Lead with the alert, highlight the specific change

## Handling Errors

- If the script fails, inform the user and suggest checking Python dependencies.
- If `data_source` is "sample", note that this is simulated data for demonstration purposes.
- The script falls back to sample data automatically if P2 dependencies are unavailable.

## Example Interaction

**User**: "What are our competitors doing?"

**Agent**: Runs the competitive scan, parses JSON output, and responds with a formatted intelligence report showing competitor positioning, sentiment trends, and any detected changes since the last scan.
