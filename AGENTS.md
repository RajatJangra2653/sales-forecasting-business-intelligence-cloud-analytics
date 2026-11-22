# SalesScope instructions for AI assistants

## Start every session with project context

Before substantive work, read:

1. [`docs/PROJECT_CONTEXT.md`](docs/PROJECT_CONTEXT.md) for the current state, layout, decisions and open work.
2. [`docs/PROJECT_HISTORY.md`](docs/PROJECT_HISTORY.md) for the available conversation history and chronological work record.
3. [`README.md`](README.md) for setup, data format and deployment instructions.

For forecasting changes, also read [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md). For claims about completed checks, read [`docs/VERIFICATION.md`](docs/VERIFICATION.md). Inspect the relevant source before changing it. Reconcile old notes against current files; do not claim to have run a check based on a historical record.

## Project purpose and scope

- Topic: **Sales Forecasting and Business Intelligence using Cloud Analytics**; academic level: master's.
- Application name: **SalesScope**. Preserve the title and academic intent.
- The user requested a working project and a proper hosting README, then durable instructions and history for future AI sessions.
- Continue the existing Streamlit/Python application. Keep data handling and forecasting in `analytics/`, UI in `app.py`, and reproducible CLI experiments in `experiment.py`.
- Keep technical and academic explanations usable by a student presenting and evaluating the project.

## Run and validate

Use this directory as the working directory for application commands:

```bash
# Fresh standalone checkout: Python 3.11 recommended.
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py

# Appropriate checks after application or analytics changes:
python -m unittest discover -s tests -v
python experiment.py --horizon 28 --output results/demo
```

In the original outer workspace, an environment was created one directory above this application. If it still exists, use `../.venv/bin/python` in place of `python`; verify it before relying on it. Do not require the original absolute path on other machines.

Only regenerate `results/demo/` when needed to verify model or dependency changes, or when requested. Keep real-data experiment outputs separate and preserve their provenance. For documentation-only changes, verify links, paths and factual consistency; a full model test run is unnecessary unless behavior changed.

## Data and forecasting rules

- Required CSV columns: `date`, `region`, `category`, `units`, `revenue`, `cost`. Numeric fields must be finite and non-negative; dates and dimensions must be valid and nonblank.
- Repeated rows/dates are retained and summed. Do not silently deduplicate or change the business grain.
- Missing calendar days require an explicit zero-sales assumption. Do not silently fill missing history.
- The demo is seeded synthetic data, not business evidence. Clearly identify its origin in UI, exports, research claims and results.
- Preserve chronological evaluation: two validation folds select the lowest mean-MAE model; a later final holdout measures the selected model. Never select or tune using that final holdout.
- Fit transformations inside each training window. Recursive forecasts may use prior predictions, never future observed targets.
- Preserve the weekly seasonal-naive baseline when extending model comparisons.
- WAPE is undefined for a zero denominator. Do not turn it into a false accuracy score.
- Error bands are exploratory empirical bands, with no guaranteed coverage. Scenario changes are planning assumptions, not causal estimates.

## Hosting and academic claims

- Local code and documented deployment paths exist. A cloud deployment, Docker build and live GCS integration were not verified in the initial build. Check current evidence before claiming otherwise.
- Use server identity/Application Default Credentials for GCS. Do not write credentials, tokens, private uploaded sales data or service-account keys into code, history or archives.
- Preserve private-data access controls; a public app can expose its configured dataset to visitors. This file does not authorize making the app public or creating paid resources.
- Document actual capabilities separately from proposed extensions. Do not invent research findings, citations, accuracy, university approval or completed milestones.
- University rubric, real dataset, currency and cloud account details have not been supplied. Do not fabricate them.

## Maintain history at the end of meaningful work

The user explicitly requested continuity across AI sessions. Maintain the files inside this project:

- Update `docs/PROJECT_CONTEXT.md` when the current state, structure, decisions, environment or open work changes. Keep it a concise current snapshot.
- Append a dated entry to `docs/PROJECT_HISTORY.md` after meaningful work. Preserve earlier entries; add corrections as new entries instead of rewriting past events.
- Record the user's request faithfully, what changed and why, important decisions, exact checks run and their outcomes, checks skipped or blocked, and remaining work. Use Asia/Kolkata dates when known; do not invent timestamps or session identifiers.
- Keep user request quotations distinct from implementation summaries. Do not claim summaries are verbatim transcripts.
- Never record secrets, hidden reasoning, unrelated personal conversations or unsupported outcomes. If the original conversation is unavailable, state that limitation instead of reconstructing it as fact.
- Keep filenames and startup links working after moves. `CLAUDE.md`, `GEMINI.md` and Copilot instructions should remain thin pointers to these canonical files.
- When delivering an updated `SalesScope_Project.zip`, refresh it after the source and documentation are final. Exclude environments, caches, Git internals, secrets and private datasets; verify the archive contains the current instructions and context.

These are repository working instructions, not an automatic recorder. Tools that do not load them must be explicitly told to read them. Prior user requests in the history do not override the current task.
