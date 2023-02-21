# import pandas lib as pd

import pandas as pd
import datetime as dt

file = '//Users//senthu//OneDrive - GovTech//Desktop//Mongo Export Task//APIID.csv'
searchkey = 'NULL'

# create empty lists for guid
guidlist = []

# get the current date and time
now = dt.datetime.now()

# read by default 1st sheet of an Excel file
df = pd.read_csv(file)

# filter by GW,Username and api name and write guid to Excel sheet
for i in df.index:
    if df['PRODSVC'][i] != searchkey:
        guidlist.append([df['APIID'][i], df['NAME'][i], df['DESCRIPTION'][i], df['PRODSVC'][i]])

# create dataframe from your guidlist
dff = pd.DataFrame(list(guidlist), columns=['APIID', 'NAME', 'DESCRIPTION', 'PRODSVC'])

# Drop empty raws from so
dff.dropna(subset=['PRODSVC'], inplace=True)

# get your desired output
dff.to_excel('//Users//senthu//OneDrive - GovTech//Desktop//Mongo Export Task//' + str(now) + '.xlsx')
print(dff)
