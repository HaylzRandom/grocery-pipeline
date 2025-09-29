# 🛒 Grocery Store ETL Pipeline

A lightweight, containerised **_ETL pipeline_** built with Python, pandas, and SQLite.
The project demonstrates real-world data engineering practices: ETL structure, logging, validation, testing, and CI/CD with GitHub Actions.

[![CI](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/ci.yml)
[![Unit Tests](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/tests.yml)
[![Full Run](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/full-run.yml/badge.svg)](https://github.com/haylzrandom/grocery-pipeline/actions/workflows/full-run.yml)

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Sqlite](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/Github%20Actions-282a2e?style=for-the-badge&logo=githubactions&logoColor=367cfe)

## 🔄 ETL Flow Overview

```mermaid
flowchart LR
    A[CSV: Grocery Sales] -->|Load| B[(SQLite Database)]
    B -->|Extract| C[Pandas DataFrame]
    D[Parquet: Extra Data] -->|Merge| C
    C -->|Transform & Clean| E[Cleaned DataFrame]
    E -->|Aggregate| F[Monthly Avg Sales]
    F -->|Save| G[CSV Outputs]
    C -->|Log| H[(Logs)]
```

## 🚀 Features

- Extracts CSV + Parquet grocery data into SQLite
- Cleans, transform, and aggregates with pandas
- Structured logging (console + file)
- Data validation (missing/empty file checks)
- Unit and integration tests with pytest
- Docker and Docker compose for reproducibility
- CI/CD with Github Actions

## 🐳 Running the pipeline

### Build containers

```bash
docker compose build
```

### Run pipeline

```bash
docker compose run --rm pipeline
```

### Dry run (no write out, just logs)

```bash
docker compose run --rm dry-run
```

Outputs:

- `data/clean_data.csv`

- `data/agg_data.csv`

- `logs/pipeline.log`

## 🧪 Testing

Run all tests:

```bash
docker compose run --rm tests
```

## Documentation

For further examples and details of the project:

- [📜 Example Logs](docs/LOG_EXAMPLES.md)
- [📊 Example Outputs](docs/OUTPUTS.md)
- [👩‍💻 Developer Guide](docs/DEVELOPER_GUIDE.md)
