from lat_long_adder import lat_long
from heat_map import create_heatmap
import pandas as pd

def main():
    loc = pd.read_csv('data/Locals.csv')
    filepath = 'data/data.csv'

    looking_for = input("What genre are you looking for? ")

    map_center = 40.758701,-111.876183




    weight_threshold = int(input("What weight threshold would you like to apply? "))

    # Load geographic data
    df = lat_long(filepath, looking_for)

    # Generate Folium heatmap visualization
    create_heatmap(df, map_center, weight_threshold)

    print("✅ Heatmap saved as 'heatmap.html'.")

if __name__ == '__main__':
    main()
