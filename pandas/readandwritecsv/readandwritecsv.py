# Vyasan Valavil
# This script will read a LogFile (Flash1.csv) created by OpenECU and convert them into a Pandas Data Frame
# It will also process it save it as another csv called hexdata1.csv

# Going to Have to Import the Following addons
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
#import os
import glob

#your csv file here:
csvfile = 'Flash1.csv'

#Here we grab 26 columns
my_cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
rawdf = pd.read_csv(csvfile, names=my_cols, engine='python', skiprows = 3)

#Now assign new names for the columns and run the for loop that will rename them.
orig    = ["B",     "D",    "E",    "G",    "H",    "I",    "J",    "K",    "L",    "M",    "N",    "O"]
new     = ["Time",  "Dir",  "Id",   "Len",  "B0",   "B1",   "B2",   "B3",   "B4",   "B5",   "B6",   "B7"]
for x in range(len(orig)):
    rawdf.rename(columns={orig[x]:new[x]}, inplace=True)
    my_cols.remove(orig[x])

#now you can drop all the column names that have not been changed by the above step
for x in range(len(my_cols)):
    rawdf.drop([my_cols[x]], axis=1, inplace=True)

#keep only required columns:
df = rawdf[rawdf['Len'] == '8']

df['b0'] = df['B0'].apply(int, base=16)
df['b1'] = df['B1'].apply(int, base=16)
df['b2'] = df['B2'].apply(int, base=16)
df['b3'] = df['B3'].apply(int, base=16)
df['b4'] = df['B4'].apply(int, base=16)
df['b5'] = df['B5'].apply(int, base=16)
df['b6'] = df['B6'].apply(int, base=16)
df['b7'] = df['B7'].apply(int, base=16)
df = df.reset_index(drop=True)

#create timeout
df['timeout'] = ""
df.at[0, 'timeout'] = 0
for x in range(len(df)-1):
    df.at[x+1, 'timeout'] = float(df.loc[x+1]['Time']) - float(df.loc[x]['Time'])

print(df)

#keep only required columns:
senddf = df
senddf = senddf[['Dir', 'timeout', 'b0', 'b1', 'b2', 'b3', 'b3', 'b4', 'b5', 'b6', 'b7']]
senddf = senddf.reset_index(drop=True)

print(senddf)

savefilename = 'hexdata1.csv'
senddf.to_csv(savefilename, index=False)

exit()