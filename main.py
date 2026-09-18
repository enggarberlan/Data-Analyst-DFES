# ==========================================
# 1. IMPORT LIBRARIES
# ==========================================
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ==========================================
# 2. LOAD AND PROFILE RAW DATA
# ==========================================
df = pd.read_csv("data/incidents.csv")

print("=== DATASET OVERVIEW ===")
print(df.head())

print("\n=== DATASET INFORMATION ===")
df.info()

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== DUPLICATE ROWS ===")
print(df.duplicated().sum())

# ==========================================
# 3. DATA CLEANING AND QUALITY CHECKS
# ==========================================
# Create a copy for cleaning
clean_df = df.copy()

print("\n=== STARTING DATA CLEANING ===")

# Standardise incident type
clean_df["incident_type"] = clean_df["incident_type"].str.strip().str.title()

print("\nIncident types after standardisation:")
print(clean_df["incident_type"].unique())

# Remove exact duplicate rows
before_duplicates = len(clean_df)

clean_df = clean_df.drop_duplicates()

after_duplicates = len(clean_df)

print("\nDuplicates removed:")
print(before_duplicates - after_duplicates)

# Replace impossible response times with missing values
clean_df.loc[
    clean_df["response_time_minutes"] <= 0,
    "response_time_minutes"
] = pd.NA

# Flag unusually high response times for review
clean_df["response_time_review"] = (
    clean_df["response_time_minutes"] > 120
)

clean_df["date"] = pd.to_datetime(
    clean_df["date"],
    errors="coerce"
)

print("\n=== CLEAN DATA SUMMARY ===")
print(clean_df)

print("\nMissing values after cleaning:")
print(clean_df.isnull().sum())

print("\nDuplicate rows after cleaning:")
print(clean_df.duplicated().sum())

print("\nRecords requiring response time review:")
print(clean_df[clean_df["response_time_review"] == True])

clean_df.to_csv(
    "data/incidents_clean.csv",
    index=False
)

print("\nClean dataset saved to data/incidents_clean.csv")

# ==========================================
# 4. PREPARE RELATIONAL DATA
# ==========================================
print("\n=== CREATING LOCATIONS DATA ===")

locations_df = (
    clean_df[["location"]]
    .drop_duplicates()
    .sort_values("location")
    .reset_index(drop=True)
)

locations_df["location_id"] = locations_df.index + 1

locations_df = locations_df.rename(
    columns={"location": "location_name"}
)

print("\n=== LOCATIONS TABLE ===")
print(locations_df)

incidents_db_df = clean_df.merge(
    locations_df,
    left_on="location",
    right_on="location_name"
)

print("\n=== INCIDENTS WITH LOCATION ID ===")
print(
    incidents_db_df[
        ["incident_id", "location", "location_id", "incident_type"]
    ]
)

# ==========================================
# 5. CREATE AND POPULATE SQLITE DATABASE
# ==========================================
print("\n=== CREATING DATABASE ===")

conn = sqlite3.connect("database/incidents.db")

with open("sql/create_tables.sql", "r") as sql_file:
    sql_script = sql_file.read()

conn.executescript(sql_script)

print("Database tables created successfully.")


# PREPARE INCIDENTS DATA FOR DATABASE
incidents_db_df = incidents_db_df[
    [
        "incident_id",
        "date",
        "location_id",
        "incident_type",
        "response_time_minutes",
        "units_dispatched",
        "response_time_review"
    ]
].copy()

# Convert date to YYYY-MM-DD format
incidents_db_df["date"] = (
    incidents_db_df["date"].dt.strftime("%Y-%m-%d")
)

# Convert Boolean values to 0 and 1 for SQLite
incidents_db_df["response_time_review"] = (
    incidents_db_df["response_time_review"].astype(int)
)

# Clear old data so the program can be run multiple times
conn.execute("DELETE FROM incidents")
conn.execute("DELETE FROM locations")

# Insert location data
locations_df.to_sql(
    "locations",
    conn,
    if_exists="append",
    index=False
)

