import pandas as pd

file_path = "C:/Users/S.D.M/stroke_ml_project/data2.csv"

df = pd.read_csv(file_path, encoding='ISO-8859-1')

print("✅ Dataset loaded successfully!")
print("Original shape:", df.shape)

num_duplicates = df.duplicated().sum()
print(f"🔍 Number of duplicate rows: {num_duplicates}")

df_unique = df.drop_duplicates()
print("After removing duplicates:", df_unique.shape)

output_path = f"C:/Users/S.D.M/stroke_ml_project/cleaned_data_unique.csv"
df_unique.to_csv(output_path, index=False, encoding='utf-8')

total_rows = len(df)
unique_rows = len(df_unique)
removed = total_rows - unique_rows
percent_removed = (removed / total_rows) * 100 if total_rows > 0 else 0

print("\n📊 ===== DATA CLEANING SUMMARY =====")
print(f"Total Rows Before Cleaning : {total_rows}")
print(f"Total Unique Rows After Cleaning : {unique_rows}")
print(f"Duplicate Rows Removed : {removed}")
print(f"Percentage of Duplicates Removed : {percent_removed:.2f}%")
print(f"\n✅ Cleaned dataset saved to: {output_path}")
print("=====================================\n")

print(df_unique.head())