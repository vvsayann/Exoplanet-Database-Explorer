-- Exoplanet Database Explorer — analytical queries
-- Run against the `astronomy` database, table `exoplanets_full`

-- 1. Which detection method found the most planets?
SELECT discoverymethod, COUNT(*) AS planet_count
FROM exoplanets_full
GROUP BY discoverymethod
ORDER BY planet_count DESC;

-- 2. Has the leading detection method changed over time?
SELECT disc_year, discoverymethod, COUNT(*) AS planet_count
FROM exoplanets_full
GROUP BY disc_year, discoverymethod
ORDER BY disc_year, planet_count DESC;

-- 3. Size distribution of confirmed planets
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

-- 4. Which stars host the most confirmed planets?
SELECT hostname, COUNT(*) AS planet_count
FROM exoplanets_full
GROUP BY hostname
HAVING COUNT(*) > 1
ORDER BY planet_count DESC
LIMIT 15;

-- 5. How has average discovery distance changed over time?
SELECT disc_year, ROUND(AVG(sy_dist), 1) AS avg_distance_pc, COUNT(*) AS planet_count
FROM exoplanets_full
WHERE sy_dist IS NOT NULL
GROUP BY disc_year
ORDER BY disc_year;
