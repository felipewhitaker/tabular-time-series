from . import TimeSeriesGenerator
import pandas as pd

def get_df(data, p, n, s): #, category_seasonal, test_split = .33):
    """[summary]

    Returns:
        [type]: [description]
    """
    
    # Define ts
    ts = TimeSeriesGenerator(data, p, n, s)
    
    # Iterate over
    features, target = [], []
    for i, (X, y) in enumerate(ts):
        features.append(X)
        target.append(y)
        
    # Set columns
    s_cols = [f'y(ts{s})_{i}' for i in range(1, n + 1)] if s > 0 else []
    x_cols = s_cols + [f'y(t-{i})' for i in range(p)][::-1]
    y_cols = [f'y(t+{i})' for i in range(1, n + 1)]
    
    # Create DataFrame
    dftime = pd.concat([
        pd.DataFrame(features, columns = x_cols),
        pd.DataFrame(target, columns = y_cols)
    ], 
        axis = 1
    )
    
    return dftime