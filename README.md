# Marketing and E-Commerce Analytics

This project provides an end-to-end data pipeline and analytics suite for e-commerce and marketing data. It covers everything from raw data ingestion and cleaning to advanced data modeling and behavioral analysis.

## Data Source
The dataset used in this project is the **Marketing and E-commerce Analytics Dataset** from Kaggle. It contains millions of event-level interactions across browsing, clicking, carting, and purchasing, and it also includes campaign exposure and experiment assignments.

- **Source URL:** [Kaggle - Marketing and E-commerce Analytics Dataset](https://www.kaggle.com/datasets/geethasagarbonthu/marketing-and-e-commerce-analytics-dataset/data)

## Overview
The goal of this project is to transform raw e-commerce CSV files into a structured, queryable data warehouse environment (DuckDB) and perform deep-dive analytics on customer behavior, marketing funnel performance, and A/B test results.

## Project Structure

### 1. Ingestion & Format Cleaning
The ingestion process is automated via `scripts/ingest_data.py`. Key operations include:
- **Standardization:** Column names are normalized to snake_case.
- **String Sanitization:** Trimming whitespace, standardizing ID formats to uppercase, and applying Title Case to categorical values.
- **Null Handling:** Mapping various "None/NaN" representations to a consistent "Unknown" state.
- **Type Casting:** Automatic detection and conversion of date and timestamp columns.
- **DuckDB Integration:** Loading cleaned DataFrames into a local DuckDB database (`database/ecommerce.duckdb`) for high-performance analytical queries.

### 2. Data Modeling
Beyond raw table ingestion, the pipeline implements a "One Big Table" (OBT) approach for analytical convenience:
- **`v_marketing_funnel` View:** A pre-joined view that combines events, customer demographics, and product metadata. This serves as the primary source for funnel and conversion analysis.

### 3. Analytics & Notebooks
The `notebooks/` directory contains detailed analyses:
- **Funnel Analysis (`funnel_analysis.ipynb`):** Investigates the customer journey from event to purchase, identifying drop-off points and conversion rates across different channels.
- **A/B Test Analysis (`ab_test_analysis.ipynb`):** Evaluates marketing campaign performance (e.g., Campaign 33) by comparing Control and Variant groups.
  - **Metrics:** Conversion Rate, Average Order Value (AOV), Average Revenue per User (ARPU) and Order Value(OV).
  - **Statistical Significance:** Employs Chi-square tests for categorical conversion data and Welch's T-tests for continuous revenue metrics to determine if observed differences are statistically significant.

---

## Getting Started
1. Ensure you have the raw CSV files in the `data/` directory.
2. Run the ingestion script:
   ```bash
   python scripts/ingest_data.py
   ```
3. Explore the analytics notebooks in `notebooks/`.
