# SalesScope: current project context

Last updated: **22 November 2026 (Asia/Kolkata)**.

## User intent

Build a master's-level project on **Sales Forecasting and Business Intelligence using Cloud Analytics**, with a proper README explaining hosting. The user then requested an instruction file so future AI tools working in this folder can recover context and project history, followed by a Word case study of the same project.

The working application, portable AI instructions, saved history and a Word case study have been created. No request to deploy the application or create cloud resources has been made.

On 22 November the user requested GitHub publication and created the public repository `RajatJangra2653/sales-forecasting-business-intelligence-cloud-analytics`. The source was pushed successfully to `main`, and the remote head was verified against the local initial commit `658f7d33a70b0157c4e3fc946936e8d1cdd61e26`. The repository includes the application, README, case study, AI instructions, history, synthetic artifacts and test workflow. Website/cloud deployment remains separate from this source upload.

## Where things live

The original workspace is `/Users/rajat/Downloads/project`. Use relative paths for portability:

| Path from outer workspace | Role |
| --- | --- |
| `AGENTS.md` | Outer-workspace instruction entry point |
| `README.md` | Outer-workspace quick start |
| `.venv/` | Existing local development environment; excluded from delivery |
| `SalesScope_Project.zip` | Packaged standalone project |
| `sales_cloud/` | Application and local Git repository root |
| `sales_cloud/AGENTS.md` | Canonical project instructions |
| `sales_cloud/app.py` | Streamlit UI with BI, forecasting, data and methodology tabs |
| `sales_cloud/analytics/data.py` | Synthetic data, validation, daily aggregation and GCS ingestion |
| `sales_cloud/analytics/forecast.py` | Three models, recursive forecasts, temporal evaluation and metrics |
| `sales_cloud/experiment.py` | Command-line experiment and CSV/JSON artifact export |
| `sales_cloud/tests/` | Analytics tests and Streamlit AppTest checks |
| `sales_cloud/results/demo/` | Checked-in synthetic experiment outputs |
| `sales_cloud/docs/` | Methodology, verification, current context and history |
| `sales_cloud/docs/SalesScope_Case_Study.docx` | Twelve-page academic case study with architecture, charts, results and references |
| `sales_cloud/.github/workflows/tests.yml` | CI workflow for a repository rooted at the application directory |

`CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` exist at both the outer workspace and application roots as thin entry points. They point to the same canonical instructions and history.

No Git repository was present during the initial build. On 22 November a Git repository was initialized inside `sales_cloud/`, with `main` as the initial branch. The GitHub repository uses the application contents as its root, so `.github/workflows/tests.yml` is in the correct location. The outer workspace and `.venv/` are outside the checkout. Repository URL: https://github.com/RajatJangra2653/sales-forecasting-business-intelligence-cloud-analytics.

## Implemented system

- **Stack:** Python, Streamlit, pandas, NumPy, scikit-learn, Plotly and google-cloud-storage. Exact direct dependencies are pinned in `requirements.txt`.
- **BI:** revenue, units, gross profit, gross margin, daily trends, region/category charts and calendar heatmap. Filters select regions, categories and dates.
- **Data:** deterministic demo (seed 42), CSV upload (20 MB maximum) or GCS via configured bucket/object and server credentials. The demo covers 2022-01-01 through 2025-12-31 with 13,149 rows, three regions and three categories.
- **Models:** weekly seasonal naive; standardized ridge regression with calendar, trend and lag features; histogram gradient boosting with the same features.
- **Evaluation:** horizons 7/14/28/56 days; at least `90 + 3 × horizon` daily observations; two chronological validation folds for selection and a separate final holdout. Metrics: MAE, RMSE and WAPE.
- **Forecast UI:** actual versus holdout predictions, future forecasts, empirical error bands, scenario revenue adjustment and CSV downloads.
- **Cloud support:** GCS ingestion implementation, Dockerfile and instructions for Streamlit Community Cloud or Google Cloud Run. Cloud Run is an intended deployment target, not an existing verified deployment.
- **Persistence:** uploads and UI forecasts are in memory. The CLI writes artifacts to an explicitly chosen output directory. No implemented data warehouse or scheduled pipeline.

## Decisions and constraints

The initial implementation chose Streamlit for an accessible Python analytics project. It uses a seeded demo so it can run immediately without credentials. Academic rigor comes from chronological validation, baseline comparison and transparent assumptions; a demonstration alone does not establish master's-level research results.

