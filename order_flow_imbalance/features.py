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
parser.add_argument("--data_frac", default=0.1, help="fraction of messages to read", type=float)

def main(data, volume_threshold, ticksize, maxlevel, data_frac):

    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    messages = lob.parse_FullMessages(data)
    logging.info("Messages uploaded correctly")

    book = lob.LimitOrderBook(volume_threshold, ticksize)
    logging.info("Book created correctly")
    
    time = 0
    n_msg = int(len(messages) * data_frac)
    for msg in tqdm(messages[:n_msg], desc="Reconstructing the book"):
        bars = book.generic_incremental_update(msg)
        if bars is not None and time == 0:
            tbars = pd.DataFrame.from_records(bars[0])
            fbars = pd.DataFrame.from_records(bars[1])
        


if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)


