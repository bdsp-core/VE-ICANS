# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 15:06:33 2021

@author: Danny
"""

import pandas as pd

df = pd.read_excel("NewFeatures.xlsx")
#df = pd.read_excel("CAR-T_ImagesCombinedWithReports.xlsx")

## Remove Images without ICANS

print(len(df))
df = df[df.Caption != "ICANS: Date not in range"]
df = df[df.Caption != "ICANS: Name not in Study"]
print(len(df))

## Remove Images disqualified for probably being asleep

df = df[df.Disqualify != 1]
print(len(df))

## Extract ICANS from caption and normalize

for i,r in df.iterrows():
    cap = r['Caption']
    icans = cap[7:]
    if icans == 'nan':
        icans = 3.5
    df.loc[i, 'icans'] = float(icans)
    
# Convert features to binary

for i, row in df.iterrows():
    d = row['delta freq']
    t = row['theta freq']
    a = row['alpha freq']
    if d == 0:
        d = 0
    elif d <= 1:
        df.loc[i, 'delta <=1Hz'] = 1
        df.loc[i, 'has delta'] = 1
    elif d <= 2:
        df.loc[i, 'delta 1<=2Hz'] = 1
        df.loc[i, 'has delta'] = 1
    elif d <= 3:
        df.loc[i, 'delta 2<=3Hz'] = 1
        df.loc[i, 'has delta'] = 1
    elif d <= 4:
        df.loc[i, 'delta 3<=4Hz'] = 1
        df.loc[i, 'has delta'] = 1
    else: print("Invalid delta freq", d, i)
        
    if t == 0:
        t = 0
    elif t <= 5:
        df.loc[i, 'theta 4<=5Hz'] = 1
        df.loc[i, 'has theta'] = 1
    elif t <= 6:
        df.loc[i, 'theta 5<=6Hz'] = 1
        df.loc[i, 'has theta'] = 1
    elif t <= 8:
        df.loc[i, 'theta 6<=8Hz'] = 1
        df.loc[i, 'has theta'] = 1
    #elif t <= 8:
    #    df.loc[i, 'theta 7<=8Hz'] = 1
    else: print("Invalid theta freq", t, i)
    
    if a == 0:
        a = 0
    elif a <= 8:
        df.loc[i, 'alpha <=8Hz'] = 1
        df.loc[i, 'has alpha'] = 1
    elif a <= 9:
        df.loc[i, 'alpha 8<=9Hz'] = 1
        df.loc[i, 'has alpha'] = 1
    elif a > 9:
        df.loc[i, 'alpha >=10Hz'] = 1
        df.loc[i, 'has alpha'] = 1
    else: print("Invalid alpha freq", a, i)
    
for i, row in df.iterrows():
    if row['pdr present'] == 0:
        df.loc[i, 'no PDR'] = 1
    else: 
        df.loc[i, 'no PDR'] = 0
        
use_cols = ['SID','File','mlv','elv',
           'delta <=1Hz','delta 1<=2Hz','delta 2<=3Hz','delta 3<=4Hz',
           'theta 4<=5Hz','theta 5<=6Hz','theta 6<=8Hz',
           'alpha <=8Hz','alpha 8<=9Hz','alpha >=10Hz',
           #'has delta','has theta','has alpha',
            'pdr present',#'no PDR',#'awake','continuous',
           'any GRDA','any GPDs','LRDA','LPDs','Intermittent brief attenuation','Burst suppression']

colsy = ['SID','File','icans','Rank1','Rank2','mean rank',]

df1 = df[use_cols]
df1 = df1.fillna(0)
df2 = df[colsy]
df2 = df2.fillna(0)

df3 = pd.DataFrame(['Burst suppression','elv',],columns=['EEGName'])

with pd.ExcelWriter('ImagesDataNewFeatures.xlsx') as writer:  
    df1.to_excel(writer, sheet_name='X',index=False)
    df2.to_excel(writer, sheet_name='y',index=False)
    df3.to_excel(writer, sheet_name='worst_delirium_names',index=False)

# =============================================================================
# df = df[use_cols]
# df.to_excel("PrepedImages_NewFeatures.xlsx")
# =============================================================================
