# Data source & provenance — VE-ICANS (Jones et al. 2022)

**Paper:** Jones DK, Eckhardt CA, ... Westover MB. *EEG-based grading of immune
effector cell-associated neurotoxicity syndrome.* Sci Rep 2022;12:20011. doi:10.1038/s41598-022-24010-1. PMID 36414694.

## Committed data (de-identified)
`ImagesDataNewFeatures_deI.xlsx` — the prepared model input: expert-rated visual EEG
features (X) + ICANS grade / ranks (y) for 316 CAR-T EEG images. Surrogate `SID`; **no PHI**
(PHI-scanned: 0 name hits).

## NOT committed (PHI)
The raw feature spreadsheets (`NewFeatures.xlsx`, `ImagesDataNewFeatures.xlsx`,
`CAR-T_ImagesCombinedWithReports.xlsx`) contain a `File`/`OldName` column with patient
names (LASTNAME~FIRSTNAME) — **do not publish**. They are gitignored. The de-identified
export drops those columns and is the canonical committed input.

## Lineage
raw EEG image captions + expert feature ratings (`prepare_new_features.py`) -> features +
ICANS grade -> de-identified `ImagesDataNewFeatures_deI.xlsx` -> `fit_model.py` (ordinal LTR model).
