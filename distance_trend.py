

import os
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

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


query = """
    SELECT disc_year, ROUND(AVG(sy_dist), 1) AS avg_distance_pc, COUNT(*) AS planet_count
    FROM exoplanets_full
    WHERE sy_dist IS NOT NULL
    GROUP BY disc_year
    ORDER BY disc_year;
"""


df = pd.read_sql(query, engine)
print(df.head())
print(f"\nTotal years: {len(df)}")


fig, ax1 = plt.subplots(figsize=(10, 6))


ax1.plot(df["disc_year"], df["avg_distance_pc"], color="tab:blue", marker="o", label="Avg distance (pc)")
ax1.set_xlabel("Discovery Year")
ax1.set_ylabel("Average Distance (pc)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")


ax2 = ax1.twinx()
ax2.bar(df["disc_year"], df["planet_count"], color="tab:orange", alpha=0.25, label="Planets found")
ax2.set_ylabel("Planets Found", color="tab:orange")
ax2.tick_params(axis="y", labelcolor="tab:orange")

plt.title("Average Discovery Distance vs. Year (Confirmed Exoplanets)")
fig.tight_layout()
plt.savefig("distance_trend.png", dpi=150)
plt.show()
