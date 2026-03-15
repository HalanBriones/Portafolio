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
df = df.rename({'REF_DATE':'year','Sex':'sex','GEO':'region','Age group':'age_group','Primary types of cancer (ICD-O-3)':'cancer_type','VALUE':'survival_rate'},axis=1)

final_columns = [
    'year',
    'region',
    'age_group',
    'sex',
    'cancer_type',
    'UOM',
    'Characteristics',
    'survival_rate',
    'STATUS',
]
final_df = df[final_columns].copy() #.copy() to make sure the data from the original dataframe is not afected
final_df['survival_rate'] = pd.to_numeric(final_df['survival_rate'],errors='coerce') #values of survival_rate to numeric
final_df['STATUS']= final_df['STATUS'].fillna('Normal')#change value from 'NaN' values to 'Normal'
# ========================

# DATA PREPARATION
# =========================
filtered_df= final_df[(final_df['Characteristics']== '5-year net survival') & (final_df['UOM']== 'Percentage')].copy()

filtered_df['cancer_type'] = filtered_df['cancer_type'].str.replace(r'\[.*\]','',regex=True)
filtered_df = filtered_df.drop(columns=['UOM','Characteristics','STATUS']) #Deleting unnecessary columns
#cleaning column year
filtered_df[['start_year','end_year']] = filtered_df['year'].str.split('/',expand=True).copy()
filtered_df['start_year'] = filtered_df['start_year'].astype(int)
filtered_df['end_year'] = filtered_df['end_year'].astype(int)
filtered_df['year_mid'] = (filtered_df['start_year']+filtered_df['end_year'])/2
filtered_df = filtered_df.drop(columns='year')
#cleaning age column
filtered_df = filtered_df[filtered_df['age_group'].str.contains('Total')==False].copy()#deleting Total from the string
filtered_df[['age_min','age_max']] = filtered_df['age_group'].str.extract(r'(\d+)\s+to\s+(\d+)') #extracted the numbers of the string
filtered_df['age_min'] = filtered_df['age_min'].astype(int) #values to integer
filtered_df['age_max'] = filtered_df['age_max'].astype(int)#values to integer
filtered_df['age_mid'] = (filtered_df['age_min'] + filtered_df['age_max'])/2 #mid point of ages
filtered_df = filtered_df.drop(columns='age_group')
#cleaning sex colum
filtered_df = filtered_df[filtered_df['sex'] != 'Both sexes']
# ==========================
filtered_df = filtered_df.groupby(['cancer_type','sex','age_min','age_max','age_mid','region','start_year','end_year','year_mid'])['survival_rate'].mean().reset_index()
filtered_df = filtered_df.sort_values(by='survival_rate',ascending=False)

filtered_df.to_csv('dataset/cancer_surv_clean.csv',sep=',', header=True, encoding='utf-8')

