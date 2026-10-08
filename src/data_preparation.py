"""
============================================================
WVS Wave 7 - Data Preparation Pipeline
============================================================
Research Question:
    "How strongly are income, education, employment, and financial
     well-being associated with life satisfaction?"

Dataset : WVS Cross-National Wave 7, v6.0
Script  : src/data_preparation.py
Author  : [Your Name]
Date    : 2026-10-07

Methodology note
----------------
This script does NOT run any regression.  Its sole purpose is to:
  1. Load the raw WVS CSV (read-only - never modified).
  2. Subset to the variables relevant to our research question.
  3. Rename those variables to human-readable names.
  4. Apply WVS-documented missing-value codes to produce proper NaN.
  5. Validate value ranges and flag impossible values.
  6. Produce a data-cleaning report.
  7. Save the cleaned, analysis-ready dataset.

References used for variable coding
-------------------------------------
  * WVS Wave 7 Master Questionnaire (2017-2020, English)
  * WVS Wave 7 Codebook / Variable Description File (v6.0)

WVS missing-value codes (applicable to most variables)
-------------------------------------------------------
  -1  = Don't know
  -2  = No answer / Refused
  -3  = Not applicable
  -4  = Not asked in survey
  -5  = Missing; Not available
  -9999 = Missing (used in some weighted/derived variables)

IMPORTANT: These codes must be treated as missing, NOT as valid
           numeric data.  We replace them with NaN before analysis.
============================================================
"""

import pandas as pd
import numpy as np
import os
import sys


# ---------------------------------------------------------------------------
# 0.  PATHS  (edit RAW_CSV_PATH if your file lives elsewhere)
# ---------------------------------------------------------------------------

RAW_CSV_PATH  = r"C:\Users\MyPC\Downloads\WVS_Cross-National_Wave_7_csv_v6_0.csv"
PROCESSED_DIR = r"C:\Users\MyPC\3RDYR-CS\Midterm_Project\data\processed"
OUTPUT_CSV    = os.path.join(PROCESSED_DIR, "wvs_analysis_ready.csv")
REPORT_TXT    = os.path.join(PROCESSED_DIR, "cleaning_report.txt")


# ---------------------------------------------------------------------------
# 1.  VARIABLE DEFINITIONS
# ---------------------------------------------------------------------------

# Mapping: raw WVS column name -> human-readable name
VARIABLE_MAP = {
    # Dependent variable
    "Q49":  "life_satisfaction",

    # Primary independent variables
    "Q288": "income",               # Household income group (1=lowest ... 10=highest)
    "Q275": "education",            # Highest educational level (ISCED, 0-8)
    "Q279": "employment",           # Employment status (categorical)

    # Financial/material well-being indicators
    "Q50":  "financial_satisfaction",   # Satisfaction with HH financial situation (1-10)
    "Q286": "financial_situation",      # HH financial situation past year (1=much worse ... 5=much better)
    "Q51":  "food_deprivation",         # Gone without enough food (1=often ... 4=never)
    "Q53":  "medical_deprivation",      # Gone without medicine (1=often ... 4=never)
    "Q54":  "cash_income_deprivation",  # Gone without cash income (1=often ... 4=never)
    "Q55":  "shelter_deprivation",      # Gone without safe shelter (1=often ... 4=never)

    # Social class / subjective standing
    "Q287": "social_class",         # Subjective social class (1=lower ... 5=upper)

    # Control variables
    "Q260": "sex",      # 1=Male, 2=Female
    "Q262": "age",      # Respondent age in years
}

# Country identifier columns (kept for control variable / fixed-effects use)
COUNTRY_COLS = ["B_COUNTRY", "B_COUNTRY_ALPHA"]

# WVS standard missing-value codes (integers)
WVS_MISSING_CODES = [-1, -2, -3, -4, -5, -9999]

# ---------------------------------------------------------------------------
# Variable-level documented valid ranges (from the WVS questionnaire).
# Values OUTSIDE these ranges will be flagged as invalid.
# ---------------------------------------------------------------------------
VALID_RANGES = {
    "life_satisfaction":        (1, 10),
    "income":                   (1, 10),
    "education":                (0, 8),      # ISCED 0-8
    "financial_satisfaction":   (1, 10),
    "financial_situation":      (1, 5),
    "food_deprivation":         (1, 4),
    "medical_deprivation":      (1, 4),
    "cash_income_deprivation":  (1, 4),
    "shelter_deprivation":      (1, 4),
    "social_class":             (1, 5),
    "sex":                      (1, 2),
    "age":                      (16, 100),   # WVS targets 18+; we use 16 as lower bound
    # employment has no simple numeric range - handled separately as categorical
}

