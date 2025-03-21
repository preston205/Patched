import pandas as pd

def load_geodata(filepath):
    """
    Load geographic data for heatmap.
    CSV columns: latitude, longitude, value
    """
    df = pd.read_csv(filepath)
    # Check columns exist
    required_cols = ['latitude', 'longitude', 'value']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f'CSV must contain columns: {required_cols}')
    return df
