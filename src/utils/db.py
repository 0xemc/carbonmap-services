import os
import psycopg2

POSTGRES_URL = os.environ.get("API_NEON_URL")

# Connect to the PostgreSQL database
conn = psycopg2.connect(POSTGRES_URL)

# Create a cursor object
cur = conn.cursor()

# Execute SQL commands to retrieve the current time and version from PostgreSQL
cur.execute("SELECT NOW();")
time = cur.fetchone()[0]

cur.execute("SELECT version();")
version = cur.fetchone()[0]

# Close the cursor and connection
cur.close()
conn.close()

# Print the results
print("Current time:", time)
print("PostgreSQL version:", version)
