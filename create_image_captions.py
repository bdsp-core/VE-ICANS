# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 20:55:49 2021

@author: Daniel Jones
"""

import pandas as pd
import numpy

df = pd.read_excel(r"C:\Users\Daniel Jones\Dropbox (Partners HealthCare)\carTproject\DannyJones\LTRmodel\ImageF\NewFeatures.xlsx")

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
    
dfres = pd.read_excel(r"C:\Users\Daniel Jones\Dropbox (Partners HealthCare)\carTproject\DannyJones\LTRmodel\ImageF\pred_scores_icans.xlsx")
dftog = pd.merge(df, dfres[["score","File"]], on=["File"])
    
## Make new captions

for i, row in dftog.iterrows():
    caption = ""
    if row["delta freq"] != 0:
        caption += "Delta frequency: " + str(row["delta freq"]) + "Hz"
        d = row['delta freq']
        if d <= 1:
            caption += " (+10)"
        elif d <= 2:
            caption += " (+6)"
        elif d <= 3:
            caption += " (+5)"
        elif d <= 4:
            caption += " (+3)"
        caption += ";  "
    if row["theta freq"] != 0:
        caption += "Theta frequency: " + str(row["theta freq"]) + "Hz"
        t = row["theta freq"]
        if t <= 5:
            caption += " (+2)"
        elif t <= 8:
            caption += " (+1)"
        caption += ";  "
    if row["alpha freq"] != 0:
        caption += "Alpha frequency: " + str(int(row["alpha freq"] )) + "Hz"
        if row["alpha freq"] > 9:
            caption += " (-1)"
        else:
            caption += " (+0)"
        caption += ";  "
    if row["pdr present"] == 1:
        caption += "PDR is present (-1);  "
# =============================================================================
#     if row["awake"] == 0:
#         caption += "No sign of being awake;  "
# =============================================================================
    if not pd.isnull(row["any GRDA"]):
        caption += "GRDA is present (+2);  "
    if not pd.isnull(row["mlv"]):
        caption += "Moderately low voltage (+2);  "
    if not pd.isnull(row["any GPDs"]):
        caption += "GPDs are present (+2);  "
    if not pd.isnull(row["elv"]):
        caption += "Low voltage: Extreme / ECS (=20 Worst);  "
    if not pd.isnull(row["Burst suppression"]):
        caption += "Burst Suppression (=20 Worst);  "
  
    
    dftog.loc[i, "NewCaption"] = caption
    
dftog.to_excel("FinalImageCaptions.xlsx")

