import pandas as pd
import numpy as np
from datetime import datetime

def main(tick_size=1e-4, time_conversion=1e9): 

    df=pd.read_csv("../data_cleaned/tbars.csv")
    # drop timetags which are previous to observation day
    date_acquisition = int(datetime.fromisoformat('2020-04-06').timestamp())
    df.drop (df[df['RequestTime']<date_acquisition].index, axis=0, inplace=True)
    df = df.sort_values(['RequestTime'], ignore_index=True)
    df['RequestTime_isoformat'] = df['RequestTime'].apply(lambda x: datetime.fromtimestamp(x/time_conversion))
    df=df.drop(['AggressorTime', 'ExecID', 'RestingHiddenQty', 'label_volume_bar'], axis=1)
    df['AggressorSide'] = df['AggressorSide'].apply(lambda x: -1 if x==49 else 1) #-1 bid side, 1 ask side
    df["LastPx"]*=tick_size

    time_delta = 5 #in minutes
    bin_edges = []

    #discretizing time in time_delta
    t = min(df['RequestTime_isoformat'])
    from datetime import timedelta
    time_delta = timedelta(minutes=time_delta)
    while t <= max(df['RequestTime_isoformat']) + time_delta:
        bin_edges.append(t)
        t = t + time_delta

    #binning data
    df['time_bin'] = pd.cut(df['RequestTime_isoformat'], bin_edges)
    df.dropna(inplace=True)
    df.index = np.arange(len(df))

    #computing occurences
    ask_side = df[df['AggressorSide']==1]
    bid_side = df[df['AggressorSide']==-1]

    middle_point_bins = [b+time_delta/2. for b in bin_edges][:-1]

    bid_observations = -bid_side.groupby('time_bin').sum()['AggressorSide']
    ask_observations = ask_side.groupby('time_bin').sum()['AggressorSide']
    occurrences = pd.DataFrame(bin_edges[1:], columns=['discr_time_isoformat'])

    occurrences['bid_observations'] = bid_observations.to_numpy()
    occurrences['ask_observations'] = ask_observations.to_numpy()
    occurrences.to_csv('../data_cleaned/occurrences.csv')

if __name__ == "__main__":
    main()