# Employment (Q279) documented categories (WVS Wave 7 questionnaire)
EMPLOYMENT_VALID_CODES = {
    1: "Full time (30+ hrs/week)",
    2: "Part time (less than 30 hrs/week)",
    3: "Self employed",
    4: "Retired/Pensioned",
    5: "Housewife not otherwise employed",
    6: "Student",
    7: "Unemployed",
    8: "Other",
}


# ---------------------------------------------------------------------------
# 2.  LOAD RAW DATA  (read-only; never modify the original file)
# ---------------------------------------------------------------------------

def load_raw_data(path):
    """
    Load the raw WVS CSV without modifying it.

    Parameters
    ----------
    path : str
        Absolute path to the WVS Wave 7 CSV file.

    Returns
    -------
    pd.DataFrame
        Full raw dataframe.
    """
    print("\n" + "="*60)
    print("STEP 1: LOADING RAW DATA")
    print("="*60)
    print("  Source:", path)

    if not os.path.isfile(path):
        sys.exit("ERROR: File not found: " + path)

    df = pd.read_csv(path, low_memory=False)
    print("  Loaded {:,} rows x {:} columns.".format(len(df), len(df.columns)))
    return df


# ---------------------------------------------------------------------------
# 3.  VERIFY REQUIRED COLUMNS EXIST
# ---------------------------------------------------------------------------

def verify_columns(df):
    """
    Confirm that every variable in VARIABLE_MAP and the country columns
    actually exists in the loaded dataframe.  Aborts if any are missing.
    """
    print("\n" + "="*60)
    print("STEP 2: VERIFYING REQUIRED COLUMNS")
    print("="*60)

    required = list(VARIABLE_MAP.keys()) + COUNTRY_COLS
    missing  = [col for col in required if col not in df.columns]

    if missing:
        sys.exit("ERROR: The following required columns are absent from the CSV:\n  " + str(missing))

    print("  All {:} required columns confirmed present.".format(len(required)))


# ---------------------------------------------------------------------------
# 4.  SUBSET AND RENAME
# ---------------------------------------------------------------------------

def subset_and_rename(df):
    """
    Select only the variables relevant to our research question
    (plus country identifiers) and rename them to readable names.

    Parameters
    ----------
    df : pd.DataFrame
        Full raw dataframe.

    Returns
    -------
    pd.DataFrame
        Subsetted dataframe with renamed columns.
    """
    print("\n" + "="*60)
    print("STEP 3: SUBSETTING AND RENAMING COLUMNS")
    print("="*60)

    keep_cols = COUNTRY_COLS + list(VARIABLE_MAP.keys())
    df_sub    = df[keep_cols].copy()
    df_sub.rename(columns=VARIABLE_MAP, inplace=True)

    print("  Retained {:} columns:".format(len(df_sub.columns)))
    for raw, clean in VARIABLE_MAP.items():
        print("    {:8s} -> {}".format(raw, clean))

    return df_sub


# ---------------------------------------------------------------------------
# 5.  INSPECT RAW VALUE DISTRIBUTIONS  (before any cleaning)
# ---------------------------------------------------------------------------

def inspect_raw_distributions(df):
    """
    Print value-count summaries for every research variable, including
    all negative codes, so we can see exactly what missing-value patterns
    appear in the actual data.
    """
    print("\n" + "="*60)
    print("STEP 4: RAW VALUE DISTRIBUTIONS (before cleaning)")
    print("="*60)

    research_vars = list(VARIABLE_MAP.values())
    for var in research_vars:
        vc       = df[var].value_counts(dropna=False).sort_index()
        neg_keys = [k for k in vc.index if pd.notna(k) and k < 0]
        nan_n    = int(df[var].isna().sum())
        total    = len(df)

        print("\n  " + var)
        print("    dtype   : " + str(df[var].dtype))
        print("    NaN     : " + str(nan_n))
        print("    Negative (WVS missing codes):")
        if neg_keys:
            for k in neg_keys:
                print("      {:6d}  -> {:,} obs".format(int(k), int(vc[k])))
        else:
            print("      (none)")
        pos_keys = sorted([k for k in vc.index if pd.notna(k) and k >= 0])
        if pos_keys:
            print("    Positive values : {} ... {}  ({} distinct)".format(
                pos_keys[0], pos_keys[-1], len(pos_keys)))
        else:
            print("    No positive values found!")


# ---------------------------------------------------------------------------
# 6.  APPLY MISSING-VALUE CODES
# ---------------------------------------------------------------------------

