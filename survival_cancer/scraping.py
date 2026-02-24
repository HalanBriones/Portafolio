import pandas as pd

path = "dataset/13100159.csv"


df = pd.read_csv(path,skiprows=1,sep=',',names=('REF_DATE','GEO','DGUID','Age group','Sex','Primary types of cancer (ICD-O-3)','Characteristics','UOM','UOM_ID','SCALAR_FACTOR','SCALAR_ID','VECTOR','COORDINATE','VALUE','STATUS','SYMBOL','TERMINATED','DECIMALS'))

#For this specific example we are using REF_DATE, GEO, Age of Group, Sex, Primary types of cancer (ICD-O-3), VALUE, Characteristics, STATUS, SYMBOL

#Re-naming some of the columns
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

#settings for better display
pd.set_option('display.max_columns', None)
pd.set_option('display.width',1000)
pd.set_option("display.max_colwidth", None)

#print(final_df.head(10)) #First x values
#print(df.tail(2)) #Last x values

#**************INSIGHTS****************#

#Insights to dataframe to later create graphics
#Cancer-Type Survival in 5 year net survival

#Filter and leave only where Charasteristics = 5 year net survival and also only keep UOM = percenteg

filtered_df= final_df[(final_df['Characteristics']== '5-year net survival') & (final_df['UOM']== 'Percentage') ]

#print(filtered_df.head(5))

cancer_survival_df = filtered_df.groupby(['cancer_type'])['survival_rate'].mean().reset_index()
cancer_survival_df.sort_values(by='survival_rate', ascending=False)

#print(cancer_survival_df.head(10))
#Sex based Differences

sex_differences_df = filtered_df.groupby(['cancer_type','Sex'])['survival_rate'].mean().reset_index()
sex_differences_df.sort_values(by='survival_rate', ascending=False)
#print(sex_differences_df.head(10))

#Age Group
#We need to clean the column Age Group in order to analize the data

#Regional Diferences
region_dif_df = filtered_df.groupby(['Region','cancer_type'])['survival_rate'].mean().reset_index()
region_dif_df.sort_values(by='survival_rate',ascending=False)
print(region_dif_df.head(30))
