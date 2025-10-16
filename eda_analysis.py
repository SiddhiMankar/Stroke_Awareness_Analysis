# eda_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# LOAD DATASET
# -----------------------------
file_path = "cleaned_data_unique.csv"  # update path if needed
if not os.path.exists(file_path):
    raise FileNotFoundError(f"{file_path} not found. Place the CSV in this folder or update the path.")

df = pd.read_csv(file_path)
print("Dataset loaded successfully.")
print(f"Shape: {df.shape}")

# -----------------------------
# BASIC INFO & MISSING VALUES
# -----------------------------
print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Missing Values ---")
missing = df.isnull().sum().sort_values(ascending=False)
print(missing[missing > 0])

# -----------------------------
# NUMERIC COLUMNS ANALYSIS
# -----------------------------
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print("\nNumeric columns:", numeric_cols)

if numeric_cols:
    print("\n--- Numeric Summary ---")
    print(df[numeric_cols].describe())

    # Plot histograms separately
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        plt.hist(df[col].dropna(), bins=20, color='skyblue', edgecolor='black')
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    # Correlation matrix
    corr = df[numeric_cols].corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.show()

# -----------------------------
# CATEGORICAL / BINARY COLUMNS ANALYSIS
# -----------------------------
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
binary_cols = [col for col in df.columns if df[col].dropna().unique().tolist() in [[0, 1], [1, 0], [0], [1]]]

print("\nCategorical columns:", cat_cols)
print("Binary columns:", binary_cols)

for col in cat_cols + binary_cols:
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index)
    plt.title(f"Distribution of {col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# -----------------------------
# MISSING VALUE VISUALIZATION
# -----------------------------
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False)
plt.title("Missing Values Heatmap")
plt.show()

# -----------------------------
# PAIRPLOTS / RELATIONSHIPS
# -----------------------------
if len(numeric_cols) <= 10:
    sns.pairplot(df[numeric_cols])
    plt.suptitle("Pairplot of Numeric Columns", y=1.02)
    plt.show()

# -----------------------------
# SUMMARY REPORT
# -----------------------------
print("\n=== EDA SUMMARY REPORT ===")
total_rows, total_cols = df.shape

print(f"Total Rows: {total_rows}")
print(f"Total Columns: {total_cols}")
print(f"\nNumeric Columns: {len(numeric_cols)}")
print(f"Categorical Columns: {len(cat_cols)}")
print(f"Binary Columns: {len(binary_cols)}")

# Missing Data Summary
missing_percent = (df.isnull().sum() / len(df)) * 100
print("\nMissing Data Overview:")
print(f" - Columns with >50% missing: {(missing_percent > 50).sum()}")
print(f" - Columns with 10–50% missing: {((missing_percent <= 50) & (missing_percent > 10)).sum()}")
print(f" - Columns with <10% missing: {(missing_percent <= 10).sum()}")

# Most Complete Columns
most_complete = missing_percent.sort_values().head(5)
print("\nMost Complete Columns:")
for col, val in most_complete.items():
    print(f" - {col} ({100 - val:.1f}% filled)")

# Sample top categories
print("\nTop Categories (sample):")
for col in cat_cols[:5]:
    top_vals = df[col].dropna().value_counts().head(3).index.tolist()
    print(f" - {col}: {top_vals}")

# -----------------------------
# SAVE CLEANED / ANALYZED DATASET
# -----------------------------
output_file = "eda_dataset.csv"
df.to_csv(output_file, index=False)
print(f"\nEDA completed. Dataset saved as {output_file}")
