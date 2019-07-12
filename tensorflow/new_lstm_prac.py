'''
This script shows how to predict stock prices using a basic RNN
'''
import tensorflow as tf
import numpy as np
import matplotlib
import os
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential, Model
from tensorflow.keras.preprocessing.sequence import pad_sequences

tf.enable_eager_execution()
tf.set_random_seed(777)  # reproducibility
'''
if "DISPLAY" not in os.environ:
    # remove Travis CI Error
    matplotlib.use('Agg')
'''
import matplotlib.pyplot as plt


def MinMaxScaler(data):
    ''' Min Max Normalization
    Parameters
    ----------
    data : numpy.ndarray
        input data to be normalized
        shape: [Batch size, dimension]
    Returns
    ----------
    data : numpy.ndarry
        normalized data
        shape: [Batch size, dimension]
    References
    ----------
    .. [1] http://sebastianraschka.com/Articles/2014_about_feature_scaling.html
    '''
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)


# train Parameters
seq_length = 7
input_dim = 5
hidden_dim = 10
output_dim = 1
learning_rate = 0.01
iterations = 500

# Open, High, Low, Volume, Close
xy = np.loadtxt('data_stock.csv', delimiter=',')
xy = xy[::-1]  # reverse order (chronically ordered)

# train/test split
train_size = int(len(xy) * 0.7)
train_set = xy[0:train_size]
test_set = xy[train_size - seq_length:]  # Index from [train_size - seq_length] to utilize past sequence

# Scale each
train_set = MinMaxScaler(train_set)
test_set = MinMaxScaler(test_set)

# build datasets
def build_dataset(time_series, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(time_series) - seq_length):
        _x = time_series[i:i + seq_length, :]
        _y = time_series[i + seq_length, [-1]]  # Next close price
        #print(_x, "->", _y)
        dataX.append(_x)
        dataY.append(_y)
    return np.array(dataX), np.array(dataY)

x_data, y_data = build_dataset(train_set, seq_length)
testX, testY = build_dataset(test_set, seq_length)


model = Sequential()

model.add(layers.LSTM(units=hidden_dim, return_sequences=True, dtype = tf.float32))
model.add(layers.TimeDistributed(layers.Dropout(rate = .2)))
model.add(layers.LSTM(units=hidden_dim, dtype = tf.float32))
model.add(layers.Dropout(rate = .2))
model.add(layers.Dense(units=1, dtype = tf.float32))

# creating loss function
def loss_fn(model, x, y, training):
    pred = model(x)
    return tf.reduce_mean(tf.square(tf.subtract(pred, y)), training)

# creating and optimizer
lr = .01
epochs = 30
batch_size = 2
opt = tf.train.AdamOptimizer(learning_rate = lr)

# generating data pipeline
tr_dataset = tf.data.Dataset.from_tensor_slices((x_data, y_data))
#tr_dataset = tr_dataset.shuffle(buffer_size=4)
#tr_dataset = tr_dataset.batch(batch_size=batch_size)

print(tr_dataset)

# training
tr_loss_hist = []

for epoch in range(epochs):
    avg_tr_loss = 0
    tr_step = 0
    
    for x_mb, y_mb in zip(x_data, y_data):
        with tf.GradientTape() as tape:
            tr_loss = loss_fn(model, x=x_mb, y=y_mb, training=True)
        grads = tape.gradient(target=tr_loss, sources=model.variables)
        opt.apply_gradients(grads_and_vars=zip(grads, model.variables))
        avg_tr_loss += tr_loss
        tr_step += 1
    else:
        avg_tr_loss /= tr_step
        tr_loss_hist.append(avg_tr_loss)
    
    if (epoch + 1) % 5 ==0:
        print('epoch : {:3}, tr_loss : {:.3f}'.format(epoch + 1, avg_tr_loss))

yhat = model.predict(x_data)
#yhat = np.argmax(yhat, axis=-1)
#print('accuracy : {:.2%}'.format(np.mean(yhat == y_data)))

plt.plot(tr_loss_hist)

