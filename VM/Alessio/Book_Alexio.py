from tqdm import tqdm
import pandas as pd
import numpy as np
import db_lob as lob


# Step 1: load a list of messages
messages_file_path = '2505133.csv'
print("Reading messages...")
messages = lob.parse_FullMessages(messages_file_path)
print("Messages read!")

# Step 2: create a LimitOrderBook object
# Some parameters are specified at instantiation time; they are related to the
# inner workings of the book:
#   * volume_threshold: this implementation of the book performs automatic
#   volume-based sampling. Instead of producing an aggregate snapshot of the
#   state of the book every, say, N minutes, it does so every time the amount
#   of traded volumes exceeds some threshold, which is aptly called
#   "volume_threshold".
#   * ticksize: in an order book, the possible prices at which a security is
#   traded are discrete. You can think of possible prices as points on a
#   grid/lattice, the spacing of which is fixed and constant. This spacing is
#   sometimes called tick size. The given value is the correct one, and you
#   should not worry about it too much.
volume_threshold = 1000000
ticksize = 0.0001
book = lob.LimitOrderBook(volume_threshold, ticksize)
print(dir(book))

# Step 3: loop over the messages and feed them to the lob
# Just for testing, let's just look at the first N% messages.
pct = 0.1
n_msg = int(len(messages) * pct)
for msg in tqdm(messages[:n_msg], desc="Reconstructing the book"):
    # Feed the message to the book. The method `generic_incremental_update`
    # takes care of all the business logic, and updates the state of the book.
    # Additionally, if a volume bar was created, it outputs that; otherwise, it
    # just gives a None.
    maybe_bars = book.generic_incremental_update(msg)
    # Check if, after the last message, the traded volume exceeded the
    # threshold. If so, then maybe_bars will not be None. Instead, it will
    # contain some data that is ready to be turned into a pair of pandas
    # DataFrames.
    if maybe_bars is not None:
        vbars = pd.DataFrame.from_records(maybe_bars[0])
        fbars = pd.DataFrame.from_records(maybe_bars[1])


# You can explore and access the book's parts from Python.
# The two sides are named askTree and bidTree. In Python, they are two
# dictionaries, with prices as keys and lists of Orders as values. Due to
# how the C++ backend works, the entries are sorted by price.
ask_side, bid_side = book.askTree, book.bidTree
# For instance, here is how you can retrieve the list of orders at the best
# prices for both ask and bid sides.
best_ask, best_bid = min(ask_side), max(bid_side)
# You can also get an idea about the appearance of the book by simply
# printing it out.
print(book)
