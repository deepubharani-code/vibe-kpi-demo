import pandas as pd
import sqlite3

# Define file paths
csv_file = 'data/raw/customers_raw.csv'
db_file = 'data/db/analytics.db'
table_name = 'customers_raw'

# Read the CSV file
df = pd.read_csv(csv_file)

# Establish a connection to the SQLite database
conn = sqlite3.connect(db_file)

# Load the DataFrame into the SQLite table
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print(f"Successfully loaded {len(df)} rows from {csv_file} to {table_name} in {db_file}")
