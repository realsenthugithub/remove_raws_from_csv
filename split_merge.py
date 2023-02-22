# setting python env varisbles
#!/usr/bin/env python3

# Importing libraries
import pandas as pd
import datetime as dt

# directory
dir = '/Users/senthu/OneDrive - GovTech/Desktop/Mongo Export Task/'

# file location from mongo raw & Mysqlraw
mysqlraw = dir +'APIIDv1.xlsx'
mongoraw = dir + '17-02-2023_11-45-17_report.csv'

# create empty list
guidlist_mysqlraw = []
guidlist_final = []

# get the current date and time
now = dt.datetime.now()

# read by default 1st sheet of an Excel file   # read by default 2nd sheet of an Excel file
df1 = pd.read_csv(mongoraw)
df2 = pd.read_excel(mysqlraw)

# remove special charaters form all colums
df1['serviceid'] = df1['serviceid'].str.replace('\W', '', regex=True)
df1['tenant'] = df1['tenant'].str.replace('\W', '', regex=True)
df1['statuscode'] = df1['statuscode'].str.replace('\W', '', regex=True)

# remove starting characters from a columns
df1['tenant'] = df1['tenant'].str[15:]
df1['statuscode'] = df1['statuscode'].str[10:]

# split a column by using a key word
df1[['count', 'svcid']] = df1["serviceid"].apply(lambda x: pd.Series(str(x).split("serviceId")))

# drop a column
dfm = df1.drop(columns=['serviceid'])

# Defining searching
searchkey = 'NULL'

# filter by GW,Username and api name and write guid to Excel sheet
for i in df2.index:
    if df2['PRODSVC'][i] != searchkey:
        guidlist_mysqlraw.append([df2['APIID'][i], df2['NAME'][i], df2['DESCRIPTION'][i], df2['PRODSVC'][i]])

# create dataframe from your guidlist
dfs = pd.DataFrame(list(guidlist_mysqlraw), columns=['APIID', 'NAME', 'DESCRIPTION', 'PRODSVC'])

# Drop empty raws from so
dfs.dropna(subset=['PRODSVC'], inplace=True)

# file name to save mongo & mysql
fmongo = dir + 'output_mongo' + str(now) + '.xlsx'
fmysql = dir + 'output_mysql' + str(now) + '.xlsx'

# save mongo & mysdl to excel
dfm.to_excel(fmongo)
dfs.to_excel(fmysql)

# read mongo & mysql files
dfmongo = pd.read_excel(fmongo)
dfmysql = pd.read_excel(fmysql)

# filter by GW,Username and api name and write guid to Excel sheet
for s in dfmongo.index:
    for j in dfmysql.index:
       if dfmongo['svcid'][s] == dfmysql['PRODSVC'][j]:
           guidlist_final.append([dfmongo['tenant'][s], dfmysql['NAME'][j], dfmongo['statuscode'][s], dfmongo['count'][s]])
           break

# create dataframe from your guidlist
df = pd.DataFrame(list(guidlist_final), columns=['tenant', 'API Name', 'statuscode', 'count'])
df.to_excel(dir + 'output_final' + str(now) + '.xlsx')
print(df)
