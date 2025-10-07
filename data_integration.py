import pandas as pd
import os

# Folder where your files are stored
data_folder = "."

# List all data files
files = [f for f in os.listdir(data_folder) if f.endswith(('.csv', '.xlsx', '.xlsm'))]

datasets = {}  # Dictionary to hold dataframes

for file in files:
    path = os.path.join(data_folder, file)
    print(f"\n🔹 Loading {file} ...")

    # Choose correct reader based on file type
    if file.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path, engine='openpyxl')

    # Store dataframe
    datasets[file] = df

    # Preview
    print(f"✅ {file} loaded successfully! Shape: {df.shape}")
    print(df.head(3))  # show first 3 rows
    print("-" * 60)

print("\nAll datasets loaded!")
print("\n🔍 Checking column names in each dataset:")
for name, df in datasets.items():
    print(f"\n{name}:")
    print(list(df.columns))
# Standardize column names for all datasets
rename_map = {
    # Names
    'Name': 'Name', 'name_(initials)': 'Name', 'Name (Initials)': 'Name',
    # Email
    'Email Address': 'Email', 'email_id': 'Email', 'Email ID': 'Email',
    # Contact
    'contact_number': 'Contact', 'Contact Number': 'Contact',
    # Age & Gender
    'Age': 'Age', 'Gender': 'Gender',
    # Location
    'Location': 'Location', 'LOcation': 'Location', 'location': 'Location', 'location.2': 'Location',
    # Timestamp
    'Timestamp': 'Timestamp',
    # TIA (stroke-related)
    'TIA': 'TIA'
}

for name, df in datasets.items():
    df.rename(columns=rename_map, inplace=True)

print("\n✅ Columns standardized for all datasets!")
for name, df in datasets.items():
    print(f"\n{name} columns after renaming:")
    print(df.columns.tolist()[:10])  # first 10 columns
# Merge all datasets using 'Email' as the primary key (assuming it's unique per person)
from functools import reduce

# List of datasets
dfs = list(datasets.values())

# Merge iteratively on 'Email' (outer join to keep all records)
merged_df = reduce(lambda left, right: pd.merge(left, right, on='Email', how='outer'), dfs)

print(f"\n✅ All datasets merged! Shape: {merged_df.shape}")
