# Verification record

Verified locally on 20 November 2026 using Python 3.9.6 on macOS with the pinned direct dependencies in requirements.txt. Python 3.11 is the recommended deployment runtime and the configured CI runtime; it was not available locally.

- Seven automated tests pass, including Streamlit AppTest rendering, forecast execution and scenario-slider reruns.
- Analytics checks cover schema failures, zero/missing data, reproducibility, seasonal recursion and final-holdout isolation.
- The CLI experiment completed for the synthetic dataset; artifacts are in results/demo.
- Selected model: Calendar ridge. Synthetic final-holdout MAE: 1301.96; RMSE: 1633.32; WAPE: 4.36%. These are demonstration results, not real-company evidence.
- Streamlit AppTest provides application interaction checks; no manual browser visual inspection was performed.
- Docker image build, hosted deployment and authenticated GCS reads were not executed locally. Docker and cloud credentials were unavailable. Hosting instructions reference official documentation.
- The bare-mode ScriptRunContext warning emitted by Streamlit's test runner does not indicate an application failure.

## GitHub publication check on 22 November 2026

- Reran `python -m unittest discover -s tests -v` from the application directory using the existing outer virtual environment, `PYTHONPYCACHEPREFIX=/private/tmp/salesscope-pycache` and `LOKY_MAX_CPU_COUNT=2`.
- Seven tests passed, zero failed, in 1.901 seconds. Only the expected Streamlit bare-mode ScriptRunContext warning was emitted.
- Application source, dependencies and saved experiment outputs were unchanged. This local check does not verify cloud deployment or an actual GitHub Actions execution.
