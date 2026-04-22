****Overview****

This project analyzes 5-year net survival rates for various types of cancer in Canada using publicly available data. The project started with data cleaning and exploratory analysis in Python, and was later extended using Power BI to create interactive dashboards.

Dataset
Source: Statistics Canada (Public Dataset: 13100159.csv)

Key Columns Used:
- REF_DATE – Year or range of years
- GEO – Region
- Age group – Age range
- Sex – Male / Female / Both Sexes
- Primary types of cancer (ICD-O-3) – Cancer type
- Characteristics – Type of measurement (we focus on 5-year net survival)
- VALUE – Survival rate in percentage
- Size: X rows, covering multiple years, regions, and age groups

****Objective****

- Identify cancer types with the highest survival rates
- Analyze differences between male and female patients
- Understand how survival changes across age groups
- Compare survival rates across regions
- Explore trends and improvements over time

****Requirements****
- Python 3 
Libraries: pandas, numpy, plotly
- Power BI (for dashboard development)
It is recommended to create a virtual environment to run the code

****Workflow****
1. Data Cleaning & Preparation (Python)
  - Filtered relevant variables (5-year survival rates)
  - Handled missing and inconsistent values
  - Standardized data formats for analysis
2. Exploratory Data Analysis (Python)
  - Created multiple visualizations using Plotly
  - Explored relationships between survival rates and key variables
  - Identified initial patterns and trends
3. Data Visualization (Power BI)
  - Exported cleaned dataset to CSV
  - Built interactive dashboards
  - Added filters (year, region, sex) to improve usability
  - Focused on making insights easier to explore

****Visualizations using Plotly****

Top 10 Cancers by Average 5-Year Survival Rate – Bar chart showing the cancers with highest average survival rates.

Sex-Based Survival Differences by Cancer Type – Grouped bar chart comparing male vs female survival rates.

Difference Between Female and Male Survival Rates – Bar chart highlighting cancers with largest sex-based differences.

Survival Rate by Age Midpoint – Line chart showing survival rate trends across age midpoints for different cancers.

Regional Differences in Survival Rates – Bar chart comparing survival rates across regions.

Survival Trends Over Time – Line chart showing 5-year survival rates over multiple years for cancers with the highest changes.

Change in Survival Rates Over Time – Line chart highlighting year-to-year changes in survival rates.

****Key Insights****

- Survival rates vary significantly depending on the type of cancer
- Age has a strong impact on survival, with lower rates in older groups
- Some cancers show consistent improvement over time, while others remain relatively stable
- Differences between male and female survival rates vary by cancer type
- Regional variations exist, though patterns are generally consistent

This project was part of my transition into data analysis. Working in a healthcare environment motivated me to explore real-world datasets and better understand how data can be used to identify trends and support decision-making.
