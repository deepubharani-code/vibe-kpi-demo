# Applied Analytics Mini Project

This project is a beginner-friendly demonstration of a simple data pipeline and KPI reporting.

## How to Run

**Step 1: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Run the ETL script to load data into the database**
```bash
python src/etl_load_sqlite.py
```

**Step 3: Run the KPI script to view city-based analytics**
```bash
python src/kpi_city.py
```

**Step 4: Run the tests**
```bash
pytest
```