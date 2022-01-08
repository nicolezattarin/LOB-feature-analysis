import pandas as pd
import numpy as np
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--data", default='../data_cleaned/time_evolution_10_levels.csv', help="filename.", type=str)
parser.add_argument("--maxlevel", default=10, help="maximum level of the book to study", type=int)
parser.add_argument("--n_intervals", default=1e3, help="number of time intervals", type=float)

def main(data, maxlevel, n_intervals):
    """
    
    """
    df = pd.read_csv(data)

    #cleaning time column
    df = df.groupby('time', sort=False).agg(np.mean)
    df = df.sort_values(['time'], ignore_index=True)
    df.drop ([0,1], axis=0, inplace=True)
    df['time'] = df.index
    df.index = range(len(df))

    #computing the quantities delta V delta D
    for i in range(maxlevel):
        print('level {}'.format(i))

        check_bid_prices = np.diff (df['bid_prices_{}'.format(i)])
        check_ask_prices = np.diff (df['ask_prices_{}'.format(i)])
        delta_W = [0]
        delta_V = [0]
        j = 1
        
        # this process can be optimized by employimg .diff and masks 
        with tqdm(total=len(df)) as pbar:
            for bcheck, acheck in zip(check_bid_prices,check_ask_prices):
                if bcheck > 0:
                    delta_W.append(df['bid_volumes_{}'.format(i)][j])
                elif bcheck == 0:
                    delta_W.append(df['bid_volumes_{}'.format(i)][j] - \
                                df['bid_volumes_{}'.format(i)][j-1])
                else:
                    delta_W.append(- df['bid_volumes_{}'.format(i)][j-1])

                if acheck < 0:
                    delta_V.append(df['ask_volumes_{}'.format(i)][j])
                elif acheck == 0:
                    delta_V.append(df['ask_volumes_{}'.format(i)][j] - \
                                df['ask_volumes_{}'.format(i)][j-1])
                else:
                    delta_V.append(-df['ask_volumes_{}'.format(i)][j-1])
                pbar.update(1)
        df['delta_W_{}'.format(i)] = delta_W
        df['delta_V_{}'.format(i)] = delta_V
        df['e_{}'.format(i)] = df['delta_W_{}'.format(i)]-df['delta_V_{}'.format(i)]
    
    #drop row without a previous item, does  not make sense in .diff
    df = df.drop([0], axis=0) 
    df.index = range(len(df))
    df.to_csv('../data_cleaned/OFI_{}_levels_computed.csv'.format(maxlevel))

    # discretization to compute OFI
    n_intervals = int(n_intervals)
    interval_size = int ((max(df['time'])-min(df['time'])) / n_intervals)

    print('Interval size', interval_size)
    print('Number of intervals', n_intervals)

    timestamps = np.array([min(df['time']) + i*interval_size for i in range(n_intervals+1)], dtype=np.float64)
    df['binned_time']= pd.cut(df['time'].astype('float'), timestamps, right=True)
    df = df.dropna()

    #ofi computaition
    ofi = df.groupby('binned_time', sort=True).agg(np.sum)
    ofi = ofi.drop(['time', 'mid_price'], axis=1)
    for i in range(maxlevel):
        ofi = ofi.drop(['bid_volumes_{}'.format(i), 'ask_volumes_{}'.format(i),\
            'bid_prices_{}'.format(i), 'ask_prices_{}'.format(i),
            'delta_W_{}'.format(i), 'delta_V_{}'.format(i)], axis=1)


if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)