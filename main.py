from lat_long_adder import lat_long
from heat_map import create_heatmap

def main():
    filepath = 'data.csv'

    looking_for = 'Indie Pop'

    map_center = [40.758701, -111.876183]

    weight_threshold = 50

    # Load geographic data
    df = lat_long(filepath, looking_for)

    # Generate Folium heatmap visualization
    create_heatmap(df, map_center, weight_threshold)

    print("✅ Heatmap saved as 'heatmap.html'.")

if __name__ == '__main__':
    main()
