import numpy as np
import pandas as pd
from tqdm import tqdm

def main():
    fbars = pd.read_csv('../data_cleaned/fbars.csv')
    vbars = pd.read_csv('../data_cleaned/tbars.csv')   

    def features (feat_df):
        """
        Assuming that features of each volume bar are the set of features of the 
        LOB volume bar after adding the last message of that volume bar
        """
        import warnings
        if min(feat_df['time']) == max(feat_df['time']):
            warnings.warn("The dataframe consists of elements which belong to the same volume bar")
        df = pd.DataFrame([])

        for i in tqdm(range(min(feat_df['time']), max(feat_df['time'])), desc="Extracting features"):
            df = df.append(feat_df[feat_df['time'] == i].iloc[-1,:], ignore_index=True)
        return df

    df = features(fbars)
    df.to_csv('../data_cleaned/features.csv', index=False)
    
if __name__ == "__main__":
    main()