import numpy as np
import pandas as pd
from tqdm import tqdm
import db_lob as lob
import argparse
import logging 

parser = argparse.ArgumentParser()
parser.add_argument("--data", default='../data/2505133.csv', help="filename.", type=str)
parser.add_argument("--volume_threshold", default=1000000, help="Volume threshold", type=int)
parser.add_argument("--ticksize", default=0.0001, help="ticksize", type=float)
parser.add_argument("--maxlevel", default=10, help="maximum level of the book to study", type=int)
parser.add_argument("--data_frac", default=0.01, help="fraction of messages to read", type=float)

def main(data, volume_threshold, ticksize, maxlevel, data_frac):
    """
    Computes the necessary quantities to compute the order flow imbalance, 
    see R. Cont, A. Kukanov, S. Stoikov, 'The Price Impact of Order Book Events', and
    K. Xu1, M.D. Gould1, and S.D. Howison1, 'Multi-Level Order-Flow Imbalance in a Limit Order Book'

    args:
        data: path to the dataframe containing the raw messages
        volume_threshold: volume threshold build a volume bar
        ticksize: discretization interval of prices at which a security is
        maxleveò: maximum level of the book to study
        data_frac: fraction of messages to read
    """

    messages = lob.parse_FullMessages(data)
    book = lob.LimitOrderBook(volume_threshold, ticksize)

    bid_prices, bid_volumes, ask_prices, ask_volumes, time, mid_price = [],[],[],[],[],[]

    n_msg = int(len(messages)*data_frac)
    for msg in tqdm(messages[:n_msg], desc="Reconstructing the book"):
        bars = book.generic_incremental_update(msg)
        if bars is not None:
            ask_side, bid_side = book.askTree, book.bidTree

            if not (any(ask_side) and any(bid_side)): continue
            
            ask = list(ask_side.values())
            bid = list(bid_side.values())

            if len(ask) < maxlevel or len(bid) < maxlevel: continue

            a = ask[:maxlevel]
            b = bid[:maxlevel]

            # try: old_a and old_b
            # except: #if old_a and old_b are not defined
            #     old_a = a
            #     old_b = b
            # else: #check if the book has changed
            #     if np.all(a == old_a) and np.all(b == old_b): continue
            # old_a = a
            # old_b = b
            ask_prices.append([x.price for x in a])
            ask_volumes.append([x.totalVolume for x in a])
            bid_prices.append([x.price for x in b])
            bid_volumes.append([x.totalVolume for x in b])
            mid_price.append(np.abs(a[0].price-b[0].price)/ticksize)
            time.append(book.datetime)

    df = pd.DataFrame(time,columns=['time'])
    for i in tqdm (range(maxlevel), desc = 'Assembling levels of the DataFrame'):
        df['ask_price_{}'.format(i)] = np.array(ask_prices, dtype=object)[:,i]
        df['ask_volume_{}'.format(i)] = np.array(ask_volumes, dtype=object)[:,i]
        df['bid_price_{}'.format(i)] = np.array(bid_prices, dtype=object)[:,i]
        df['bid_volume_{}'.format(i)] = np.array(bid_volumes, dtype=object)[:,i]
    df['mid_price'.format(i)] = mid_price

    import os
    dir = '../data_cleaned'
    if os.path.isdir(dir)==False:
            os.mkdir(dir)
    print('Saving the DataFrame to {}'.format(dir))
    df.to_csv(dir+'/time_evolution_{}_levels.csv'.format(maxlevel), index=False)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)


