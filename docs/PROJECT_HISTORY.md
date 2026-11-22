# SalesScope: project conversation and work history

This is the durable record of the project history available when this file was created on **20 November 2026 (Asia/Kolkata)**. User requests below are quoted verbatim. Work records are summaries of visible actions and results, not a verbatim export of every assistant message or tool call. No inaccessible conversations are included.

Future assistants: append meaningful session entries using the template at the end, and keep `PROJECT_CONTEXT.md` current. Preserve earlier entries; add dated corrections when necessary.

## 20 November 2026 — Initial project request and delivery

### User request (verbatim)

> i want to create a project and my topic is Sales Forecasting and Business Intelligence using Cloud Analytics
>
>
> its masters level project
>
>
> can you build this , also create a proper readme file how it can be hosted

### Starting state and scope

- The workspace was `/Users/rajat/Downloads/project`, initially empty.
- Python 3.9.6 was available. Docker and uv were not available in the initial inspection. No Git repository existed.
- The assistant chose Python/Streamlit and implemented the project in `sales_cloud/`. The user had not specified a framework, real dataset or cloud provider.
- The assistant stated that it would deliver source and hosting instructions without creating cloud resources. Demo data were explicitly labelled synthetic.

### Work completed

- Created Streamlit BI dashboards with revenue/profit/margin/unit metrics, date/region/category filters, trends, category/region comparisons and a calendar heatmap.
- Added seeded synthetic sales data, validated CSV ingestion, explicit missing-day handling and optional GCS ingestion using server credentials.
- Implemented weekly seasonal naive, calendar/lag ridge and histogram gradient boosting forecasts.
- Implemented two chronological validation folds for model selection, a separate final holdout and a refit for future forecasts. Added MAE/RMSE/WAPE, empirical error bands and scenario adjustment.
- Added downloadable filtered sales, forecasts and fold metrics.
- Added a standalone experiment CLI writing comparisons, validation folds, holdout predictions, forecasts and a JSON summary.
- Created the hosting README, methodology/dissertation guide, verification record, Dockerfile, Streamlit configuration, ignore files and GitHub Actions workflow.
- Added an outer quick-start README and packaged `SalesScope_Project.zip`.

### Implementation corrections

- Replaced the forecast action button with a toggle so Streamlit scenario changes preserve visible forecast results during reruns.
- Updated dataframe sizing and kept chart sizing compatible with the pinned Streamlit version.
- The initial dependency download failed under restricted networking; a permitted retry installed dependencies.
- Initial NumPy 2.0.2 produced numerical runtime warnings. The final pin was changed to NumPy 1.26.4, then the tests and CLI experiment were rerun successfully.
- Local bytecode cache permissions initially blocked compile checks; a writable temporary cache location allowed the syntax check to complete.

### Verification and evidence

- `python -m unittest discover -s tests -v` ultimately passed **7 tests**. The existing outer virtual environment was used from the application directory as `../.venv/bin/python`.
- The final local check used a writable temporary `PYTHONPYCACHEPREFIX` and `LOKY_MAX_CPU_COUNT=2` for the original restricted environment. These were execution settings, not application requirements.
- AppTest exercised initial rendering, forecast execution and scenario-slider reruns without application exceptions.
- The CLI command `python experiment.py --horizon 28 --output results/demo` completed on the synthetic demo. Selected model: Calendar ridge; MAE 1301.9566657220914; RMSE 1633.3189362859982; WAPE 4.3649950659543855%.
- Final source/requirements and experiment artifacts were packaged into the ZIP.
- Verified locally with Python 3.9.6. Python 3.11 was configured for Docker/CI but not exercised locally.
- No Docker build, cloud deployment, live GCS read, manual browser visual inspection or GitHub Actions execution was completed.

### Delivery

The assistant delivered links to the ZIP, README and methodology document, stated that all seven tests passed, and stated that data were synthetic and the cloud deployment had not been performed. It supplied this original-workspace run command:

```bash
cd /Users/rajat/Downloads/project/sales_cloud
../.venv/bin/python -m streamlit run app.py
```

### Outstanding inputs

University rubric, real dataset, currency, deployment account and dissertation details had not been supplied. Real-data research and cloud deployment remained future work.

## 20 November 2026 — Durable AI instructions and history

### User request (verbatim)

> also create the codex instruction file if any ai tool is ran in this folder it should get the context and shld be able to get all the history

### Work completed and decisions

