import pandas as pd
import plotly.express as px
import os

def create_snowfall_heatmap(data_file):
    # Check if the cleaned data file exists
    if not os.path.exists(data_file):
        print(f"❌ Error: Cannot find the data file at {data_file}")
        print("Please run your filtering script (filter_snowfall.py) first.")
        return

    print(f"📖 Loading cleaned weather station data from: {data_file}")
    df = pd.read_csv(data_file)
    
    target_col = 'ANN-SNOW-NORMAL'
    
    print("🗺️ Rendering interactive Mapbox density heatmap...")
    
    # Generate the geographic density heatmap
    fig = px.density_mapbox(
        df, 
        lat='LATITUDE', 
        lon='LONGITUDE', 
        z=target_col, 
        radius=12,                        # Controls how much the heat points blend together
        center=dict(lat=37.0902, lon=-95.7129), # Coordinates to center the map over the US
        zoom=3.5,                         # Starting zoom level (fits the contiguous US nicely)
        mapbox_style="carto-positron",    # Clean, light-colored background map layer (No API key needed)
        color_continuous_scale="Blues",   # Lighter colors = less snow, darker blue = high snow
        title="Average Annual US Snowfall Baseline (1991–2020 Normals)",
        labels={target_col: 'Annual Snowfall (Inches)'},
        hover_name='NAME'                 # Displays the station/city name when hovering over a point
    )
    
    # Maximize the layout margins to make the map fill the entire window
    fig.update_layout(
        margin={"r":0, "t":50, "l":0, "b":0},
        title_font=dict(size=20, family="Arial")
    )
    
    print("🚀 Opening map in your default web browser...")
    # This will trigger your browser to open an interactive HTML window
    fig.show()

if __name__ == "__main__":
    # Point directly to your polished, clean dataset
    cleaned_csv_path = r""
    
    create_snowfall_heatmap(cleaned_csv_path)