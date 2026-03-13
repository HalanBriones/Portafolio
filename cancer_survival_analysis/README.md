****Overview****

This project analyzes 5-year net survival rates for various types of cancer in Canada using publicly available data. The analysis explores patterns across cancer type, sex, age groups, region, and trends over time, providing insights into survival differences and improvements.

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

Identify top cancer types by survival rate

Explore sex-based survival differences

Examine age-specific survival trends

Compare regional survival rates

Analyze trends over time and changes in survival

****Requirements****
- Python 3 
Libraries: pandas, numpy, plotly

It is recommended to create a virtual environment to run the code

****Visualizations****

Top 10 Cancers by Average 5-Year Survival Rate – Bar chart showing the cancers with highest average survival rates.

Sex-Based Survival Differences by Cancer Type – Grouped bar chart comparing male vs female survival rates.

Difference Between Female and Male Survival Rates – Bar chart highlighting cancers with largest sex-based differences.

Survival Rate by Age Midpoint – Line chart showing survival rate trends across age midpoints for different cancers.

Regional Differences in Survival Rates – Bar chart comparing survival rates across regions.

Survival Trends Over Time – Line chart showing 5-year survival rates over multiple years for cancers with the highest changes.

Change in Survival Rates Over Time – Line chart highlighting year-to-year changes in survival rates.

****Insights****

Cancer Type Ranking: Identify cancers with highest and lowest survival rates.

Sex Differences: Reveal disparities between male and female patients.

Age Analysis: Show how survival rates change across age groups.

Regional Differences: Highlight variations between provinces/regions.

Trends Over Time: Capture improvements or declines in survival rates across years.

This project demonstrates data cleaning, analysis, visualization, and insight extraction