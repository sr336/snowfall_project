import pandas as pd
import plotly.express as px
import os

def create_custom_heatmap(data_file):
    # Check if the cleaned data file exists
    if not os.path.exists(data_file):
        print(f"❌ Error: Cannot find the data file at {data_file}")
        print("Please run your filtering script first.")
        return

    print(f"📖 Loading cleaned weather station data from: {data_file}")
    df = pd.read_csv(data_file)
    
    target_col = 'ANN-SNOW-NORMAL'
    
    # Determine the maximum snowfall to define our custom color stops.
    z_max = df[target_col].max()
    print(f"📊 The maximum annual snowfall in your dataset is {z_max:.1f} inches.")

    # Calculate the normalized stop for 100 inches.
    # Color stops in Plotly are values between 0.0 (start) and 1.0 (end).
    if z_max > 100:
        custom_stop = 100.0 / z_max
    else:
        custom_stop = 1.0 
    
    # Create the multi-stop sequential custom color scale:
    # 0.0 (Start): White -> custom_stop (100 inches): Blue -> 1.0 (End): Red
    custom_color_scale = [
        (0.0, "white"),         # 0 Inches: Pure white
        (custom_stop, "blue"),  # 100 Inches: Solid blue
        (1.0, "red")            # Maximum data value: Pure red
    ]

    print("🗺️ Rendering enhanced Mapbox density heatmap with custom gradient...")
    
    # Generate the geographic density heatmap
    fig = px.density_mapbox(
        df, 
        lat='LATITUDE', 
        lon='LONGITUDE', 
        z=target_col, 
        radius=15,                        # Controls blending (blur/glow effect)
        center=dict(lat=37.0902, lon=-95.7129), # Coordinates to center over the US
        zoom=3.5,                         # Starting zoom level
        mapbox_style="carto-positron",    # Clean, light map background
        
        # FIX: Replaced 'zmin' and 'zmax' with the correct 'range_color' parameter
        color_continuous_scale=custom_color_scale,  
        range_color=[0, z_max],                     # Explicitly locks the color scale bounds
        
        title="Enhanced US Annual Snowfall Baseline (1991–2020) with Custom Scale",
        labels={target_col: 'Annual Snowfall (Inches)'},
        hover_name='NAME'                 # Displays the location/station name on hover
    )
    
    # Maximize the layout margins to fill the screen
    fig.update_layout(
        margin={"r":0, "t":50, "l":0, "b":0},
        title_font=dict(size=20, family="Arial")
    )
    
    print("🚀 Opening map in your default web browser...")
    fig.show()

if __name__ == "__main__":
    # Point directly to your clean dataset
    cleaned_csv_path = r""
    
    create_custom_heatmap(cleaned_csv_path)