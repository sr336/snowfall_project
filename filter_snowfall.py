import pandas as pd
import os

def remove_missing_snowfall(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ Error: Cannot find the input file at {input_file}")
        print("Please run your aggregation script first to generate it.")
        return

    print(f"📖 Reading master combined data from: {input_file}")
    df = pd.read_csv(input_file, low_memory=False)
    
    # Track the starting size of the dataset
    initial_count = len(df)
    target_col = 'ANN-SNOW-NORMAL'
    
    # Safety check to make sure the column exists
    if target_col not in df.columns:
        print(f"❌ Error: Column '{target_col}' was not found in the dataset!")
        print(f"Available columns are: {list(df.columns)}")
        return
        
    print(f"🧹 Scrubbing rows with missing values in '{target_col}'...")
    
    # dropna removes any row where the specified subset column contains NaN/null
    df_cleaned = df.dropna(subset=[target_col])
    
    # Calculate the filtering metrics
    final_count = len(df_cleaned)
    rows_removed = initial_count - final_count
    
    # Save the polished data to a new CSV file
    df_cleaned.to_csv(output_file, index=False)
    
    # Print a quick summary of the operation
    print("\n--- Filtering Summary ---")
    print(f"📊 Total stations evaluated: {initial_count}")
    print(f"🗑️ Rows with missing data removed: {rows_removed}")
    print(f"✅ Stations remaining for your map: {final_count}")
    print(f"💾 Cleaned dataset successfully saved to: {output_file}")

if __name__ == "__main__":
    # Point directly to your file paths
    input_master_csv = r""
    output_cleaned_csv = r""
    
    remove_missing_snowfall(input_master_csv, output_cleaned_csv)