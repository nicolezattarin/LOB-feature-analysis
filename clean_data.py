from tqdm import tqdm
import pandas as pd
import numpy as np
import db_lob as lob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--messages_file_path", default='2505133.csv', help="filename.", type=str)
parser.add_argument("--volume_threshold", default=1000000, help="Volume threshold", type=int)
parser.add_argument("--ticksize", default=0.0001, help="ticksize", type=float)
parser.add_argument("--data_frac", default=0.95, help="fraction of messages to read", type=float)


def main(messages_file_path, volume_threshold, ticksize, data_frac):
    """
    Takes a csv file with messages and builds the LOB. 
    The LOB is then saved in a .csv file, in order to be available also without employing directly the package db_lob
    This code stores also the time evolution of the spread and save it in a .csv file.
    
    args:
        messages_file_path: path to the csv file containing the messages
        volume_threshold: volume threshold for the messages to be considered
        ticksize: ticksize used for the LOB
        data_frac: fraction of messages to read
    """

    print("Reading messages...")
    messages = lob.parse_FullMessages(messages_file_path)
    print("Messages read!")

    #building the book
    book = lob.LimitOrderBook(volume_threshold, ticksize)

    # ZATTA fix datafrac = 1
    print("Building the LOB...")
    print(messages_file_path)
    spread = []
    vbar_label = 0
    n_msg = int(len(messages) * data_frac)
    for msg in tqdm(messages[:n_msg], desc="Reconstructing the book"):
        bars = book.generic_incremental_update(msg)
        if bars is not None and vbar_label == 0:
            vbars = pd.DataFrame.from_records(bars[0])
            fbars = pd.DataFrame.from_records(bars[1])
            vbars['volume_bar_label'] = vbar_label
            fbars['volume_bar_label'] = vbar_label
            vbar_label += 1
            ask_side, bid_side = book.askTree, book.bidTree
            spread.append(np.abs(min(ask_side)-max(bid_side)))
        elif bars is not None and vbar_label != 0:
            vtemp = pd.DataFrame.from_records(bars[0])
            ftemp = pd.DataFrame.from_records(bars[1])
            vtemp['volume_bar_label'] = vbar_label
            ftemp['volume_bar_label'] = vbar_label
            vbars = vbars.append(vtemp)
            fbars = fbars.append(ftemp)
            vbar_label += 1
            ask_side, bid_side = book.askTree, book.bidTree
            spread.append(np.abs(min(ask_side)-max(bid_side)))

    # function to read the data and return a df
    def df_from_book(book):
        import pandas as pd
        ask_side, bid_side = book.askTree, book.bidTree
        a = list(ask_side.values())
        b = list(bid_side.values())
        ask_price, bid_price, ask_volume, bid_volume = [], [], [], []
        for ask, bid in zip(a,b):
            ask_price.append(ask.price)
            bid_price.append(bid.price)
            ask_volume.append(ask.totalVolume)
            bid_volume.append(bid.totalVolume)
        df = pd.DataFrame(ask_volume, columns=['ask_volume'])
        df['ask_price'] = ask_price
        df['bid_volume'] = bid_volume
        df['bid_price'] = bid_price
        return df

    # saving the LOB as a csv file
    df = df_from_book(book)
    import os
    dir = 'data_cleaned'
    if os.path.isdir(dir)==False:
            os.mkdir(dir)
    df.to_csv(dir+'/LOB.csv', index=False)

    # saving the spread as a csv file
    spread = pd.DataFrame(spread)
    spread.to_csv(dir+'/spread.csv', index=False)

    # saving tbars fbars
    # vbars are the trades that participate in the volume bar.
    # fbars is the set of raw features for all timestamps inside the volume bar.
    vbars.to_csv(dir+'/vbars.csv', index=False)
    fbars.to_csv(dir+'/fbars.csv', index=False)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)