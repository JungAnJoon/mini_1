'''
This script shows how to predict stock prices using a basic RNN
'''
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
#tf.disable_eager_execution()

tf.set_random_seed(777)  # reproducibility
'''
if "DISPLAY" not in os.environ:
    # remove Travis CI Error
    matplotlib.use('Agg')
'''

tf.reset_default_graph()

'''
def MinMaxScaler(data):
    
    Min Max Normalization
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
    
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)
'''

# train Parameters
seq_length = 10
data_dim = 13
hidden_dim = 20
output_dim = 1
learning_rate = 0.01
iterations = 500

lstm_sizes = 1
keep_prob_ = 1


dataset = pd.read_csv(r'../data/plus/v1/seongsan_1_2014.csv')
test_df = pd.read_csv(r'../data/plus/v1/seongsan_1_2015.csv')
#dataset = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/plus/v1/non_zero_seongsan_1_2014.csv")


base = ['기온(C)', '강수량(mm)', '풍속(m/s)', 
       '풍향(16방위)', '습도(%)', '증기압(hPa)', 
       '이슬점온도(C)', '현지기압(hPa)', '해면기압(hPa)', 
       '일조(hr)', '적설(cm)', '지면온도(C)', '발전량']


xy = dataset[base].values
xyTest = test_df[base].values
#xy = xy[::-1]  # reverse order (chronically ordered)

# train/test split
train_size = int(len(xy) * 0.7)
train_sets = xy
test_sets = xyTest[ (len(xy) - train_size) - seq_length:]  # Index from [train_size - seq_length] to utilize past sequence



# Scale each
train_scaler = MinMaxScaler().fit(train_sets)
test_scaler = MinMaxScaler().fit(test_sets)

train_set = train_scaler.transform(train_sets)
test_set = test_scaler.transform(test_sets)


# build datasets
def build_dataset(time_series, not_scaled ,seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(time_series) - seq_length):
        _x = time_series[i:i + seq_length, :]
        _y = not_scaled[i + seq_length, [-1]]  # Next close price
        #print(_x, "->", _y)
        dataX.append(_x)
        dataY.append(_y)
    return np.array(dataX), np.array(dataY)


trainX, trainY = build_dataset(train_set, train_sets, seq_length)
testX, testY = build_dataset(test_set, test_sets, seq_length)

trainY_scaler = MinMaxScaler().fit(trainY)
testY_scaler = MinMaxScaler().fit(testY)

trainY = trainY_scaler.transform(trainY)
testY = testY_scaler.transform(testY)



# input place holders
X = tf.placeholder(tf.float32, [None, seq_length, data_dim])
Y = tf.placeholder(tf.float32, [None, 1])
'''
# build a LSTM network
cell = tf.keras.layers.LSTMCell(hidden_dim)
outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
Y_pred = tf.contrib.layers.fully_connected(
    outputs[:, -1], output_dim, activation_fn=None)  # We use the last cell's output
'''


lstms = []
for i in range(lstm_sizes):
    lstms.append(tf.contrib.rnn.BasicLSTMCell(
    num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh))

# Add dropout to the cell
drops = [tf.contrib.rnn.DropoutWrapper(lstm, output_keep_prob=keep_prob_) for lstm in lstms]

# Stack up multiple LSTM layers, for deep learning

cell = tf.contrib.rnn.MultiRNNCell(drops)


#cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)

Y_pred = tf.contrib.layers.fully_connected(
    outputs[:, -1], output_dim, activation_fn=None)  # We use the last cell's output

# cost/loss
loss = tf.reduce_sum(tf.square(Y_pred - Y))  # sum of the squares
# optimizer
optimizer = tf.train.AdamOptimizer(learning_rate)
#optimizer = tf.train.RMSPropOptimizer(learning_rate)

train = optimizer.minimize(loss)

# RMSE
targets = tf.placeholder(tf.float32, [None, 1])
predictions = tf.placeholder(tf.float32, [None, 1])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets - predictions)))

# R squared
total_error = tf.reduce_sum(tf.square(tf.subtract(targets, tf.reduce_mean(targets))))
unexplained_error = tf.reduce_sum(tf.square(tf.subtract(targets, predictions)))
R_squared = tf.subtract(1.0, tf.div(unexplained_error, total_error))

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)

    # Training step
    for i in range(iterations):
        _, step_loss = sess.run([train, loss], feed_dict={
                                X: trainX, Y: trainY})
        if i%100 == 0 or i == iterations-1:
            print("[step: {}] loss: {}".format(i, step_loss))

    # Test step
    test_predict = sess.run(Y_pred, feed_dict={X: testX})
    rmse_val = sess.run(rmse, feed_dict={
                    targets: testY, predictions: test_predict})
    
    r_squared = sess.run(R_squared, feed_dict={
                    targets: testY, predictions: test_predict})
    print("----------Scaled----------")
    print("Target std: {}".format(np.std(testY)))
    print("RMSE: {}".format(rmse_val))
    print("R squared: {}".format(r_squared))
    
    
    mapeT = []
    mapeP = []
    for t, p in zip(testY, test_predict):
        if t != 0:
            mapeT.append(t)
            mapeP.append(p)
    mapeT = np.array(mapeT)
    mapeP = np.array(mapeP)
    
    print("MAPE: {}".format(np.mean(np.abs((mapeT - mapeP) / mapeT)) * 100))
    
    # Plot predictions
    plt.plot(testY, color='blue')
    plt.plot(test_predict, color='red')
    plt.xlabel("Time Period")
    plt.ylabel("Wind Power")
    plt.show()
    
    
    
    print("----------Non_Scaled----------")
    
    reverseTestY = testY_scaler.inverse_transform(testY)
    reversePredict = testY_scaler.inverse_transform(test_predict)
    
    print("Target std: {}".format(np.std(reverseTestY)))
    
    non_scaled_rmse_val = sess.run(rmse, feed_dict={
                    targets: reverseTestY, predictions: reversePredict})
    
    non_scaled_r_squared = sess.run(R_squared, feed_dict={
                    targets: reverseTestY, predictions: reversePredict})
    print("RMSE: {}".format(non_scaled_rmse_val))
    print("R squared: {}".format(non_scaled_r_squared))
    
    mapeT = []
    mapeP = []
    for t, p in zip(reverseTestY, reversePredict):
        if t != 0:
            mapeT.append(t)
            mapeP.append(p)
    mapeT = np.array(mapeT)
    mapeP = np.array(mapeP)
    
    print("MAPE: {}".format(np.mean(np.abs((mapeT - mapeP) / mapeT)) * 100))
    
    # Plot predictions
    plt.plot(reverseTestY, color='blue')
    plt.plot(reversePredict, color='red')
    plt.xlabel("Time Period")
    plt.ylabel("Wind Power")
    plt.show()
    
    np.mean(reverseTestY)
    np.std(reverseTestY)/2
    np.mean(reversePredict)
    
    