def apply_missing_value_codes(df):
    """
    Replace WVS system missing-value codes with NaN.

    WVS coding convention (applies to the numeric research variables):
      -1  = Don't know
      -2  = No answer / Refused
      -3  = Not applicable
      -4  = Not asked in survey
      -5  = Missing; Not available
      -9999 = Missing

    NOTE: We ONLY replace these specific negative integers with NaN.
          We do NOT touch positive values or the country identifiers.

    Parameters
    ----------
    df : pd.DataFrame
        Subsetted, renamed dataframe.

    Returns
    -------
    pd.DataFrame
        Dataframe with WVS missing codes converted to NaN.
    """
    print("\n" + "="*60)
    print("STEP 5: APPLYING MISSING-VALUE CODES")
    print("="*60)

    numeric_vars = list(VARIABLE_MAP.values())

    for var in numeric_vars:
        before = df[var].isna().sum()
        df[var] = pd.to_numeric(df[var], errors="coerce")      # coerce stray strings
        df[var] = df[var].replace(WVS_MISSING_CODES, np.nan)  # WVS codes -> NaN
        after  = df[var].isna().sum()
        new_nan = after - before
        if new_nan > 0:
            print("  {:30s}: {:,} values converted to NaN (WVS codes)".format(var, new_nan))
        else:
            print("  {:30s}: no WVS missing codes found".format(var))

    return df


# ---------------------------------------------------------------------------
# 7.  VALIDATE VALUE RANGES
# ---------------------------------------------------------------------------

def validate_value_ranges(df):
    """
    Flag and nullify values that lie outside the documented valid range
    for each variable (after WVS missing codes have already been removed).

    Employment is handled separately: only codes NOT in EMPLOYMENT_VALID_CODES
    are treated as invalid.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe after missing-code replacement.

    Returns
    -------
    pd.DataFrame
        Dataframe with out-of-range values set to NaN and a warning printed.
    """
    print("\n" + "="*60)
    print("STEP 6: VALIDATING VALUE RANGES")
    print("="*60)

    for var, (lo, hi) in VALID_RANGES.items():
        if var not in df.columns:
            continue
        mask_valid   = df[var].isna() | ((df[var] >= lo) & (df[var] <= hi))
        out_of_range = (~mask_valid).sum()
        if out_of_range > 0:
            print("  WARNING - {:}: {:,} values outside [{}, {}] -> set to NaN".format(
                var, out_of_range, lo, hi))
            df.loc[~mask_valid, var] = np.nan
        else:
            print("  {:30s}: all values within [{}, {}]  OK".format(var, lo, hi))

    # Employment: flag codes not in the documented set
    if "employment" in df.columns:
        valid_emp    = set(EMPLOYMENT_VALID_CODES.keys())
        mask_bad_emp = df["employment"].notna() & ~df["employment"].isin(valid_emp)
        n_bad        = mask_bad_emp.sum()
        if n_bad > 0:
            bad_vals = df.loc[mask_bad_emp, "employment"].value_counts().to_dict()
            print("  WARNING - employment: {:,} undocumented codes -> set to NaN".format(n_bad))
            print("    Undocumented codes: " + str(bad_vals))
            df.loc[mask_bad_emp, "employment"] = np.nan
        else:
            print("  {:30s}: all codes within documented set  OK".format("employment"))

    return df


# ---------------------------------------------------------------------------
# 8.  DUPLICATE RESPONDENT CHECK
# ---------------------------------------------------------------------------

def check_duplicates(df):
    """
    Check for duplicate rows.

    The WVS v6.0 CSV does not include a simple respondent-ID column; the
    closest proxy is (B_COUNTRY, D_INTERVIEW) but D_INTERVIEW is not in our
    subset.  We therefore check for fully-duplicated rows across all retained
    columns as a conservative duplicate test.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe.

    Returns
    -------
    pd.DataFrame
        Dataframe with exact duplicate rows removed (if any).
    """
    print("\n" + "="*60)
    print("STEP 7: CHECKING FOR DUPLICATE ROWS")
    print("="*60)

    n_before = len(df)
    df       = df.drop_duplicates()
    n_after  = len(df)
    removed  = n_before - n_after

    if removed > 0:
        print("  WARNING: {:,} fully-duplicated rows removed.".format(removed))
    else:
        print("  No exact duplicate rows found.  OK")

    return df


# ---------------------------------------------------------------------------
# 9.  ASSIGN DATA TYPES
# ---------------------------------------------------------------------------

