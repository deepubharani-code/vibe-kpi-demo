import sqlite3
import pandas as pd
import pytest
import io
import sys
import os
from contextlib import redirect_stdout
from pytest import approx

# Add the project root to the Python path to allow for `from src...` imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.kpi_city import city_kpi

# Fixture to set up an in-memory database for testing
@pytest.fixture
def db_connection(monkeypatch):
    # Setup: Create an in-memory database and populate it
    conn = sqlite3.connect(':memory:')
    # Use an absolute path for robustness in tests
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'customers_raw.csv')
    df = pd.read_csv(csv_path)
    df.to_sql('customers_raw', conn, index=False)

    # Monkeypatch the original db_file path to use the in-memory db
    monkeypatch.setattr('src.kpi_city.DB_PATH', ':memory:')

    yield conn

    # Teardown: Close the connection
    conn.close()


def test_city_kpi_happy_path(db_connection):
    """Tests the happy path for the city_kpi function."""
    result = city_kpi("Mumbai", conn=db_connection)

    assert result is not None
    assert result["city"] == "Mumbai"
    assert result["n_customers"] == 4
    assert result["avg_spend"] == approx(60.28, abs=0.01)
    assert result["churn_rate"] == 0.2500


def test_city_kpi_injection_attempt(db_connection):
    """Tests that an SQL injection attempt does not return all rows."""
    result = city_kpi("Mumbai' OR 1=1 --", conn=db_connection)

    # The function should return None for a city that doesn't exist, 
    # which is the case for the injection attempt.
    assert result is None
