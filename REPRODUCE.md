# Reproduce — VE-ICANS (Jones et al., Sci Rep 2022)

Fits the ordinal / learning-to-rank ICANS-severity scoring model from **committed,
de-identified** features and prints/saves cross-validated predictions.

## One command (verified 2026-07-07)
```bash
pip install -r requirements.txt
python fit_model.py          # reads ImagesDataNewFeatures_deI.xlsx (X, y sheets)
```
Produces `results_ltr_*.pickle` + `cv_predictions_*.csv` (gitignored outputs).
`AUCgraph_new.py` / `table_info.py` render the paper's performance figures/tables from those.

## Data
`ImagesDataNewFeatures_deI.xlsx` (committed, PHI-clean): sheet **X** = 316 rows of binary
visual-EEG features per image; **y** = ICANS grade + expert ranks; subjects are surrogate
`SID` (no names). See `DATA_SOURCE.md`. The raw, name-containing feature files are **not**
committed (gitignored).

## Reproducibility fixes applied (2026-07-07)
- `_logistic_loss_and_grad` compatibility shim (sklearn removed the private fn in >=1.1).
- Patient grouping uses the de-identified `SID` (the original `File`/name column is removed).
- Points at the de-identified `ImagesDataNewFeatures_deI.xlsx`.