def assign_dtypes(df):
    """
    Assign appropriate pandas dtypes:
      * sex, employment -> stored as Int64 (nullable integer; label mapping at analysis stage)
      * education, income, social_class -> pandas Int64 (nullable integer, ordered)
      * age -> pandas Int64 (nullable integer)
      * Deprivation, financial, life satisfaction scales -> pandas Int64

    We use nullable integer (Int64 capital-I) so NaN can coexist with integers,
    avoiding unwanted float conversion.

    NOTE: We do NOT convert employment or sex to arbitrary numeric codes here.
          They remain as their original WVS integer codes until the analysis
          stage, where they will be one-hot-encoded as needed.
    """
    print("\n" + "="*60)
    print("STEP 8: ASSIGNING DATA TYPES")
    print("="*60)

    # All numeric research columns use nullable Int64
    int_cols = [
        "life_satisfaction", "income", "education", "financial_satisfaction",
        "financial_situation", "food_deprivation", "medical_deprivation",
        "cash_income_deprivation", "shelter_deprivation", "social_class",
        "age", "sex", "employment",
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype("Int64")

    print("  Nullable Int64 assigned to all numeric research variables.")
    print("  NOTE: employment and sex kept as integer codes; labels applied at analysis stage.")

    return df


# ---------------------------------------------------------------------------
# 10. MISSING-VALUE SUMMARY
# ---------------------------------------------------------------------------

def missing_value_summary(df):
    """
    Compute a summary table of missing values per variable.

    Returns
    -------
    pd.DataFrame
        Summary table with columns: variable, n_missing, pct_missing, n_valid.
    """
    total = len(df)
    rows  = []
    for col in df.columns:
        n_miss = int(df[col].isna().sum())
        rows.append({
            "variable":    col,
            "n_missing":   n_miss,
            "pct_missing": round(100 * n_miss / total, 2),
            "n_valid":     total - n_miss,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 11. LISTWISE DELETION CHECK  (for regression core variables)
# ---------------------------------------------------------------------------

def check_listwise_deletion(df):
    """
    Report how many observations would be lost if we performed listwise
    deletion on the core regression variables.

    If loss > 10%, a warning is printed and the user should consider
    multiple imputation or other strategies before proceeding to regression.
    """
    print("\n" + "="*60)
    print("STEP 9: LISTWISE DELETION CHECK (core regression variables)")
    print("="*60)

    core_vars = [
        "life_satisfaction", "income", "education",
        "employment", "financial_satisfaction",
    ]
    core_vars = [v for v in core_vars if v in df.columns]

    total    = len(df)
    complete = df[core_vars].dropna().shape[0]
    pct_lost = 100 * (total - complete) / total

    print("  Core variables: " + str(core_vars))
    print("  Total observations    : {:,}".format(total))
    print("  Complete cases (all)  : {:,}".format(complete))
    print("  Observations dropped  : {:,}  ({:.1f}%)".format(total - complete, pct_lost))

    if pct_lost > 10:
        print("\n  WARNING: Listwise deletion would remove {:.1f}% of respondents.".format(pct_lost))
        print("  Consider Multiple Imputation (MI) or keeping missing-value indicators.")
    else:
        print("\n  Listwise deletion loss is acceptable (<10%).")


# ---------------------------------------------------------------------------
# 12. GENERATE CLEANING REPORT
# ---------------------------------------------------------------------------

def generate_report(n_raw, n_after_dedup, df_cleaned, miss_table, report_path):
    """
    Write a plain-text data-cleaning report summarising all steps.
    """
    total = len(df_cleaned)
    lines = [
        "=" * 60,
        "WVS WAVE 7 - DATA CLEANING REPORT",
        "=" * 60,
        "",
        "Raw CSV observations        : {:,}".format(n_raw),
        "After duplicate removal     : {:,}".format(n_after_dedup),
        "After range validation      : {:,}  (rows kept; invalid values set to NaN)".format(total),
        "",
        "-" * 60,
        "VARIABLE DICTIONARY (final dataset)",
        "-" * 60,
        "{:<30} {:<35} {}".format("Variable", "Valid-range / categories", "WVS Code"),
        "-" * 70,
        "{:<30} {:<35} {}".format("life_satisfaction",       "1-10 (1=dissatisfied, 10=satisfied)", "Q49"),
        "{:<30} {:<35} {}".format("income",                  "1-10 (1=lowest, 10=highest)",         "Q288"),
        "{:<30} {:<35} {}".format("education",               "0-8 (ISCED classification)",           "Q275"),
        "{:<30} {:<35} {}".format("employment",              "1-8 (categorical - see codebook)",     "Q279"),
        "{:<30} {:<35} {}".format("financial_satisfaction",  "1-10 (1=dissatisfied, 10=satisfied)", "Q50"),
        "{:<30} {:<35} {}".format("financial_situation",     "1-5 (1=much worse, 5=much better)",   "Q286"),
        "{:<30} {:<35} {}".format("food_deprivation",        "1-4 (1=often, 4=never)",               "Q51"),
        "{:<30} {:<35} {}".format("medical_deprivation",     "1-4 (1=often, 4=never)",               "Q53"),
        "{:<30} {:<35} {}".format("cash_income_deprivation", "1-4 (1=often, 4=never)",               "Q54"),
        "{:<30} {:<35} {}".format("shelter_deprivation",     "1-4 (1=often, 4=never)",               "Q55"),
        "{:<30} {:<35} {}".format("social_class",            "1-5 (1=lower, 5=upper)",               "Q287"),
        "{:<30} {:<35} {}".format("sex",                     "1=Male, 2=Female (categorical)",       "Q260"),
        "{:<30} {:<35} {}".format("age",                     "Continuous (years)",                   "Q262"),
        "",
        "-" * 60,
        "MISSING VALUES BY VARIABLE (after cleaning)",
        "-" * 60,
    ]

    for _, row in miss_table.iterrows():
        lines.append(
            "  {:<30} {:>7,} missing  ({:>5.1f}%)  |  {:>7,} valid".format(
                row["variable"], row["n_missing"], row["pct_missing"], row["n_valid"]
            )
        )

    lines += [
        "",
        "-" * 60,
        "METHODOLOGICAL NOTES",
        "-" * 60,
        "1. Employment (Q279) is CATEGORICAL; do not treat as continuous.",
        "   Use dummy/indicator variables in regression.",
        "2. Sex (Q260) is CATEGORICAL (Male/Female); dummy in regression.",
        "3. Education (Q275) is an ordered ISCED scale (0-8).",
        "   Can be treated as ordinal or as a set of dummies.",
        "4. Income (Q288) is an ordered income-position variable (1-10),",
        "   NOT a dollar-amount measure of wealth.",
        "5. Life satisfaction (Q49) is the dependent variable (1-10).",
        "6. Deprivation items (Q51, Q53, Q54, Q55) are coded 1-4:",
        "   higher values = LESS deprivation (4=never went without).",
        "   Consider reversing scale before interpretation.",
        "",
        "-" * 60,
        "OUTPUT FILE",
        "-" * 60,
        "  " + OUTPUT_CSV,
        "",
        "=" * 60,
    ]

    report_str = "\n".join(lines)
    print("\n" + "="*60)
    print("CLEANING REPORT")
    print("="*60)
    print(report_str)

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(report_str)
    print("\n  Report saved ->", report_path)


# ---------------------------------------------------------------------------
# 13. SAVE CLEANED DATASET
# ---------------------------------------------------------------------------

def save_cleaned_dataset(df, path):
    """
    Save the cleaned, analysis-ready dataset to CSV.

    Parameters
    ----------
    df   : pd.DataFrame  - cleaned dataframe
    path : str           - output path
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print("\n  Cleaned dataset saved ->", path)
    print("  Shape: {:,} rows x {:} columns".format(df.shape[0], df.shape[1]))


# ---------------------------------------------------------------------------
# 14. MAIN PIPELINE
# ---------------------------------------------------------------------------

def main():
    """
    Execute the full data-preparation pipeline in order.
    """
    print("\n" + "=" * 60)
    print(" WVS WAVE 7 - DATA PREPARATION PIPELINE")
    print("=" * 60)

    # --- Load ---
    df_raw = load_raw_data(RAW_CSV_PATH)
    n_raw  = len(df_raw)

    # --- Verify columns ---
    verify_columns(df_raw)

    # --- Subset & rename ---
    df = subset_and_rename(df_raw)
    del df_raw   # free memory; we no longer need the full 613-column frame

    # --- Inspect raw distributions (before any cleaning) ---
    inspect_raw_distributions(df)

    # --- Apply WVS missing-value codes ---
    df = apply_missing_value_codes(df)

    # --- Validate ranges ---
    df = validate_value_ranges(df)

    # --- Duplicate check ---
    n_before_dedup = len(df)
    df = check_duplicates(df)
    n_after_dedup  = len(df)

    # --- Assign dtypes ---
    df = assign_dtypes(df)

    # --- Listwise deletion check ---
    check_listwise_deletion(df)

    # --- Missing-value summary ---
    miss_table = missing_value_summary(df)

    # --- Report ---
    generate_report(n_raw, n_after_dedup, df, miss_table, REPORT_TXT)

    # --- Save ---
    save_cleaned_dataset(df, OUTPUT_CSV)

    print("\n" + "=" * 60)
    print(" PIPELINE COMPLETE - awaiting your review before analysis.")
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
