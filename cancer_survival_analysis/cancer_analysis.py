import pandas as pd
import plotly.express as px

# DATA LOADING
# ==========================
path = "dataset/rawdataset/13100159.csv"

df = pd.read_csv(path,skiprows=1,sep=',',names=('REF_DATE','GEO','DGUID','Age group','Sex','Primary types of cancer (ICD-O-3)','Characteristics','UOM','UOM_ID','SCALAR_FACTOR','SCALAR_ID','VECTOR','COORDINATE','VALUE','STATUS','SYMBOL','TERMINATED','DECIMALS'))
# ==========================

# DATA CLEANING
# ==========================
#For this specific example we are using REF_DATE, GEO, Age of Group, Sex, Primary types of cancer (ICD-O-3), VALUE, Characteristics, STATUS, SYMBOL
#Re-naming some columns for better clarity 
df = df.rename({'REF_DATE':'Year','GEO':'Region','Age group':'age_group','Primary types of cancer (ICD-O-3)':'cancer_type','VALUE':'survival_rate'},axis=1)

final_columns = [
    'Year',
    'Region',
    'age_group',
    'Sex',
    'cancer_type',
    'UOM',
    'Characteristics',
    'survival_rate',
    'STATUS',
]
#We use .copy() to make sure the data from the original dataframe is not afected
final_df = df[final_columns].copy() 
#Transforming the values of survival_rate to numeric
final_df['survival_rate'] = pd.to_numeric(final_df['survival_rate'],errors='coerce')
#Values in column STATUS are E: estimate, F: unreliable and NaN for Normal - change value from 'NaN' values to 'Normal'
final_df['STATUS']= final_df['STATUS'].fillna('Normal')
# ========================

# DATA PREPARATION
# =========================
filtered_df= final_df[(final_df['Characteristics']== '5-year net survival') & (final_df['UOM']== 'Percentage')].copy()
filtered_df['cancer_type'] = filtered_df['cancer_type'].str.replace(r'\[.*\]','',regex=True)
# =========================

# ANALYSIS
# ==========================
# -------------------
# CANCER SURVIVAL RANKING
# -------------------
cancer_survival_df = filtered_df.groupby(['cancer_type'])['survival_rate'].mean().reset_index()
cancer_survival_df = cancer_survival_df.sort_values('survival_rate',ascending=False) #descending order
cancer_survival_df['rank'] = cancer_survival_df['survival_rate'].rank(ascending=False,method='dense') #create rank column 
# -----------------------
# Sex Differences
#-----------------------
filtered_df = filtered_df[filtered_df['Sex'] != 'Both sexes'] #Delete Sex=both sexes
sex_differences_df = filtered_df.groupby(['cancer_type','Sex'])['survival_rate'].mean().reset_index()
#reshape column sex into  female and male colums using pivot()
sex_differences_df = sex_differences_df.pivot(
    index='cancer_type',
    columns='Sex',
    values='survival_rate'
)
sex_differences_df['differences'] = sex_differences_df['Females'] - sex_differences_df['Males']  
sex_differences_df = sex_differences_df.reset_index()#change it back to number indexes insteand of cancer type
sex_differences_df = sex_differences_df.sort_values(by='differences',ascending=False)
# --------------------
# AGE ANALYSIS
# -------------------
#Clean Age Group data with regular expresions -> (\d+)\s+to\s+(\d+)
df_age = filtered_df[filtered_df['age_group'].str.contains('Total')==False].copy()#deleting Total from the string
df_age[['age_min','age_max']] = df_age['age_group'].str.extract(r'(\d+)\s+to\s+(\d+)') #extracted the numbers of the string
df_age['age_min'] = df_age['age_min'].astype(int) #values to integer
df_age['age_max'] = df_age['age_max'].astype(int)#values to integer
df_age['age_mid'] = (df_age['age_min'] + df_age['age_max'])/2 #mid point of ages
age_group_df = df_age.groupby(['cancer_type','age_mid'])['survival_rate'].mean().reset_index()
age_group_df = age_group_df.sort_values(by='age_mid',ascending=False)
top_cancer_surv_rate = age_group_df.groupby('cancer_type')['survival_rate'].mean().nlargest(5).index
final_age_group_df = age_group_df[age_group_df['cancer_type'].isin(top_cancer_surv_rate)]
final_age_group_df = final_age_group_df.sort_values(by=['cancer_type','age_mid'])
# --------------------
# REGIONAL DIFFERENCES
# --------------------
#Regional Diferences
region_dif_df = filtered_df.groupby(['Region','cancer_type'])['survival_rate'].mean().reset_index()
region_dif_df = region_dif_df.sort_values(by='survival_rate',ascending=True)
region_dif_df = region_dif_df.pivot(
    index='cancer_type',
    columns='Region',
    values='survival_rate'
)
region_dif_df=region_dif_df.reset_index()
#---------------------------
# SURVIvAL TRENDS OVER TIME
# --------------------------
#Analysis overtime
df_year = filtered_df.groupby(['cancer_type','Year'])['survival_rate'].mean().reset_index()
df_year[['start_year','end_year']] = df_year['Year'].str.split('/',expand=True).copy()
df_year['start_year'] = df_year['start_year'].astype(int)
df_year['end_year'] = df_year['end_year'].astype(int)
df_year['year_mid'] = (df_year['start_year']+df_year['end_year'])/2 
df_year = df_year.drop(columns='Year') #Delete column Year is not longer usefull in this example
df_year = df_year.sort_values(by=['cancer_type','year_mid'])
df_year['survival_change']= df_year.groupby('cancer_type')['survival_rate'].diff()#calculate the diff of survival rate to see improvments over the years
df_year['survival_change'] = df_year['survival_change'].fillna(0)#instead of NaN we put 0
#Filter Top 5 cancer type with highest survival change due to many years per cancer type
top_cancer_changes = df_year.groupby('cancer_type')['survival_change'].mean().nlargest(5).index
df_year_top = df_year[df_year['cancer_type'].isin(top_cancer_changes)]
df_year_top = df_year_top.sort_values(by=['cancer_type','year_mid'])
# ==========================

