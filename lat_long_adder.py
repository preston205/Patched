import pandas as pd
import random

def lat_long(filepath,search_for):
# 
    df = pd.read_csv(filepath)
    Loc = pd.read_csv('data/Locals.csv')
    genre_matrix = pd.read_csv('data/genre_matrix.csv')

    df['latitude'] = None
    df['longitude'] = None
    df['weight'] = None
    df['pull'] = None
    selected = genre_matrix[genre_matrix['Genre'] == search_for]
    #print(selected)

    for idx, row in df.iterrows():
        if df.at[idx, 'Instagram Follower count:'] < df.at[idx, 'Spotify monthly listeners']:
            pull = df.at[idx, 'Spotify monthly listeners'] 
        else:
            pull_modifer = df.at[idx, 'Instagram Follower count:'] / 3
            pull = min(df.at[idx, 'Instagram Follower count:'], df.at[idx, 'Spotify monthly listeners'] + pull_modifer)
        
        df.at[idx,'pull'] = pull
        
        wgt1 = selected.iloc[0][df.at[idx, 'Primary Genre']]
        wgt2 = selected.iloc[0][df.at[idx, 'Primary Genre']]
        wgt3 = selected.iloc[0][df.at[idx, 'Primary Genre']]
        wgt_total = (10 * wgt1) + (6 * wgt2) + (2 * wgt3)
        

        df.at[idx, 'weight'] = wgt_total
        

        match = Loc[Loc['City'] == row['location']]
        if not match.empty:
            df.at[idx, 'latitude'] = match.iloc[0]['latitude'] + (random.randint(-10,10) * 0.001)
            df.at[idx, 'longitude'] = match.iloc[0]['longitude'] + (random.randint(-10,10) * 0.001)


        else:
            print(f"No match found for location: {row['location']}")

    df.to_csv('updated_data.csv', index=False)

    # Check columns exist
    required_cols = ['latitude', 'longitude']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f'CSV must contain columns: {required_cols}')
    return df