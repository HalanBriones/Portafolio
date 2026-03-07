import pandas as pd
import plotly.express as px

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
#**************INSIGHTS****************#
#Insights to dataframe to later create graphics
#Filter and leave only where Charasteristics = 5 year net survival and also only keep UOM = percenteg
filtered_df= final_df[(final_df['Characteristics']== '5-year net survival') & (final_df['UOM']== 'Percentage')].copy()
filtered_df['cancer_type'] = filtered_df['cancer_type'].str.replace(r'\[.*\]','',regex=True)
#Cancer-Type Survival in 5 year net survival
cancer_survival_df = filtered_df.groupby(['cancer_type'])['survival_rate'].mean().reset_index()
cancer_survival_df = cancer_survival_df.sort_values('survival_rate',ascending=False) #Descending order
cancer_survival_df['rank'] = cancer_survival_df['survival_rate'].rank(ascending=False,method='dense') #create rank column
#Limiting the dataframe to 10 types of cancer
cancer_survival_df = cancer_survival_df.head(10)
graph_can_surv = px.bar(
    data_frame = cancer_survival_df,
    x = 'survival_rate',
    y = 'cancer_type',
    orientation = 'h',
    color = 'rank',
    text = 'survival_rate', #add label on top of the bars
    title = 'Average Survival rate by Cancer Type', #head of the graphic
    labels={
        'survival_rate':'Survival Rate (%)',
        'cancer_type':'Cancer Type',
        'rank':'Ranking'
    }
)
#Showing yaxe ascending
#graph_can_surv.show()
#Sex based Differences per Type of cancer
filtered_df = filtered_df[filtered_df['Sex'] != 'Both sexes'] #Delete Sex=both sexes
sex_differences_df = filtered_df.groupby(['cancer_type','Sex'])['survival_rate'].mean().reset_index()
#reshape column sex into  female and male colums using pivot() -> turn rows into columns
sex_differences_df = sex_differences_df.pivot(
    index='cancer_type',
    columns='Sex',
    values='survival_rate'
)
sex_differences_df['differences'] = sex_differences_df['Females'] - sex_differences_df['Males']  
sex_differences_df = sex_differences_df.reset_index()#change it back to number indexes insteand of cancer type
sex_differences_df = sex_differences_df.head(10)
sex_differences_df = sex_differences_df.sort_values(by='differences',ascending=False)
#Graphic females vs males by cancer type 
graph_sex_surv_a = px.bar(
    data_frame = sex_differences_df,
    x = ['Females','Males'],
    y = 'cancer_type',
    barmode='group',
    orientation = 'h',
    title = 'Sex  Survival rate Difference by Cancer Type', #head of the graphic
)
graph_sex_surv_a.update_layout(#Change name of axis title
    xaxis_title = 'Survival Rate (%)',
    yaxis_title = 'Cancer Type'
)
#graph_sex_surv_a.show()
#Graphic difference survival rate female vs male
graph_sex_surv_b = px.bar(
    data_frame = sex_differences_df,
    x = 'differences',
    y = 'cancer_type',
    orientation = 'h',
    title = 'Difference Survival rate Female vs Male by Cancer Type', #head of the graphic
    labels = {
        'differences':'Survival Rate Difference (%)',
        'cancer_type':'Cancer Type'
    }
)
#graph_sex_surv_b.show()

#Age Group
#Clean Age Group data with regular expresions -> (\d+)\s+to\s+(\d+)
df_age = filtered_df[filtered_df['age_group'].str.contains('Total')==False].copy()#deleting Total from the string
df_age[['age_min','age_max']] = df_age['age_group'].str.extract(r'(\d+)\s+to\s+(\d+)') #r means raw strign - extracted the numbers of the string
df_age['age_min'] = df_age['age_min'].astype(int) #values to integer
df_age['age_max'] = df_age['age_max'].astype(int)#values to integer
df_age['age_mid'] = (df_age['age_min'] + df_age['age_max'])/2 #mid point of ages
age_group_df = df_age.groupby(['cancer_type','age_mid'])['survival_rate'].mean().reset_index()
age_group_df = age_group_df.sort_values(by='age_mid',ascending=True)
age_group_df = age_group_df.head(40)#work with only 40 examples
graph_age_surv = px.line(
    data_frame=age_group_df,
    x= 'age_mid',
    y='survival_rate',
    orientation = 'v',
    color='cancer_type',
    markers=True,
    title = 'Age Mid Point Survival Rate by Cancer Type',
    labels={
        'age_mid' : 'Age Mid Point',
        'survival_rate' : 'Survival Rate (%)',
        'cancer_type' : 'Cancer Type'
    }
)
#graph_age_surv.show()
#Regional Diferences
region_dif_df = filtered_df.groupby(['Region','cancer_type'])['survival_rate'].mean().reset_index()
region_dif_df = region_dif_df.sort_values(by='survival_rate',ascending=True)
region_dif_df = region_dif_df.pivot(
    index='cancer_type',
    columns='Region',
    values='survival_rate'
)
region_dif_df=region_dif_df.reset_index()
graph_reg_surv = px.bar(
    data_frame=region_dif_df,
    x='cancer_type',
    y=['Canada','Canada (excluding Quebec)'],  
    barmode='group',
    orientation='v',
    title='Survival Rates per Region by Type of Cancer',
    labels={
        'cancer_type':'Cancer Type',
        'value':'Survival Rate (%)'
    }
)
#graph_reg_surv.show()
#Analysis overtime
df_year = filtered_df.groupby(['cancer_type','Year'])['survival_rate'].mean().reset_index()
df_year = df_year.sort_values(by='survival_rate',ascending=False)
df_year[['start_year','end_year']] = df_year['Year'].str.split('/',expand=True).copy()
df_year['start_year'] = df_year['start_year'].astype(int)
df_year['end_year'] = df_year['end_year'].astype(int)
df_year['year_mid'] = (df_year['start_year']+df_year['end_year'])/2 
df_year = df_year.drop(columns='Year')
df_year['survival_change']= df_year.groupby('cancer_type')['survival_rate'].diff()
df_year['survival_change'] = df_year['survival_change'].fillna(0)
#df_year=df_year.head(20)
#Filter Top 5 type with survival change due to many years per cancer type
top_cancer_changes = df_year.groupby('cancer_type')['survival_change'].mean().nlargest(5).index
df_year_top = df_year[df_year['cancer_type'].isin(top_cancer_changes)]
print(df_year_top['cancer_type'].unique())


graph_year_surv = px.line(
    data_frame = df_year,
    x= 'year_mid',
    y='survival_rate',
    color='cancer_type',
    title ='5 year Survival rate(%) Over Time by Cancer Type',
    labels = {
        'year_mid': 'Year Mid Point',
        'survival_rate':'Survival Rate (%)',
        'cancer_type':'Cancer Type'
    }
)

# graph_year_surv.update_traces(mode='lines+markers')#ad the dots in the lines
# graph_year_surv.show()

