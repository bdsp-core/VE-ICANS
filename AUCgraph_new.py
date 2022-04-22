# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 20:19:34 2022

@author: Danny
"""

import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import confusion_matrix, cohen_kappa_score, roc_auc_score, roc_curve
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import seaborn as sns
sns.set_style('ticks')

maxScore = 20
    
#%%
def bootstrap_curves(x, xs, ys, bounds=None, verbose=True):
    _, idx = np.unique(x, return_index=True)
    idx = np.sort(idx)
    x = x[idx]
    idx = np.argsort(x)
    x_res = x[idx]
    
    ys_res = []
    for _ in tqdm(range(len(xs)), disable=not verbose):
        try:
            xx = xs[_]
            yy = ys[_]
            _, idx = np.unique(xx, return_index=True)
            idx = np.sort(idx)
            xx = xx[idx]; yy = yy[idx]
            idx = np.argsort(xx)
            xx = xx[idx]; yy = yy[idx]
            foo = interp1d(xx, yy, kind='linear')
            ys_res.append( foo(x) )
        except Exception as ee:
            print(str(ee))
            continue
    ys_res = np.array(ys_res)
    if bounds is not None:
        ys_res = np.clip(ys_res, bounds[0], bounds[1])
        
    return x_res, ys_res





K = 4
df_pred = pd.read_csv(r'../Data/cv_predictions_ltr_Nbt0haoqi.csv')
df_pred['SID'] = df_pred.SID.astype(str)
df_pred = df_pred[(df_pred.cvi!='full')&(df_pred.bti==0)].reset_index(drop=True)
y = df_pred.y.values
yp = df_pred.z.values


Nbt = 1000
random_state = 2020
np.random.seed(random_state)
ys = []; yps = []; yp_probs = []
for bti in tqdm(range(Nbt+1)):
    if bti==0:
        df_bt = df_pred.copy()
    else:
        btids = np.random.choice(len(df_pred), len(df_pred), replace=True)
        df_bt = df_pred.iloc[btids].reset_index(drop=True)
    ys.append( df_bt.y.values )
    yps.append( df_bt.z.values )
    yp_probs.append( df_bt[[f'prob({x})' for x in range(K)]].values )
    #yps_int.append( np.argmax(yp_probs, axis=1) )
    
    
# AUC

levels = list(np.arange(1,K))
aucs = []
aucs_lb = []
aucs_ub = []
Ns = []
level_todraw = 2
for level in tqdm(levels):
    aucs_bt = []
    fprs = []
    tprs = []
    for bti in range(Nbt+1):
        ids = (ys[bti]==0)|(ys[bti]>=level)
        y_ = (ys[bti][ids]>=level).astype(int)
        yp_ = yp_probs[bti][ids][:,level:].sum(axis=1)               #level:].sum(axis=1)
        if len(set(y_))==1:
            continue
        aucs_bt.append(roc_auc_score(y_,yp_))
        fpr_, tpr_, tt = roc_curve(y_, yp_)
        fprs.append(fpr_)
        tprs.append(tpr_)
        if bti==0:
            Ns.append(((y_==0).sum(), (y_==1).sum()))
    if Nbt>0:
        auc_lb, auc_ub = np.percentile(aucs_bt[1:], (2.5, 97.5))
    else:
        auc_lb = np.nan
        auc_ub = np.nan
    aucs.append(aucs_bt[0])
    aucs_lb.append(auc_lb)
    aucs_ub.append(auc_ub)
    
    if level==level_todraw:
        fpr, tprs_bt = bootstrap_curves(fprs[0], fprs, tprs, bounds=[0,1], verbose=False)
        tpr_lb, tpr_ub = np.percentile(tprs_bt[1:], (2.5, 97.5), axis=0)

figsize = (11,9.5)
panel_xoffset = -0.12
panel_yoffset = 1.01

# scatter plot
plt.close()
fig = plt.figure(figsize=figsize)
gs = fig.add_gridspec(2, 2)
# =============================================================================
# ax = fig.add_subplot(gs[0, :])
# ax = fig.add_subplot(gs[1,0])
# =============================================================================
ax = fig.add_subplot()
ax.fill_between(levels, aucs_lb, aucs_ub, color='k', alpha=0.2, label='95% CI')
ax.plot(levels, aucs, c='k', lw=2, marker='o')
ax.annotate('',
    (level_todraw+3.05, aucs[levels.index(level_todraw)]-0.03), 
    xytext=(level_todraw+0.35, aucs[levels.index(level_todraw)]-0.01),
    arrowprops=dict(color='k', width=2, headwidth=6))

ax.legend(loc='upper left', frameon=False)
ax.set_xticks(levels)
ax.set_xlim(levels[0]-0.1, levels[-1]+0.1)
ax.set_ylim(0.61, 1.0)
ax.set_yticks([0.7,0.8,0.9,1])
ax.set_ylabel('AUROC')
ax.set_xlabel('Comparison level x (ICANS=0 vs. ICANS$\geq$x)')
ax.yaxis.grid(True)
sns.despine()

axins = ax.inset_axes([0.53, 0.05, 0.43, 0.43])
   
axins.fill_between(fpr, tpr_lb, tpr_ub, color='k', alpha=0.2, label='95% CI')
axins.plot(fpr, tprs_bt[0], c='k', lw=2)#, label=f'CAM-S LF <= {level} vs. >={level+1}:\nAUC = {auc:.2f} [{auc_lb:.2f} - {auc_ub:.2f}]')# (n={np.sum(y2[0]==0)})

axins.plot([0,1],[0,1],c='k',ls='--')
#axins.legend(loc='lower right', frameon=False)
axins.set_xlim([-0.01, 1.01])
axins.set_ylim([-0.01, 1.01])
axins.set_xticks([0,0.25,0.5,0.75,1])
axins.set_yticks([0,0.25,0.5,0.75,1])
axins.set_xticklabels(['0','0.25','0.5','0.75','1'])
axins.set_yticklabels(['0','0.25','0.5','0.75','1'])
axins.set_ylabel('Sensitivity')
axins.set_xlabel('1 - Specificity')
axins.xaxis.set_label_coords(0.5, 0.15)
axins.grid(True)
sns.despine()

ax.text(panel_xoffset, panel_yoffset, 'B', ha='right', va='top', transform=ax.transAxes, fontweight='bold')

plt.show()
