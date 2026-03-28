---
name: lead_scoring
description: Scores leads using XGBoost classifier, identifies hot prospects (>70% conversion probability), and explains scores with SHAP feature importance.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Lead Scoring

You are OpenClaw's Lead Scoring capability. When the user asks about lead priorities, hot leads, or which leads to follow up with, run the scoring pipeline and present the results.

## How to Execute

Run the following command to generate a lead scoring report:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python scripts/lead_scoring.py --output json
```

## How to Present Results

Parse the JSON output and present an actionable lead scoring briefing:

1. **Summary**: Total leads scored, model performance (ROC-AUC), and the hot/warm/cold distribution.

2. **Hot Leads**: The most important section. For each hot lead, show:
   - Lead score and conversion probability
   - Key attributes (Tags, Source, Time on Site, Activity)
   - **SHAP-based reasons** — explain WHY this lead scored high using the `shap_reasons` list
   - These reasons come from the model's feature importance analysis

3. **Explaining SHAP Reasons**: Present the reasons in plain English:
   - "Pipeline stage indicates intent" → This lead's status in the sales pipeline is the strongest signal they'll convert
   - "High website engagement" → They spent significant time browsing, showing genuine interest
   - "Active communication" → Recent phone calls or SMS exchanges indicate active engagement
   - "Working professional" → Their occupation correlates with higher conversion rates

4. **Top Predictive Features**: Show the SHAP feature importance ranking so the user understands what drives conversions overall.

5. **Recommendations**: Present the prioritized action list:
   - Hot leads → immediate personal outreach
   - Warm leads → nurture with content
   - Cold leads → automated campaigns only

## Score Categories

| Category | Score Range | Meaning | Recommended Action |
|----------|-----------|---------|-------------------|
| Hot | 70-100 | >70% likely to convert | Immediate follow-up, phone call, demo |
| Warm | 40-70 | Moderate intent | Email sequences, case studies, webinars |
| Cold | 0-40 | Low probability | Automated nurture only |

## Handling Errors

- If the script fails, inform the user and suggest checking Python dependencies.
- If `data_source` is "sample", note that sample data was used for demonstration.
- If `data_source` is "p4_precomputed", the scores come from P4's trained XGBoost model on the test set.
- The model achieves 93.8% accuracy and 0.978 ROC-AUC on held-out test data.

## Example Interaction

**User**: "Which leads should we follow up with?"

**Agent**: Runs the lead scoring script, parses JSON output, and responds with a prioritized list of hot leads with their scores, key attributes, and SHAP-based explanations for why each lead is likely to convert.
