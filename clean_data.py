import pandas as pd
import os

# loading dataset
df = pd.read_csv("data/crop_data_raw.csv")

'''#raw data preview
print("\n Raw Data Preview")
print(df.head())
print("\n Shape:", df.shape)
print("\n Columns:", df.columns.tolist())'''

# renaming columns
df.rename(columns={
    "state_name": "state",
    "district_name": "district",
    "crop_year": "year",
    "crop": "crop",
    "season": "season",
    "area_": "area",
    "production_": "production"
}, inplace=True)

# droping cloumns with missing and zero values
df.dropna(subset=['area', 'production'], inplace=True)
df = df[(df['area']>0) & (df['production']>0)]

# convert types 
df['area'] = pd.to_numeric(df['area'], errors='coerce')
df['production'] = pd.to_numeric(df['production'], errors='coerce')

# droping rows that coudn't be converted
df.dropna(subset=['area', 'production'], inplace=True)

# yeild column
df['yield'] = df["production"] / df["area"]

# saving cleaned data
clean_path = "data/cleaned_data.csv"
df.to_csv(clean_path, index=False)

'''#Cleaned data preview
print(f"\n Cleaned data saved to: {clean_path}")
print(" Final Shape:", df.shape)
print(df.head())'''
