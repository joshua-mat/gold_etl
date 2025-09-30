This project implements a lightweight **ETL (Extract, Transform, Load) pipeline** that scrapes daily gold rates from the web, stores them in a database, and generates visualizations for trend analysis.

It demonstrates the core principles of **data engineering** in a compact Python project.

Pipeline Flow

1. **Extract**

   * Uses `requests` + `BeautifulSoup` to scrape gold rates from a public website.

2. **Transform**

   * Cleans raw data (removes suffixes like `9th Sept 2025` → `2025-09-09`).
   * Converts date to ISO format (`YYYY-MM-DD`).
   * Ensures numeric consistency in price values.
   * Keeps only the last 10 days of data.

3. **Load**

   * Loads the transformed data into a local **SQLite database (`gold_rates.sqlite`)**.
   * The pipeline runs daily docker.


**Working on**

4. **Visualize**

   * Reads the database into **Pandas**.
   * Uses **Matplotlib/Seaborn** to plot daily gold price trends.
