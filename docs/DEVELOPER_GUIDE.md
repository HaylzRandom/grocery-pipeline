# 👩‍💻 Developer Guide

## ✅ Validation

The `validate.py` step ensures input files are usable before processing:

- Missing file -> raises `FileNotFoundError`
- 0-byte file -> raises `ValueError("{file_name} is empty")`
- Header-only CSV -> raises `ValueError("{file_name} is empty")`
- Valid file -> returns `True`

## 🧪 Tests

- **Unit Tests**

  - `test_extract.py` -> checks SQLite + Parquet loading
  - `test_transform.py` -> checks cleaning, missing values, filtering
  - `text_validate.py` -> checks valid, missing, empty, and 0-byte files

- **Integration Test**

  - `test_pipeline.py` -> (`test_pipeline_dry_run`) runs the full ETL and asserts logs include _“Pipeline finished successfully”_.

- Logs are captured with `caplog` in tests to verify behaviour.

## ⚙️ CI/CD

This project uses GitHub Actions for continuous integration and delivery.

- GitHub Actions workflow triggers on:

  - **CI**
    - Every **push** (any branch)
    - Every **pull request** (any branch)
  - **Tests**
    - Every **push** (any branch)
    - Every **pull request** (any branch)
  - **Full Run**
    - Every **push** (any branch)
    - Every **pull request to `main`**
    - **Scheduled** weekly on Sunday at 23:00 UTC

- Each of the jobs do as follows:
  - **CI** -> Build Docker images for the pipeline and tests
  - **Tests** - Runs unit and integration tests with pytest inside Docker Compose
  - **Full Run** -> Runs full pipeline from start to finish

Jobs use Docker compose to build the environment and run tests

[![CI](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/ci.yml)
[![Unit Tests](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/tests.yml)
[![Full Run](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/full-run.yml/badge.svg)](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/full-run.yml)

## 📜 Smoke Test Bash File

This bash file is useful for quickly testing on local deployment.

The script will:

- Clean out any old data and logs
- Build the docker image
- Run the full pipeline
- Check the outputs
- Run the tests
- Confirm completion
