import folium
from folium.plugins import HeatMap

def create_heatmap(df, map_center, weight_threshold, zoom_start=15, output_file='heatmap.html'):
    """
    Creates and saves an interactive heatmap using Folium.
    """
    
    # Initialize the map centered around provided coordinates
    fmap = folium.Map(location=map_center, zoom_start=8, tiles = 'CartoDB positron' )



# Filter data points by weight threshold
    heat_data = [
        [row['latitude'], row['longitude'], float(row['weight'])]
        for _, row in df.iterrows()
        if int(row['weight']) >= weight_threshold
    ]

    
    for idx, row in df.iterrows():
        if df.at[idx,'weight'] >= weight_threshold:
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f" {row['Band name:'], row['Band Instagram handle:']}"
                ).add_to(fmap)


    # Add heatmap
    HeatMap(data=heat_data, radius=15).add_to(fmap)

    # Save to HTML
    fmap.save('heatmap.html')
    print('got here')
