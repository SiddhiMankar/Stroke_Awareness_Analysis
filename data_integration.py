import pandas as pd
import glob
import re

# Load all CSV files in the folder
file_paths = glob.glob("C:\\Users\\S.D.M\\stroke_ml_project\\*.csv")
dfs = [pd.read_csv(f, encoding='latin1', dtype=str) for f in file_paths]  # dtype=str avoids mixed type issues

# Function to clean column names and make them unique
def clean_columns(df):
    df = df.copy()
    new_cols = []
    seen = {}
    for col in df.columns:
        col_clean = col.lower().strip()
        col_clean = re.sub(r"[^\w]+", "_", col_clean)  # replace special chars and spaces with _
        col_clean = re.sub(r"_+", "_", col_clean)      # remove multiple underscores
        col_clean = col_clean.strip("_")
        # Make unique
        if col_clean in seen:
            seen[col_clean] += 1
            col_clean = f"{col_clean}_{seen[col_clean]}"
        else:
            seen[col_clean] = 0
        new_cols.append(col_clean)
    df.columns = new_cols
    return df

# Apply cleaning to all datasets
dfs = [clean_columns(df) for df in dfs]

# Merge duplicate columns (like location, location_1, location_2) into a single column
def merge_duplicate_columns(df):
    df = df.copy()
    cols_map = {}
    for col in df.columns:
        base = re.sub(r'_\d+$', '', col)  # remove suffix _1, _2
        if base not in cols_map:
            cols_map[base] = [col]
        else:
            cols_map[base].append(col)
    for base, cols in cols_map.items():
        if len(cols) > 1:
            # Combine non-null values into the first column
            df[base] = df[cols].bfill(axis=1).iloc[:, 0]
            df = df.drop(columns=[c for c in cols if c != base])
    return df

dfs = [merge_duplicate_columns(df) for df in dfs]

# Find common columns across all datasets
common_cols = set(dfs[0].columns)
for df in dfs[1:]:
    common_cols = common_cols.intersection(set(df.columns))
print("Common columns across datasets:", common_cols)

# Align columns and merge
dfs_aligned = [df[list(common_cols)] for df in dfs]
merged_df = pd.concat(dfs_aligned, ignore_index=True)

print("Merged dataset shape:", merged_df.shape)

# -----------------------------
# FORCED BINARY / NUMERIC CONVERSION
# -----------------------------
binary_map = {
    'yes': 1, 'no': 0,
    'male': 0, 'female': 1,
    'true': 1, 'false': 0,
    'single': 0, 'married': 1,
    'maybe': 0.5,
    'never': 0, 'occasionally': 2, 'frequently': 3, 'rarely': 1,
    'immediately': 0, 'at the opportune time':1,
    'undergrad': 0, 'graduate': 1, 'specialty': 2, 'other': 3,
    'Within a day':1
}

# Columns to explicitly numerize
binary_columns_forced = [
    'do_you_think_trouble_seeing_in_one_or_both_the_eyes_is_a_stroke_symptom',
    'does_your_insurance_plan_provide_coverage_for_your_family_members_as_well',
    'do_you_have_any_preference_for_junk_food_like_mcdonald_s_burger_how_often_do_you_ask_for_outside_food_like_zomato_swiggy',
    'for_females_have_you_ever_taken_oral_contraceptives_or_hormonal_therapy',
    'do_you_think_sudden_nosebleed_is_a_stroke_of_symptom',
    'gender',
    'marital_status',
    'do_you_consume_alcohol',
    'educational_level',
    'do_you_think_sudden_confusion_trouble_speaking_or_understanding_speech_is_a_stroke_symptom',
    'do_you_think_sudden_numbness_or_weakness_of_face_arm_or_leg_is_a_symptom_of_stroke',
    'do_you_currently_have_medical_insurance',
    'do_you_have_a_family_history_of_brain_or_heart_stroke_of_hypertension_or_diabetes',
    'how_soon_would_you_consult_a_specialist_after_experiencing_the_first_symptom'
]

# Apply conversion
for col in binary_columns_forced:
    if col in merged_df.columns:
        merged_df[col] = (
            merged_df[col].astype(str)
            .str.lower()
            .str.strip()
            .map(binary_map)
        )

# Quick check
print(merged_df[binary_columns_forced].head())

# Save final merged dataset
merged_df.to_csv("merged_dataset.csv", index=False)
print("Merged dataset with specified binary columns saved successfully.")
