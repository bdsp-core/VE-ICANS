# VE-ICANS

Code for **VE-ICANS** — a Visual-EEG-feature-based score for the severity
of **Immune-effector-Cell-Associated Neurotoxicity Syndrome (ICANS)**,
the neurotoxicity that can follow CAR-T cell therapy. Sibling of the
[`VE-CAM-S`](https://github.com/bdsp-core/VE-CAM-S) delirium-severity
score.

## What it does

Given expert-rated visual EEG features (delta / theta / alpha frequency
content, plus other image-level features) extracted from clinical EEG
recordings of CAR-T patients, fit a small, interpretable ordinal model
that predicts the patient's ICANS grade (0–4). The model is constrained
to produce a clinically usable integer / half-integer score — coefficients
are restricted to a fixed decimal grid (e.g. `0.1` or `0.5` increments),
can be bounded and ordered, and can be constrained to sum to a target
total. This is what turns a logistic-regression-style fit into something
that looks like a clinical scoring rubric.

## Layout

```
prepare_new_features.py        clean / curate the input feature spreadsheet
                               (drop out-of-range or "asleep" images,
                               extract numeric ICANS grade from caption,
                               binarise frequency-band features)
fit_model.py                   main modelling code. Defines:
                                 - MyLogisticRegression — logistic regression with
                                   coefficient-decimal / sum / bound / order constraints
                                 - MyCalibrator — ordinal recalibration wrapper around
                                   mord.LogisticAT
                               Plus the cross-validation / hyperparameter search driver.
AUCgraph_new.py                bootstrap ROC + calibration curves
table_info.py                  Table-1 patient summary statistics
                               (median/IQR, p-values via Mann-Whitney)
create_image_captions.py       helper for generating image captions
```

## Required environment

- Python 3 with `numpy`, `pandas`, `scipy`, `scikit-learn`, `mord`
  (ordinal logistic regression), `matplotlib`, `seaborn`, `tqdm`,
  `openpyxl` (Excel I/O).
- Input feature workbook (`NewFeatures.xlsx`) and clinical-data
  spreadsheets organised as in the original analysis (see the absolute
  paths in `table_info.py` for the layout).

## Related repos

- [`bdsp-core/VE-CAM-S`](https://github.com/bdsp-core/VE-CAM-S) —
  visual-EEG-feature-based delirium-severity score; same constrained-
  coefficient modelling approach.
- [`bdsp-core/E-ICANS`](https://github.com/bdsp-core/E-ICANS) —
  fully-automated EEG-based ICANS severity prediction via
  learning-to-rank (no human EEG-feature grading).

## Status

Research code accompanying the VE-ICANS analysis (2021–2022).
