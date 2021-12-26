### High-level "API" outline

#### Messages and the LimitOrderBook
The conceptual framework behind this implementation is the following.

A LimitOrderBook (or LOB for short) is a data structure that keeps track of
resting orders during a trading day. The state of the book changes when new
messages arrive from the exchange. It is possible to associate a timestamp to
each incoming message. The LOB then evolves at each of these timestamps, and
its state transitions according to the message itself. This means that, for
each message type, a specific update rule is used to compute the new state of
the LOB.

For each security, a large number of messages are sent over the course of a day.
These messages belong to one of 8 possible types:
1. OrderAdd;
2. OrderDelete;
3. OrderModify;
4. OrderModifySamePrio;
5. OrderMassDelete;
6. FullOrderExecution;
7. PartialOrderExecution;
8. ExecutionSummary.

Messages 6 to 8 are only sent by the exchange when a trade happens. The
ExecutionSummary messages, in particular, contain general information about the
trade event. However, they do not directly change the state of the book.
Instead, the updates to the book that result from a trade taking place are
carried by messages 6 and 7.

#### Basic usage
The code assumes a specific workflow when reconstructing the Limit Order Book.
In the first place, list of incoming messages must be created. This list has
been already created for you, so you need not to worry about it.

The messages in the list belong in principle to different message types. They
can however be cast to a "blanket type", called `FullMessage`, which is a
superset of all message types, together with a flag to identify the underlying
specific message type. This means that, in practice, a list of `FullMessage`s
is created directly.

The update rules are very different from message to message. The function
`incremental_update` is overloaded for each message type, and implements all
the update rules. However, to make usage easier, the wrapper
`generic_incremental_update` is provided. This function takes a `FullMessage`
as input, and based on its underlying message type flag, calls the appropriate
`incremental_update`.

#### Feature extraction and volume bars
The LOB is not only a logging device, but it can also act as a data generator.
The basic idea is that, for each state of the book, a set of features can be
extracted/computed. These features can then be collected and analyzed as a
standard "rectangular" dataset (i.e., a simple CSV or columnar file format; we
have coded the library in such a way that these columns are exposed as Numpy
record arrays, which are very closely related to pandas DataFrames).

A fundamental assumption behind our approach is that data should be sampled
according to the trading volume. Usually, bars are created by aggregating all
the data that falls inside a fixed time interval (i.e., 5 minute bars take all
the available data in chunks of 5 minutes and aggregate it). Volume bars
instead focus on the activity of a security: define a threshold value $x$, that
represents the "activity threshold". As soon as the cumulative traded volumes
exceed this threshold, a bar is created, and the data inside it gets
aggregated. The implementation of the LOB assumes this methodology; as such,
the threshold is required as an input parameter when creating a LOB.


The threshold may be exceeded at any point in time (equivalently, at any point
in the list of `FullMessage`s). As such, the function
`generic_incremental_update` outputs:
* `None`, if no volume bar was created as a result of the current message;
* a tuple of (all the trades since the last volume bar, features for the
  current volume bar), if the current message triggered the exceeding of the
  volume threshold, and as a consequence, a volume bar was created.

Another parameter that is required by the LOB is the tick size. In an order
book, the possible prices at which a security is traded are discrete. You can
think of possible prices as points on a grid/lattice, the spacing of which is
fixed and constant. This spacing is sometimes called tick size. A great deal of
research is done by exchanges in order to identify the ideal tick size.

Ideally, this means that the code should look something like this:
```python3
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
# The volume threshold and the ticksize must be provided at instantiation time
volume_threshold = 1000000
ticksize = 0.0001
book = lob.LimitOrderBook(volume_threshold, ticksize)

# Step 3: loop over the messages and feed them to the lob
for msg in tqdm(messages):
    maybe_bars = book.generic_incremental_update(msg)
    # check if, after the last message, the traded volume exceeded the
    # threshold. If so, then maybe_bars will not be None. Instead, it will
    # contain some data that is ready to be turned into a pair of pandas
    # DataFrames.
    if maybe_bars is not None:
        tbars = pd.DataFrame.from_records(maybe_bars[0])
        fbars = pd.DataFrame.from_records(maybe_bars[1])
```

The chunks are composed of two parts: one is the set of trades that participate
in the volume bar (`tbars`); the other is the set of raw features for all
timestamps inside the volume bar (`fbars`).

In general, the two have different lengths: inside a bar, there may have been N
trades, but 10 times as many OrderAdd, OrderModify, ... messages. Since the
final features may be computed from both, aggregations on these DataFrames will
need to be different between the two.

Ideally, the end product should be a DataFrame which has a row of features for
each volume bar.