- Inspected the existing source layout, README, methodology, verification record and saved experiment summary. A separate read-only review checked the handoff facts and directory-layout caveats.
- Added outer and application-level `AGENTS.md` files. The inner file is canonical; the outer file directs tools into the existing application.
- Added `docs/PROJECT_CONTEXT.md` as the current snapshot and this file as the chronological record, including both available user requests.
- Added thin `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` entry points at both roots so context travels with either the whole workspace or standalone application.
- Added README guidance and a fallback prompt for tools that do not discover instruction files automatically.
- Instructed future assistants to update current context and append meaningful work, exact checks and unresolved items to history without inventing inaccessible conversations or saving secrets.
- Documented that the nested CI workflow requires the application to become the repository root or the workflow to be adapted at the outer root.
- Refreshed the downloadable ZIP to include the instructions and saved context/history.

### Verification and limits

- Ran a Python documentation check across 12 files and 35 local links/imports; all targets existed and both user requests were present. A separate read-only review found no material factual or instruction conflicts.
- Rebuilt `SalesScope_Project.zip` using Python's `zipfile`, checked its integrity and compared every archived file with the current source, including the instructions and context/history. Environments, caches, Git internals and secret-file patterns were excluded.
- Application code and dependencies were unchanged; analytics and dashboard tests were not rerun in this documentation-only follow-up. The earlier seven-test result remains a historical result.
- Instruction discovery depends on each tool and its settings. No claim is made that every AI tool will load these files automatically or expose private chat histories.

## 20 November 2026 — Word case study

### User request (verbatim)

> can you create a word document on the case study of same project ?

### Changes and decisions

- Created `docs/SalesScope_Case_Study.docx`, a twelve-page academic case study with an abstract, hypothetical retail setting, objectives, data contract, architecture, forecasting methods, chronological evaluation, results, BI decisions, proposed cloud hosting, verification, limitations and references.
- Included seven tables, an architecture diagram, a validation comparison chart and a final-holdout chart. Charts use the saved experiment artifacts; no application model was retrained for this task.
- Preserved synthetic-data provenance, unspecified currency units, separate validation and final-holdout measurements, and the historical January 2026 forecast period. Potential business value and proposed cloud deployment are distinguished from measured results.
- Calculated validation MAE reductions and illustrative scenario totals from saved artifacts. A separate read-only reviewer checked numerical and methodological claims without modifying source or rerunning experiments.
- Verified primary forecasting, estimator and cloud documentation and included seven clickable external references alongside project evidence paths.
- Linked the case study from both READMEs, updated the current context, and refreshed the project ZIP to include the final document and this work record.

### Verification

- Used the bundled document runtime at `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python` with python-docx and ReportLab. Document preparation and render intermediates were kept outside the project under `/private/tmp/salesscope_case_study/`.
- Ran the Documents skill's `render_docx.py` with the bundled LibreOffice and Poppler; produced and visually inspected all twelve page images. Re-rendered after adjusting reference links; compared page-image hashes to confirm pages 1 through 11 were unchanged, then inspected the revised reference page.
- Ran `a11y_audit.py` on the final DOCX: zero high, medium or low issues.
- Structural checks verified DOCX ZIP integrity, seven reference hyperlinks, three image descriptions, seven tables and the presented metric values. Local README links and final archive/source consistency were checked.
- The application code, requirements and saved model results were unchanged. Application tests, Docker builds and cloud integration were not rerun for this document-only task.

### Remaining work

- The requested Word case study is complete. Personal or university-specific submission formatting can be added when supplied. Real-data evaluation and deployment verification remain the previously documented research and operational next steps.

## 22 November 2026 — Prepare GitHub source publication

### User request (verbatim)

> can you help me push it to github in a new repo name the repo as per the project topic

The assistant selected `sales-forecasting-business-intelligence-cloud-analytics`. The user then created and supplied https://github.com/RajatJangra2653/sales-forecasting-business-intelligence-cloud-analytics.git.

### Changes and decisions

- Verified the connected account, repository ownership, public visibility and push access. The user-created repository was empty. Preserve its visibility; do not change it based on an earlier private-repository default.
- Initialized `sales_cloud/` as the local Git root on `main`, keeping `.github/workflows/tests.yml` at the repository root without moving the application.
- Added the actual repository URL and fresh-clone instructions to the README and updated context. Kept the local environment and outer project ZIP outside Git.
- Extended ignore rules to exclude `.env.*`, `.DS_Store` and Streamlit secrets from Git or Docker context as appropriate.
- A separate read-only review found no source-publication blockers, common credential-pattern hits or private datasets. Saved results are the documented synthetic demo artifacts.