Daily revenue is summed over the selected input rows. Refunds/negative amounts are unsupported. Missing dates require explicit confirmation before zero filling. The November indicator reflects the demo's calendar structure and needs justification for a real dataset. The empirical error band does not guarantee 90% coverage. Scenario adjustments are assumptions, not estimates of causal marketing or pricing effects.

Keep ingestion/analytics separate from the Streamlit UI. Preserve temporal controls when adding features or models. See `METHODOLOGY.md` for the exact fold definitions and research limitations.

## Recorded verification and results

The initial build ran **7 tests successfully** using Python **3.9.6 on macOS**. Python **3.11** is recommended and configured for Docker/CI, but was not tested locally during that build. The suite covers validation, missing dates, reproducibility, seasonal recursion, forecast bounds, zero/short series, final-holdout isolation and dashboard/scenario interactions.

On 22 November, the same seven tests passed again using the existing local environment before GitHub upload. The first GitHub Actions run then exposed a fresh-install dependency conflict: newly resolved PyArrow required NumPy 2, while the project pins NumPy 1.26.4. Requirements now explicitly pin PyArrow 21.0.0, the working local version. After that correction, all seven tests passed both locally and on GitHub Actions with Python 3.11.18. The successful remote run is https://github.com/RajatJangra2653/sales-forecasting-business-intelligence-cloud-analytics/actions/runs/44987679184 for source commit `de94667e6df1606e17c298561ee2eee01183a099`. Forecasting logic and saved results were unchanged.

The 28-day synthetic CLI experiment selected **Calendar ridge**:

| Final holdout metric | Recorded value |
| --- | --- |
| MAE | 1301.9566657220914 |
| RMSE | 1633.3189362859982 |
| WAPE (%) | 4.3649950659543855 |

These are historical **synthetic-data** measurements, not real-world accuracy. Evidence: `results/demo/summary.json` and `docs/VERIFICATION.md`. The follow-up instruction-file task did not rerun the model or application tests because it changed documentation only.

Initial checks did not include a manual browser visual review, Docker image build, cloud deployment, live authenticated GCS read or actual GitHub Actions run. Do not imply these succeeded.

The Word case study uses these saved artifacts and includes synthetic-data provenance, a hypothetical retail setting, validation comparisons, final-holdout results, an architecture diagram and two charts. It distinguishes proposed hosting and potential business benefits from measured evidence. The document was rendered and visually reviewed across all 12 pages, and its accessibility audit reported no high, medium or low issues. Application models and tests were not rerun for this document-only task. See the latest history entry for its checks.

## Run commands in this original workspace

From the outer workspace:

```bash
cd sales_cloud
../.venv/bin/python -m streamlit run app.py
../.venv/bin/python -m unittest discover -s tests -v
../.venv/bin/python experiment.py --horizon 28 --output results/demo
```

For a new machine, create an application-local environment using the README rather than relying on the outer `.venv/`. The initial build moved NumPy from 2.0.2 to **1.26.4** after numerical warnings; preserve the final requirements pin unless a tested change justifies updating it.

For Git operations in the original checkout, `origin` points to the GitHub repository above and local `main` tracks `origin/main`. GitHub CLI was installed through Homebrew and authorized by the user as `RajatJangra2653`. Only this checkout's GitHub credential helper was configured to use `/opt/homebrew/bin/gh auth git-credential`; other repositories retain their existing Git credential configuration. Do not rely on that machine-specific helper path in a new clone.

## Open work and missing inputs

No implementation work is currently blocked. The following remain possible next steps, not completed features or user commitments:

- Obtain the university rubric, licensed real dataset, business currency/cost definitions and academic submission requirements.
- Evaluate real data and write a dissertation with verified academic sources.
- Build/test Docker and deploy to a user-selected cloud account if requested.
- Verify private GCS ingestion with the actual runtime identity and dataset.
- Add authentication, persistent forecast storage, scheduling, monitoring, external drivers or further models if requested.

No university name, supervisor, submission deadline, real dataset, cloud project ID or hosting budget has been supplied.

## Continuity

Read `PROJECT_HISTORY.md` after this snapshot for the original user requests and work record. Update this file when current facts change; append chronological history separately. Repository documents can preserve only material saved here. They do not recover inaccessible chats or automatically record every future tool session.
