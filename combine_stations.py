import os
import glob
import pandas as pd
import numpy as np
import time

def aggregate_station_files(folder_path, output_file):
    print(f"🔍 Searching for CSV files in: {folder_path}")
    
    # Grab all CSV files inside the directory
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    total_files = len(csv_files)
    
    if total_files == 0:
        print("❌ No CSV files found! Please verify the folder path layout.")
        return

    print(f"📂 Found {total_files} station files. Commencing aggregation...")
    
    all_station_rows = []
    start_time = time.time()
    
    # Target columns we want to keep for the final map.
    # Restricting columns here saves significant memory and processing time.
    cols_to_keep = ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ANN-SNOW-NORMAL']
    
    for index, file_path in enumerate(csv_files, 1):
        try:
            # Read the 2-row station CSV file
            df = pd.read_csv(file_path, low_memory=False)
            
            # Normalize column names to uppercase to avoid case-sensitivity bugs
            df.columns = df.columns.str.upper()
            
            # Filter down to only columns that actually exist in this file
            available_cols = [c for c in cols_to_keep if c in df.columns]
            df_filtered = df[available_cols].copy()
            
            # Store the row in our staging list
            all_station_rows.append(df_filtered)
            
        except Exception as e:
            # If a single file is corrupt, skip it and keep processing the rest
            print(f"⚠️ Error reading {os.path.basename(file_path)}: {e}")
            continue
            
        # Progress reporter so you know the script hasn't frozen
        if index % 2000 == 0 or index == total_files:
            elapsed = time.time() - start_time
            print(f"   Processed {index}/{total_files} files... ({elapsed:.1f} seconds elapsed)")

    print("\n🔄 Merging all station rows into a single master dataset...")
    combined_df = pd.concat(all_station_rows, ignore_index=True)
    
    print("🧹 Cleaning data and parsing NOAA weather flags...")
    target_col = 'ANN-SNOW-NORMAL'
    
    if target_col in combined_df.columns:
        # Convert values to numeric, turning errors into NaN
        combined_df[target_col] = pd.to_numeric(combined_df[target_col], errors='coerce')
        
        # Replace NOAA's numeric placeholder flags:
        # -9999.0 means Missing Data
        # -7777.0 means a "Trace" amount (less than 0.1 inch)
        combined_df[target_col] = combined_df[target_col].replace(-9999.0, np.nan)
        combined_df[target_col] = combined_df[target_col].replace(-7777.0, 0.05)
        
        # Drop rows missing map coordinates
        if 'LATITUDE' in combined_df.columns and 'LONGITUDE' in combined_df.columns:
            combined_df = combined_df.dropna(subset=['LATITUDE', 'LONGITUDE'])
            
        # Save the final consolidated file
        combined_df.to_csv(output_file, index=False)
        print(f"🎉 Success! Master file saved to: {output_file}")
        print(f"📊 Consoles contain {len(combined_df)} unique US weather stations.")
    else:
        # Fallback if the folder didn't contain annual snowfall records
        combined_df.to_csv(output_file, index=False)
        print(f"⚠️ Processed files, but '{target_col}' column was missing.")
        print(f"💾 Saved general available parameters to: {output_file}")

if __name__ == "__main__":
    # Your explicit folder path wrapped in a raw string (r"...")
    source_folder = r""
    
    # Output path where the master CSV file will be generated
    output_master_csv = r""
    
    aggregate_station_files(source_folder, output_master_csv)