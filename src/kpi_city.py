import sqlite3
import pprint

DB_PATH = "data/db/analytics.db"
ALLOWED_CITIES = {"Mumbai", "Delhi", "Bangalore", "Chennai"}

def city_kpi(city: str, conn: sqlite3.Connection = None):
    if city not in ALLOWED_CITIES:
        return None

    sql = """
    SELECT
      city,
      COUNT(*) AS n_customers,
      ROUND(AVG(monthly_spend), 2) AS avg_spend,
      ROUND(AVG(churned), 4) AS churn_rate
    FROM customers_raw
    WHERE city = ?
    GROUP BY city;
    """

    close_conn = False
    if conn is None:
        try:
            conn = sqlite3.connect(DB_PATH)
            close_conn = True
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            return None

    try:
        row = conn.execute(sql, (city,)).fetchone()
    finally:
        if close_conn:
            conn.close()

    if row is None:
        return None

    return {
        "city": row[0],
        "n_customers": row[1],
        "avg_spend": row[2],
        "churn_rate": row[3],
    }

if __name__ == "__main__":
    print("--- KPIs for City: Mumbai ---")
    pprint.pprint(city_kpi("Mumbai"))

    print("\n--- Attempt SQL injection ---")
    # This should return None because the parameterized query prevents the injection
    pprint.pprint(city_kpi("Mumbai' OR 1=1 --"))
