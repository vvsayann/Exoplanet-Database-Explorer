# Exoplanet Database Explorer

A PostgreSQL database of real confirmed exoplanet data from the NASA Exoplanet
Archive, with analytical SQL queries answering genuine astronomy questions,
plus a Python/pandas script for visualizing trends.

## Data source

[NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu) —
*Planetary Systems Composite Parameters* (`pscomppars`) table, the current
maintained table of ~6,300 confirmed exoplanets (as of download date).

## Schema

Table `exoplanets_full` in a PostgreSQL database named `astronomy`:

| Column | Type | Description |
|---|---|---|
| `pl_name` | VARCHAR(100) PK | Planet name |
| `hostname` | VARCHAR(100) | Host star name |
| `discoverymethod` | VARCHAR(50) | Detection method (Transit, RV, etc.) |
| `disc_year` | INTEGER | Year of discovery |
| `pl_controv_flag` | SMALLINT | 0/1 controversial-detection flag |
| `pl_orbper`, `pl_orbpererr1`, `pl_orbpererr2`, `pl_orbperlim` | NUMERIC/SMALLINT | Orbital period (days) + uncertainty + limit flag |
| `pl_rade`, `pl_radeerr1`, `pl_radeerr2`, `pl_radelim` | NUMERIC/SMALLINT | Planet radius (Earth radii) + uncertainty + limit flag |
| `sy_dist`, `sy_disterr1`, `sy_disterr2` | NUMERIC | System distance (parsecs) + uncertainty |

## Analytical queries

- Which detection method has found the most planets?
- How has the leading detection method changed over time? (Radial Velocity → Transit, coinciding with Kepler's 2009 launch)
- What's the size distribution of confirmed planets? (Reveals detection bias toward large planets)
- Which stars host the most confirmed planets? (Surfaces known systems like Kepler-90/KOI-351 and TRAPPIST-1)
- How has the average discovery distance changed over time?

See `queries.sql` for the full query set.

## Python / visualization

`exoplanet_distance_trend.py` connects to the database via SQLAlchemy,
pulls the distance-over-time query into a pandas DataFrame, and plots it
against the count of planets found per year.

### Setup

```powershell
py -m pip install psycopg2-binary sqlalchemy pandas matplotlib
$env:ASTRONOMY_DB_PASSWORD = "your_postgres_password"
py exoplanet_distance_trend.py
```

## Tools used

PostgreSQL 18, pgAdmin 4, Python (pandas, SQLAlchemy, matplotlib)
