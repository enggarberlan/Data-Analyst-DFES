-- 1. Number of incidents by type
SELECT
    incident_type,
    COUNT(*) AS total_incidents
FROM incidents
GROUP BY incident_type
ORDER BY total_incidents DESC;


-- 2. Number of incidents by location
SELECT
    l.location_name,
    COUNT(i.incident_id) AS total_incidents
FROM incidents AS i
JOIN locations AS l
    ON i.location_id = l.location_id
GROUP BY l.location_name
ORDER BY total_incidents DESC;


-- 3. Average response time by incident type
SELECT
    incident_type,
    ROUND(AVG(response_time_minutes), 2) AS average_response_time
FROM incidents
WHERE response_time_review = 0
GROUP BY incident_type
ORDER BY average_response_time DESC;


-- 4. Total units dispatched by location
SELECT
    l.location_name,
    SUM(i.units_dispatched) AS total_units_dispatched
FROM incidents AS i
JOIN locations AS l
    ON i.location_id = l.location_id
GROUP BY l.location_name
ORDER BY total_units_dispatched DESC;