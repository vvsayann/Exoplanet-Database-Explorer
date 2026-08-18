"""
Exoplanet Database Explorer — size distribution chart
Connects to the local PostgreSQL 'astronomy' database, buckets planets
by radius into size categories, and plots them as a bar chart.
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

# --- 2. Same query as queries.sql (#3) ---
query = """
    SELECT
        CASE
            WHEN pl_rade < 1.25 THEN 'Earth-sized'
            WHEN pl_rade < 2.0  THEN 'Super-Earth'
            WHEN pl_rade < 6.0  THEN 'Neptune-sized'
            ELSE 'Jupiter-sized'
        END AS size_category,
        COUNT(*) AS planet_count
    FROM exoplanets_full
    WHERE pl_rade IS NOT NULL
    GROUP BY size_category
    ORDER BY planet_count DESC;
"""

# --- 3. Pull into DataFrame ---
df = pd.read_sql(query, engine)
print(df)

# --- 4. Order categories smallest to largest for a sensible x-axis ---
category_order = ["Earth-sized", "Super-Earth", "Neptune-sized", "Jupiter-sized"]
df["size_category"] = pd.Categorical(df["size_category"], categories=category_order, ordered=True)
df = df.sort_values("size_category")

# --- 5. Plot ---
fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.bar(df["size_category"], df["planet_count"], color="tab:orange")
ax.set_ylabel("Planet Count")
ax.set_title("Confirmed Exoplanets by Size Category")

# Label each bar with its count
for bar, count in zip(bars, df["planet_count"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{count}",
            ha="center", va="bottom", fontsize=10)

fig.tight_layout()
plt.savefig("size_distribution.png", dpi=150)
plt.show()
