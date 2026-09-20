# Emergency Incident Data Analysis

## Project Overview

This project demonstrates a simple end-to-end data analysis workflow using
Python, SQL, SQLite, Pandas and Matplotlib.

The project uses a small synthetic emergency incident dataset created for
demonstration purposes. It is not real DFES operational data.

The objective is to demonstrate how raw incident data can be validated,
cleaned, stored in a relational database, analysed using SQL, and presented
through simple visualisations.

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Matplotlib

## Data Quality Process

Before performing analysis, the dataset was checked for common data quality
issues.

The following issues were identified:

- Missing response time values
- Duplicate records
- Inconsistent incident type formatting
- An impossible negative response time
- An unusually high response time requiring review

The cleaning process:

- Standardised incident type values
- Removed exact duplicate records
- Converted impossible negative response times to missing values
- Flagged unusually high response times for review rather than automatically
  deleting them
- Converted dates into a consistent date format

This approach preserves potentially valid information while identifying
records that may require further validation.

## Database Design

The cleaned data is stored in a SQLite relational database.

Two tables are used:

### locations

Stores unique location information.

- location_id - Primary Key
- location_name

### incidents

Stores incident information.

- incident_id - Primary Key
- date
- location_id - Foreign Key
- incident_type
- response_time_minutes
- units_dispatched
- response_time_review

The incidents and locations tables are connected using location_id.

## SQL Analysis

SQL queries were used to analyse:

- Number of incidents by incident type
- Number of incidents by location
- Average response time by incident type
- Total units dispatched by location

The analysis uses SQL operations including:

- JOIN
- GROUP BY
- COUNT
- AVG
- SUM
- WHERE
- ORDER BY

## Key Findings

Within this synthetic demonstration dataset:

- Fire was the most frequently recorded incident type, with 5 incidents.
- Perth recorded the highest number of incidents, with 4 incidents.
- Hazmat had the highest average response time at 14.00 minutes among
  records included in the response-time analysis.
- Perth recorded the highest total number of units dispatched, with 16 units.

The unusually high response time of 250 minutes was flagged for review and
excluded from the average response-time analysis rather than being
automatically deleted from the database.

## Visualisations

The project produces three visualisations:

### Number of incidents by type
![Number of Incidents by Type](D:\Enggar\Career\Data Analyst DFES\output\incidents_by_type.png)

### Average response time by incident type
![Number of Incidents by Type](D:\Enggar\Career\Data Analyst DFES\output\average_response_time.png)

### Total units dispatched by location
![Number of Incidents by Type](D:\Enggar\Career\Data Analyst DFES\output\units_dispatched_by_location.png)

The charts are saved in the `output` directory.

## Project Structure

    data/
        incidents.csv
        incidents_clean.csv

    database/
        incidents.db

    output/
        incidents_by_type.png
        average_response_time.png
        units_dispatched_by_location.png

    sql/
        create_tables.sql
        analysis.sql

    main.py
    README.md

## Limitations

This project uses a small synthetic dataset and is intended to demonstrate
technical skills and analytical methodology rather than make conclusions
about real emergency service operations.

With a larger operational dataset, the analysis could be extended to examine
time-based trends, geographic patterns, resource utilisation and operational
performance.