# VISUALIZATIONS
# ==========================
# CANCER SURVIVAL RANKING
graph_can_surv = px.bar(
    data_frame = cancer_survival_df.head(10),
    x='survival_rate',
    y='cancer_type',
    orientation='h',
    color='rank',
    text='survival_rate',
    title='Top 10 Cancers by Average 5-Year Survival Rate',
    labels = {
        'survival_rate':'Survival Rate (%)',
        'cancer_type':'Cancer Type',
        'rank':'Ranking'
    }
)
#graph_can_surv.show()
# SEX DIFFERENCES
#Graphic females vs males by cancer type 
graph_sex_surv_a = px.bar(
    data_frame = sex_differences_df.head(10),
    x = ['Females','Males'],
    y = 'cancer_type',
    barmode='group',
    orientation = 'h',
    title = 'Survival Rate Differences Between Male and Female Patients', #head of the graphic
)
graph_sex_surv_a.update_layout(#Change name of axis title
    xaxis_title = 'Survival Rate (%)',
    yaxis_title = 'Cancer Type'
)
#graph_sex_surv_a.show()
#Graphic difference survival rate female vs male
graph_sex_surv_b = px.bar(
    data_frame = sex_differences_df.head(10),
    x = 'differences',
    y = 'cancer_type',
    orientation = 'h',
    title = 'Difference Between Female and Male Survival Rates', #head of the graphic
    labels = {
        'differences':'Survival Rate Difference (%)',
        'cancer_type':'Cancer Type'
    }
)
#graph_sex_surv_b.show()
# AGE ANALYSIS
graph_age_surv = px.line(
    data_frame=final_age_group_df,
    x= 'age_mid',
    y='survival_rate',
    orientation = 'v',
    color='cancer_type',
    markers=True,
    title = 'Impact of Age on 5-Year Survival Rates',
    labels={
        'age_mid' : 'Age (Mid Point)',
        'survival_rate' : 'Survival Rate (%)',
        'cancer_type' : 'Cancer Type'
    }
)
graph_age_surv.show()
#REGIONAL DIFFERENCES
graph_reg_surv = px.bar(
    data_frame=region_dif_df,
    x='cancer_type',
    y=['Canada','Canada (excluding Quebec)'],  
    barmode='group',
    orientation='v',
    title='Regional Differences in Cancer Survival Rates',
    labels={
        'cancer_type':'Cancer Type',
        'value':'Survival Rate (%)'
    }
)
#graph_reg_surv.show()
# SURVIVAL TRENDS OVER TIME
graph_year_surv = px.line( #Survival rate over the years
    data_frame = df_year_top,
    x= 'year_mid',
    y='survival_rate',
    color='cancer_type',
    title ='Cancer Survival Trends Over Time',
    labels = {
        'year_mid': 'Year Mid Point',
        'survival_rate':'Survival Rate (%)',
        'cancer_type':'Cancer Type'
    }
)
graph_year_surv.update_traces(mode='lines+markers')#ad the dots in the lines
#graph_year_surv.show()

graph_year_surv_change = px.line( #Survival change over the years
    data_frame = df_year_top,
    x= 'year_mid',
    y='survival_change',
    color='cancer_type',
    title ='Changes in Survival Rates Over Time',
    labels = {
        'year_mid': 'Year Mid Point',
        'survival_change':'Survival Change',
        'cancer_type':'Cancer Type'
    }
)
graph_year_surv_change.update_traces(mode='lines+markers')#ad the dots in the lines
#graph_year_surv_change.show()
# ==========================

