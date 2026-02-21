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
    'survival_rate',
    #'Characteristics',
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

print(final_df.head(10)) #First x values
#print(df.tail(2)) #Last x values

#**************INSIGHTS****************#

#Insights to dataframe to later create graphics


#Cancer-Type Survival
#Sex based Differences
#Age Group
#Regional Diferences