### Verification and current state

- GitHub metadata and `git ls-remote` confirmed the new repository and its empty state before upload.
- Reran `PYTHONPYCACHEPREFIX=/private/tmp/salesscope-pycache LOKY_MAX_CPU_COUNT=2 ../.venv/bin/python -m unittest discover -s tests -v` from `sales_cloud/`: seven passed, zero failed. The only warning was the expected Streamlit test-mode ScriptRunContext warning.
- Verified ignore behavior for `.env`, `.env.local`, `.streamlit/secrets.toml`, `.venv/bin/python` and `.DS_Store` with `git check-ignore`.
- Source commit preparation is complete; the push outcome and any remote CI result will be recorded after verification. Application code, requirements and saved model results were not changed.

### Authentication before upload

- Created local initial commit `658f7d3` with 28 project files, including the case study, instructions, synthetic artifacts and CI workflow.
- The first HTTPS push was denied because the existing Git credential selected a different account. No matching stored credential or SSH identity was available for the repository owner.
- A write through the connected GitHub integration was also denied with HTTP 403, despite the account metadata reporting repository push permission. No remote source commit was created by either failed attempt.
- Installed the official GitHub CLI through Homebrew and started device sign-in for the repository owner, including workflow access required by the committed test workflow. The user must complete authorization. Device codes and credentials are deliberately excluded from this record.
- Chose not to replace global Git authentication during sign-in, so other repositories can retain their existing account configuration.

### Successful upload

- The user completed GitHub CLI authorization. Verified that the active authenticated account was `RajatJangra2653`.
- Configured a GitHub-specific credential helper only inside the local `sales_cloud/` checkout, keeping other repositories' Git account settings intact.
- Ran `git push -u origin main` successfully. Verified that local HEAD and `git ls-remote origin refs/heads/main` both returned initial source commit `658f7d33a70b0157c4e3fc946936e8d1cdd61e26`.
- Verified the remote top-level source tree, including `.github`, `app.py`, `analytics`, `docs`, `results` and the README. Public repository URL: https://github.com/RajatJangra2653/sales-forecasting-business-intelligence-cloud-analytics.
- GitHub Actions started the `Analytics tests` workflow for that commit: https://github.com/RajatJangra2653/sales-forecasting-business-intelligence-cloud-analytics/actions/runs/44987535668. It was in progress at the first verification checkpoint.
- This publishes project source; no website hosting, cloud deployment or paid resources were created.

### Fresh install compatibility correction

- The first GitHub Actions run completed with six analytics tests passing and the dashboard test failing. A newly resolved PyArrow dependency required NumPy 2 or newer, conflicting with this project's pinned NumPy 1.26.4. This did not occur in the original Python 3.9 environment, which already used PyArrow 21.0.0.
- Added an explicit `pyarrow==21.0.0` requirement to preserve the locally tested combination in fresh Python 3.11 installs. Forecasting logic and saved experiment outputs were unchanged.
- The corrected dependency pin and publication history are being pushed as a follow-up commit; its remote CI outcome will be checked before final delivery.

### Final publication verification

- Pushed corrected source commit `de94667e6df1606e17c298561ee2eee01183a099`. Compared all 28 local file blob hashes against GitHub's recursive tree; every file matched.
- The post-pin local suite passed seven tests with zero failures in 1.703 seconds. GitHub Actions also passed all seven tests on Ubuntu with Python 3.11.18 in 3.793 seconds: https://github.com/RajatJangra2653/sales-forecasting-business-intelligence-cloud-analytics/actions/runs/44987679184.
- Updated verification and context to record the successful remote run. The final follow-up commit changes documentation only and uses `[skip ci]` because the application source and dependency pins have already passed the hosted checks.
- Refreshed the outer workspace ZIP from the final source and documentation, excluding `.git/`, environments, caches and secrets. Source publication is complete; application hosting remains a separate task.

## Template for future entries

Append a new dated section **above this template** after meaningful work:

```markdown
## YYYY-MM-DD (Asia/Kolkata) — Short session title

### User request
Quote the relevant request exactly when available, or label it as a summary.

### Changes and decisions
- Files or behavior changed, purpose and important decisions.

### Verification
- Exact commands/checks actually run and outcomes.
- Checks not run and any blockers; link saved evidence where available.

### Remaining work
- Unresolved items and the next useful action, or state that the requested work is complete.
```