# Insert incident data
incidents_db_df.to_sql(
    "incidents",
    conn,
    if_exists="append",
    index=False
)

conn.commit()

print("\nData inserted into database successfully.")

# ==========================================
# 6. VERIFY DATABASE
# ==========================================
print("\n=== DATABASE VERIFICATION ===")

query = """
SELECT
    i.incident_id,
    i.date,
    l.location_name,
    i.incident_type,
    i.response_time_minutes,
    i.units_dispatched,
    i.response_time_review
FROM incidents AS i
JOIN locations AS l
    ON i.location_id = l.location_id
ORDER BY i.incident_id;
"""

result = pd.read_sql_query(query, conn)

print(result)


# ==========================================
# 7. SQL DATA ANALYSIS
# ==========================================
print("\n=== SQL DATA ANALYSIS ===")

# 1. Number of incidents by type
query_incident_type = """
SELECT
    incident_type,
    COUNT(*) AS total_incidents
FROM incidents
GROUP BY incident_type
ORDER BY total_incidents DESC;
"""

incidents_by_type = pd.read_sql_query(
    query_incident_type,
    conn
)

print("\nIncidents by type:")
print(incidents_by_type)

# 2. Number of incidents by location
query_location = """
SELECT
    l.location_name,
    COUNT(i.incident_id) AS total_incidents
FROM incidents AS i
JOIN locations AS l
    ON i.location_id = l.location_id
GROUP BY l.location_name
ORDER BY total_incidents DESC;
"""

incidents_by_location = pd.read_sql_query(
    query_location,
    conn
)

print("\nIncidents by location:")
print(incidents_by_location)

# 3. Average response time by incident type
query_response_time = """
SELECT
    incident_type,
    ROUND(AVG(response_time_minutes), 2) AS average_response_time
FROM incidents
WHERE response_time_review = 0
GROUP BY incident_type
ORDER BY average_response_time DESC;
"""

response_by_type = pd.read_sql_query(
    query_response_time,
    conn
)

print("\nAverage response time by incident type:")
print(response_by_type)

# 4. Total units dispatched by location
query_units = """
SELECT
    l.location_name,
    SUM(i.units_dispatched) AS total_units_dispatched
FROM incidents AS i
JOIN locations AS l
    ON i.location_id = l.location_id
GROUP BY l.location_name
ORDER BY total_units_dispatched DESC;
"""

units_by_location = pd.read_sql_query(
    query_units,
    conn
)

print("\nTotal units dispatched by location:")
print(units_by_location)


# ==========================================
# DATA VISUALISATION
# ==========================================

print("\n=== CREATING VISUALISATIONS ===")

# Chart 1: Incidents by type
plt.figure(figsize=(8, 5))

plt.bar(
    incidents_by_type["incident_type"],
    incidents_by_type["total_incidents"]
)

plt.title("Number of Incidents by Type")
plt.xlabel("Incident Type")
plt.ylabel("Number of Incidents")

plt.tight_layout()

plt.savefig(
    "output/incidents_by_type.png"
)

plt.close()

print("Created: output/incidents_by_type.png")

# Chart 2: Average response time by incident type
plt.figure(figsize=(8, 5))

plt.bar(
    response_by_type["incident_type"],
    response_by_type["average_response_time"]
)

plt.title("Average Response Time by Incident Type")
plt.xlabel("Incident Type")
plt.ylabel("Average Response Time (Minutes)")

plt.tight_layout()

plt.savefig(
    "output/average_response_time.png"
)

plt.close()

print("Created: output/average_response_time.png")

# Chart 3: Total units dispatched by location
plt.figure(figsize=(8, 5))

plt.bar(
    units_by_location["location_name"],
    units_by_location["total_units_dispatched"]
)

plt.title("Total Units Dispatched by Location")
plt.xlabel("Location")
plt.ylabel("Units Dispatched")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "output/units_dispatched_by_location.png"
)

plt.close()

print("Created: output/units_dispatched_by_location.png")

conn.close()