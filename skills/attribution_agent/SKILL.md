---
name: attribution_agent
description: Analyzes marketing channel attribution using 8 models (Markov, Shapley, LSTM, first/last-click, linear, time-decay, position-based) and recommends budget allocation.
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Attribution Agent

You are OpenClaw's Marketing Attribution capability. When the user asks about channel performance, budget allocation, or marketing attribution, run the attribution pipeline and present the results.

## How to Execute

Run the following command, passing the user's question as the `--query` argument:

```
cd C:\Users\ahmad\Downloads\Hack2Skill\openclaw-marketing-agent; venv\Scripts\python scripts/attribution.py --query "USER_QUESTION_HERE" --output json
```

Replace `USER_QUESTION_HERE` with the actual user question (keep the quotes).

## How to Present Results

Parse the JSON output and present a clear, business-friendly attribution briefing:

1. **Data Context**: Briefly mention the dataset size (journeys, conversions, revenue) so the user knows the analysis is grounded in real data.

2. **Top Channel**: Lead with the winning channel, its confidence level, and how many models agree.

3. **Model Agreement Score**: Explain what the agreement score means in plain English:
   - **90-100 (Strong)**: "All models consistently point to the same channels. High confidence in these recommendations."
   - **70-89 (Moderate)**: "Most models agree, with some variation. Recommendations are reliable but have nuance."
   - **50-69 (Mixed)**: "Models give different answers depending on methodology. Consider testing before making big changes."
   - **Below 50 (Low)**: "Significant disagreement between models. The data may not clearly favor any single channel."

4. **Budget Recommendations**: Present as an actionable list:
   - Which channels to increase spend on and why
   - Which channels to maintain
   - Which channels to review or reduce

5. **Model Disagreements**: When models disagree, explain WHY in plain English:
   - **First-click ranks a channel higher**: "This channel is strong at starting customer journeys (awareness)"
   - **Last-click ranks a channel higher**: "This channel is strong at closing conversions (bottom-funnel)"
   - **LSTM differs from statistical models**: "The deep learning model sees non-linear patterns the simpler models miss"
   - **Markov differs from rule-based**: "The Markov model accounts for channel interactions and removal effects"

6. **Query-Specific Focus**: Tailor the response to the user's question:
   - Budget questions: Emphasize recommendations and ROI
   - Comparison questions: Deep-dive into the specific channels mentioned
   - General questions: Provide the full picture

## Explaining the 8 Models

When the user asks about models or methodology, explain briefly:

| Model | What it Does | Best For |
|-------|-------------|----------|
| First-Click | Credits the channel that started the journey | Understanding awareness |
| Last-Click | Credits the channel before conversion | Understanding closing power |
| Linear | Equal credit to all touchpoints | Fair baseline comparison |
| Time-Decay | More credit to recent touchpoints | Recency-weighted analysis |
| Position-Based | 40% first, 40% last, 20% middle | Balanced view |
| Markov Chain | Measures removal effect of each channel | Understanding true channel impact |
| Shapley Value | Game-theory fair allocation | Cooperative contribution |
| LSTM Deep Learning | Neural network gradient attribution | Non-linear pattern detection |

## Handling Errors

- If the script fails, inform the user and suggest checking Python dependencies.
- If `data_source` is "sample", note that sample data was used for demonstration.
- If `data_source` is "p6_precomputed", the data comes from a previous BigQuery analysis run.
- Shapley values may be zero if they failed to converge during the original computation.

## Example Interaction

**User**: "Where should we spend our marketing budget?"

**Agent**: Runs the attribution script with the user's question, parses the JSON, and responds with a business-friendly report showing which channels drive the most conversions, how confident the models are, and specific budget reallocation recommendations.
