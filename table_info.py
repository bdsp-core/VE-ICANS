# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 23:22:40 2022

@author: Danny
"""

import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import mannwhitneyu

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def tostr(n1, n2):
    return f"{n1:.1f} ({n2:.1f})"
def tostr3(n1, n2, n3):
    return f"{n1:.0f} ({n2:.0f} - {n3:.0f})"
def tostrP(n1, n2):
    n2 = 100 * n1/n2
    return f"{n1:.0f} ({n2:.1f}%)"

df_all = pd.read_excel(r"C:\Users\Daniel Jones\Dropbox (Partners HealthCare)\carTproject\Clinical Data collated\JustPatients_NoICANS_12132021.xlsx")
df_features = pd.read_excel(r"C:\Users\Daniel Jones\Dropbox (Partners HealthCare)\carTproject\DannyJones\LTRmodel\ImageF\NewFeatures.xlsx")
df_icans = pd.read_excel(r"C:\Users\Daniel Jones\Dropbox (Partners HealthCare)\carTproject\Clinical Data collated\Allpatients_8282021.xlsx")

used_ids = set(df_features.SID.values)

df_filter = df_all.loc[df_all['ID'].isin(used_ids)]

#%%
# Find icans <= 2 vs > 2
# Calculate duration of icans

twoandbelow = []
abovetwo = []
icansDur = []
maxIcans = []


for mrn in df_filter.MRN:
    if(max(df_icans[df_icans["MRN"] == mrn]["meanscore_"])) <= 2:
        twoandbelow.append(mrn)
    else:
        abovetwo.append(mrn)
        
    cnt = 0
    for n in df_icans[df_icans["MRN"] == mrn]["meanscore_"]:
        if n > 0:
            cnt += 1
    print(mrn, cnt)
    icansDur.append(cnt)
    maxIcans.append(max(df_icans[df_icans["MRN"] == mrn]["meanscore_"]))
    
df_filter["IcansDuration"] = icansDur
df_filter["MaxIcans"] = maxIcans

#%% Create summaries

# Make length of stay column
df_filter.DCDate = pd.to_datetime(df_filter.DCDate)
df_filter.AdmitDate = pd.to_datetime(df_filter.AdmitDate)
df_filter["Length of Stay"] = (df_filter["DCDate"] - df_filter["AdmitDate"]).dt.days.astype(int)

# Make Duration of Icans column

# Seperate into low and high
df_low = df_filter.loc[df_filter["MRN"].isin(twoandbelow)]
df_high = df_filter.loc[df_filter["MRN"].isin(abovetwo)]

#Make summaries
df_summary = df_filter.describe()
df_summary_low = df_low.describe()
df_summary_high = df_high.describe()

#%%
## Calculate Age mean(sd)

total = df_summary.Age["mean"]
total_sd = df_summary.Age["std"]
print("Total Age:  " + tostr(total, total_sd))
low = df_summary_low.Age["mean"]
low_sd = df_summary_low.Age["std"]
print("Low Age:  " + tostr(low, low_sd))
high = df_summary_high.Age["mean"]
high_sd = df_summary_high.Age["std"]
print("High Age:  " + tostr(high, high_sd))
AgeResult = mannwhitneyu(df_low["Age"], df_high["Age"])
print("MannWhitneyTest for Age: %f" % AgeResult.pvalue)

#%%
## Calculate Length of Stay median (iqr)
print("\nLength of Stay\n")

print("Total:  " + tostr3(np.median(df_filter["Length of Stay"]), df_summary["Length of Stay"]["25%"], df_summary["Length of Stay"]["75%"]))
print("Low:  " + tostr3(np.median(df_low["Length of Stay"]), df_summary_low["Length of Stay"]["25%"], df_summary_low["Length of Stay"]["75%"]))
print("high:  " + tostr3(np.median(df_high["Length of Stay"]), df_summary_high["Length of Stay"]["25%"], df_summary_high["Length of Stay"]["75%"]))
LOSResult = mannwhitneyu(df_low["Length of Stay"], df_high["Length of Stay"])
print("MannWhitneyTest for Age: %f" % LOSResult.pvalue)

#%% Gender n (%)
print("\nGender\n") 

df_gender = df_filter.Gender.value_counts()
print("Total:")
print("Female: " + tostrP(df_gender["F"], df_filter.Gender.count()))
print("Male: " + tostrP(df_gender["M"], df_filter.Gender.count()))

df_gender = df_low.Gender.value_counts()
print("Low:")
print("Female: " + tostrP(df_gender["F"], df_low.Gender.count()))
print("Male: " + tostrP(df_gender["M"], df_low.Gender.count()))

df_gender = df_high.Gender.value_counts()
print("High:")
print("Female: " + tostrP(df_gender["F"], df_high.Gender.count()))
print("Male: " + tostrP(df_gender["M"], df_high.Gender.count()))

GenderResult = mannwhitneyu(df_low["Gender"], df_high["Gender"])
print("MannWhitneyTest for Death: %f" % GenderResult.pvalue)


#%% Race
print("\nRace\n") 

# I need key, these values are not accurate
df_race = df_filter.PatientRaceCD.value_counts()
print("Total:")
print("Asian: " + tostrP(df_race[4], df_filter.PatientRaceCD.count()))
print("Black: " + tostrP(df_race[2], df_filter.PatientRaceCD.count()))
print("White: " + tostrP(df_race[1], df_filter.PatientRaceCD.count()))
print("Other or Unknown: " + tostrP(df_race[6] + df_race[8] + df_race[7], df_filter.PatientRaceCD.count()))

df_race = df_low.PatientRaceCD.value_counts()
print("Low:")
print("Asian: " + tostrP(0, df_low.PatientRaceCD.count()))
print("Black: " + tostrP(df_race[2], df_low.PatientRaceCD.count()))
print("White: " + tostrP(df_race[1], df_low.PatientRaceCD.count()))
print("Other or Unknown: " + tostrP(df_race[6], df_low.PatientRaceCD.count()))

df_race = df_high.PatientRaceCD.value_counts()
print("High:")
print("Asian: " + tostrP(df_race[4], df_high.PatientRaceCD.count()))
print("Black: " + tostrP(df_race[2], df_high.PatientRaceCD.count()))
print("White: " + tostrP(df_race[1], df_high.PatientRaceCD.count()))
print("Other or Unknown: " + tostrP(df_race[8] + df_race[7], df_high.PatientRaceCD.count()))

RaceResult = mannwhitneyu(df_low["PatientRaceCD"], df_high["PatientRaceCD"])
print("MannWhitneyTest for Race: %f" % RaceResult.pvalue)

#%% Ethnicity
print("\nEthnicity\n") 

# I need key, these values are not accurate
df_ethnicity = df_filter.EthnicGroupCD.value_counts()
print("Total:")
print("Hispanic: " + tostrP(df_ethnicity[42], df_filter.EthnicGroupCD.count()))
print("Non-Hispanic: " + tostrP(df_ethnicity[43], df_filter.EthnicGroupCD.count()))
print("Unavailable: " + tostrP(df_ethnicity[3], df_filter.EthnicGroupCD.count()))

df_ethnicity = df_low.EthnicGroupCD.value_counts()
print("Low:")
print("Hispanic: " + tostrP(df_ethnicity[42], df_low.EthnicGroupCD.count()))
print("Non-Hispanic: " + tostrP(df_ethnicity[43], df_low.EthnicGroupCD.count()))
print("Unavailable: " + tostrP(df_ethnicity[3], df_low.EthnicGroupCD.count()))

df_ethnicity = df_high.EthnicGroupCD.value_counts()
print("High:")
print("Hispanic: " + tostrP(df_ethnicity[42], df_high.EthnicGroupCD.count()))
print("Non-Hispanic: " + tostrP(df_ethnicity[43], df_high.EthnicGroupCD.count()))
print("Unavailable: " + tostrP(df_ethnicity[3], df_high.EthnicGroupCD.count()))

EthResult = mannwhitneyu(df_low["EthnicGroupCD"], df_high["EthnicGroupCD"])
print("MannWhitneyTest for Ethnicity: %f" % EthResult.pvalue)

#%% Malignancy
print("\nMalignancy\n") 

# I need key, these values are not accurate
df_mal = df_filter["Malignancy  (ALL, DLBCL, MM)"].value_counts()
print("Total:")
print("DLBCL: " + tostrP(df_mal["DLBCL"], df_filter["Malignancy  (ALL, DLBCL, MM)"].count()))
print("PMBCL: " + tostrP(df_mal["PMBCL"], df_filter["Malignancy  (ALL, DLBCL, MM)"].count()))
print("FL: " + tostrP(df_mal["FL"], df_filter["Malignancy  (ALL, DLBCL, MM)"].count()))
print("Other: " + tostrP(133-121,133))
# =============================================================================
# print("MCL: " + tostrP(df_mal["MCL-blastoid"], df_filter["Malignancy  (ALL, DLBCL, MM)"].count()))
# print("B-ALL: " + tostrP(df_mal["B-ALL"], df_filter["Malignancy  (ALL, DLBCL, MM)"].count()))
# print("MM: " + tostrP(df_mal["MM"], df_filter["Malignancy  (ALL, DLBCL, MM)"].count()))
# print("MZL: " + tostrP(df_mal["MZL"], df_filter["Malignancy  (ALL, DLBCL, MM)"].count()))
# =============================================================================

df_mal = df_low["Malignancy  (ALL, DLBCL, MM)"].value_counts()
print("Low:")
print("DLBCL: " + tostrP(df_mal["DLBCL"], df_low["Malignancy  (ALL, DLBCL, MM)"].count()))
#print("PMBCL: " + tostrP(df_mal["PMBCL"], df_low["Malignancy  (ALL, DLBCL, MM)"].count()))
print("FL: " + tostrP(df_mal["FL"], df_low["Malignancy  (ALL, DLBCL, MM)"].count()))
print("Other: " + tostrP(54-51,df_low["Malignancy  (ALL, DLBCL, MM)"].count()))

df_mal = df_high["Malignancy  (ALL, DLBCL, MM)"].value_counts()
print("High:")
print("DLBCL: " + tostrP(df_mal["DLBCL"], df_high["Malignancy  (ALL, DLBCL, MM)"].count()))
print("PMBCL: " + tostrP(df_mal["PMBCL"], df_high["Malignancy  (ALL, DLBCL, MM)"].count()))
print("FL: " + tostrP(df_mal["FL"], df_high["Malignancy  (ALL, DLBCL, MM)"].count()))
print("Other: " + tostrP(79-70,df_high["Malignancy  (ALL, DLBCL, MM)"].count()))

MagResult = mannwhitneyu(df_low["Malignancy  (ALL, DLBCL, MM)"], df_high["Malignancy  (ALL, DLBCL, MM)"])
print("MannWhitneyTest for Malignancy: %f" % MagResult.pvalue)

#%% Aggressive
print("\nAggressive\n") 

df_aggr = df_filter.Aggressive.value_counts()
print("Total:")
print("Aggressive: " + tostrP(df_aggr[1], df_filter.Aggressive.count()))
print("Indolent: " + tostrP(df_aggr[0], df_filter.Aggressive.count()))

df_aggr = df_low.Aggressive.value_counts()
print("Low:")
print("Aggressive: " + tostrP(df_aggr[1], df_low.Aggressive.count()))
print("Indolent: " + tostrP(df_aggr[0], df_low.Aggressive.count()))

df_aggr = df_high.Aggressive.value_counts()
print("High:")
print("Aggressive: " + tostrP(df_aggr[1], df_high.Aggressive.count()))
print("Indolent: " + tostrP(df_aggr[0], df_high.Aggressive.count()))

AggResult = mannwhitneyu(df_low["Aggressive"], df_high["Aggressive"])
print("MannWhitneyTest for Aggressive: %f" % AggResult.pvalue)


#%% 1-year post discharge death
print("\nDeceased 1 year post\n") 

df_death = df_filter["1YearDeath"].value_counts()
print("Total:")
print("Alive: " + tostrP(df_death[0], df_filter["1YearDeath"].count()))
print("Deceased: " + tostrP(df_death[1], df_filter["1YearDeath"].count()))

df_death = df_low["1YearDeath"].value_counts()
print("Low:")
print("Alive: " + tostrP(df_death[0], df_low["1YearDeath"].count()))
print("Deceased: " + tostrP(df_death[1], df_low["1YearDeath"].count()))

df_death = df_high["1YearDeath"].value_counts()
print("High:")
print("Alive: " + tostrP(df_death[0], df_high["1YearDeath"].count()))
print("Deceased: " + tostrP(df_death[1], df_high["1YearDeath"].count()))

DeathResult = mannwhitneyu(df_low["1YearDeath"], df_high["1YearDeath"])
print("MannWhitneyTest for Death: %f" % DeathResult.pvalue)

#%% Max Icans median (iqr)
print("\nMax Icans\n")

print("Total:  " + tostr3(np.median(df_filter["MaxIcans"]), df_summary["MaxIcans"]["25%"], df_summary["MaxIcans"]["75%"]))
print("Low:  " + tostr3(np.median(df_low["MaxIcans"]), df_summary_low["MaxIcans"]["25%"], df_summary_low["MaxIcans"]["75%"]))
print("high:  " + tostr3(np.median(df_high["MaxIcans"]), df_summary_high["MaxIcans"]["25%"], df_summary_high["MaxIcans"]["75%"]))

MaxIResult = mannwhitneyu(df_low["MaxIcans"], df_high["MaxIcans"])
print("MannWhitneyTest for Max Icans: %f" % MaxIResult.pvalue)

#%% Duration Icans median (iqr)
print("\nIcans Duration\n")

print("Total:  " + tostr3(np.median(df_filter["IcansDuration"]), df_summary["IcansDuration"]["25%"], df_summary["IcansDuration"]["75%"]))
print("Low:  " + tostr3(np.median(df_low["IcansDuration"]), df_summary_low["IcansDuration"]["25%"], df_summary_low["IcansDuration"]["75%"]))
print("high:  " + tostr3(np.median(df_high["IcansDuration"]), df_summary_high["IcansDuration"]["25%"], df_summary_high["IcansDuration"]["75%"]))

DurResult = mannwhitneyu(df_low["IcansDuration"], df_high["IcansDuration"])
print("MannWhitneyTest for Icans Duration: %f" % DurResult.pvalue)



#df_filter.describe().to_excel("description.xlsx")