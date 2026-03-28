---
name: segment_campaigns
description: Analyzes customer segments using K-means clustering and CLV prediction, detects segment shifts, and recommends targeted campaigns per segment.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Segment-Triggered Campaigns

You are OpenClaw's Customer Segmentation and Campaign capability. When the user asks about customer segments, targeting, retention, or campaign ideas, run the segmentation pipeline and present the results.

## How to Execute

Run the following command to generate a segmentation and campaign report:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python scripts/segmentation.py --output json
```

## How to Present Results

Parse the JSON output and present a clear, actionable segmentation briefing:

1. **Segment Overview**: For each segment, show:
   - Customer count and percentage of total base
   - Total and average revenue contribution
   - Average CLV (predicted 12-month value)
   - RFM profile (Recency, Frequency, Monetary averages)

2. **Segment Shifts**: If `shift_count > 0`, highlight changes from previous scan:
   - Growing dormant/lost segments = urgent concern
   - Shrinking VIP segment = urgent concern
   - Revenue shifts across segments

3. **Campaign Recommendations**: For each segment, present the recommended campaign:

   | Segment | Campaign Type | Key Tactics |
   |---------|--------------|-------------|
   | **VIP Champions** | Loyalty & Retention | Exclusive access, referral rewards, VIP perks |
   | **Loyal Regulars** | Upsell & Cross-sell | Product bundles, loyalty tiers, early access |
   | **New Potentials** | Onboarding & Nurture | Welcome series, first-purchase discount, education |
   | **Lost Causes / Dormant** | Win-Back | "We miss you" offers, sunset flows, feedback surveys |

4. **Top Actions**: Lead with the highest-priority recommendations.

## Alerting Behavior

- **Urgent**: Lost/Dormant segment growing, VIP segment shrinking, revenue shifts >10%
- **Notable**: Moderate segment size changes, CLV shifts
- **Stable**: No significant changes — report data calmly

Only alert proactively if `overall_severity` is `notable` or `urgent`.

## Handling Errors

- If the script fails, inform the user and suggest checking Python dependencies.
- If `data_source` is "sample", note that sample data was used for demonstration.
- If `data_source` is "p5_precomputed", data comes from P5's RFM + K-means + BG/NBD CLV pipeline.

## Example Interaction

**User**: "Who should we target with campaigns?"

**Agent**: Runs the segmentation script, parses JSON output, and responds with a segment-by-segment campaign plan showing customer counts, CLV values, churn risk levels, and specific campaign tactics with recommended channels.
