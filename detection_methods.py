"""
Exoplanet Database Explorer — detection method chart
Connects to the local PostgreSQL 'astronomy' database, pulls planet
counts by detection method, and plots them as a horizontal bar chart.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Connection details ---
DB_USER = "postgres"
DB_PASSWORD = os.environ.get("ASTRONOMY_DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "astronomy"

if not DB_PASSWORD:
    raise RuntimeError(
        "ASTRONOMY_DB_PASSWORD environment variable not set. "
        "Run: $env:ASTRONOMY_DB_PASSWORD = \"your_password\"  (PowerShell)"
    )

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --- 2. Same query as queries.sql (#1) ---
query = """
    SELECT discoverymethod, COUNT(*) AS planet_count
    FROM exoplanets_full
    GROUP BY discoverymethod
    ORDER BY planet_count DESC;
"""

# --- 3. Pull into DataFrame ---
df = pd.read_sql(query, engine)
print(df)

# --- 4. Plot ---
fig, ax = plt.subplots(figsize=(9, 6))

# Horizontal bars, sorted so the biggest method is on top
ax.barh(df["discoverymethod"][::-1], df["planet_count"][::-1], color="tab:blue")
ax.set_xlabel("Planets Found")
ax.set_title("Confirmed Exoplanets by Detection Method")

# Label each bar with its count
for i, count in enumerate(df["planet_count"][::-1]):
    ax.text(count, i, f" {count}", va="center", fontsize=9)

fig.tight_layout()
plt.savefig("detection_methods.png", dpi=150)
plt.show()
