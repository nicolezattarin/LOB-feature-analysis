

from datetime import datetime

time_series = ofi.drop(['bin_label', 'time_bin'], axis=1)
time_series.index.name = 'date'
time_series.index = ofi['time_bin'].apply(lambda x: datetime.strptime(ofi['time_bin'][0][1:27],"%Y-%m-%d %H:%M:%S.%f" ))

# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = [], []
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	df = pd.concat(cols, axis=1)
	df.columns = names
	df.dropna(inplace=True)
	return df

#preprocessing 
from sklearn.preprocessing import MinMaxScaler #scaling each feature to a given range
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(time_series.values)
data = series_to_supervised(data, 1, 1).values

train_frac = 0.5
val_frac = 0.25
test_frac = 0.25
N_train = int(train_frac*len(time_series))
N_val = int(val_frac*len(time_series))
N_test = int(test_frac*len(time_series))

train = data[:N_train, :]
val = data[N_train:N_train+N_val, :]
test = data[N_train+N_val:, :]

train_data, train_target = train[:, :-1], train[:, -1]
val_data, val_target = val[:, :-1], val[:, -1]
test_data, test_target = test[:, :-1], test[:, -1]

train_data = train_data.reshape((train_data.shape[0], 1, train_data.shape[1]))
val_data = val_data.reshape((val_data.shape[0], 1, val_data.shape[1]))
test_data = test_data.reshape((test_data.shape[0], 1, test_data.shape[1]))

# design network
from keras.models import Sequential
from keras.layers import Dense, LSTM

model = Sequential()
model.add(LSTM(50, input_shape=(train_data.shape[1], train_data.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')

fitted = model.fit(train_data, train_target, epochs=50, batch_size=72, 
				validation_data=(val_data, val_target), verbose=0, shuffle=False)
fig, ax = plt.subplots(figsize=(8,5))
sns.set_theme(style='white', font_scale=1.5, palette='Dark2')
sns.lineplot(np.arange(len(fitted.history['loss'])), fitted.history['loss'], label='train', lw=3)
sns.lineplot(np.arange(len(fitted.history['val_loss'])), fitted.history['val_loss'], label='test', lw=3)

# make a prediction
yhat = model.predict(test_data)
test_data = test_data.reshape((test_data.shape[0], test_data.shape[2]))

# invert scaling for forecast
inv_yhat = np.concatenate((yhat, test_data[:, 1:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

# invert scaling for actual
test_y = test_target.reshape((len(test_target), 1))
inv_y = np.concatenate((test_y, test_data[:, 1:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]

# calculate RMSE
from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

#time evoltion
import matplotlib.pyplot as plt
import seaborn as sns
ms = 0
lw = 2
fig, ax = plt.subplots(figsize=(13,7))

for c in time_series.columns:
    g = sns.lineplot(x=np.arange(len(time_series)), y=time_series[c] , ax=ax, 
                linewidth=lw, marker='o', markersize=ms, label=c)
g.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)

# An inner plot to show the peak frequency
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
axins = inset_axes(ax,  "30%", "40%" ,loc="upper right", borderpad=3)
maxlevel = 10
for l in range(maxlevel):
    g = sns.lineplot(x=np.arange(len(time_series)), y=time_series['OFI_{}'.format(l)] , ax=axins, 
                linewidth=1, marker='o', markersize=ms, label=c)
axins.get_legend().remove()
axins.set_ylim(-3.5e7,3.5e7)
axins.set_ylabel('')
axins.set_xlabel('')
axins.set_xticklabels([])
axins.set_yticklabels([])


# fft
from scipy.fftpack import fft, fftfreq, ifft
time_step = 1e-3
signal = time_series['OFI_0'].to_numpy()
signal_fft = fft(signal)
power = np.abs(signal_fft)
freq = fftfreq(len(signal), d=time_step) 

pos_mask = np.where(freq > 0)
pfreq = freq[pos_mask]
peak_freq = pfreq[power[pos_mask].argmax()]

fcleaned = signal_fft.copy()
fcleaned[(np.abs(freq) )> peak_freq] = 0
cleaned_signal = ifft(fcleaned)
real_signal = np.real(cleaned_signal)


fig, ax = plt.subplots(2, 1, figsize=(10, 6))
sns.set_theme(style='white', font_scale=1.5, palette ='Dark2')
sns.lineplot(x=freq, y=power, ax=ax[0], lw=lw, label='power')
time = np.arange(len(real_signal))

sns.lineplot(x=time, y=real_signal, ax=ax[1], lw=lw, label = 'real')
