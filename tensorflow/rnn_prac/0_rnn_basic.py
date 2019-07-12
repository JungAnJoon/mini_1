import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)
tf.enable_eager_execution()

 # One hot encoding for each char in 'hello'
h = [1, 0, 0, 0]
e = [0, 1, 0, 0]
l = [0, 0, 1, 0]
o = [0, 0, 0, 1]

x_data = np.array([[h]], dtype=np.float32)

hidden_size = 2
cell = layers.SimpleRNNCell(units = hidden_size)
rnn = layers.RNN(cell, return_sequences=True, return_state = True)
outputs, states = rnn(x_data)


# equivalent to above case
#rnn = layers.SimpleRNN(units=hidden_size, return_sequences=True,
#                       return_state=True) # layers.SimpleRNNCell + layers.RNN
#
#outputs, states = rnn(x_data)

print('x_data: {}, shape: {}'.format(x_data, x_data.shape))
print('outputs: {}, shape: {}'.format(outputs, outputs.shape))
print('states: {}, shape: {}'.format(states, states.shape))



# One cell RNN input_dim (4) -> output_dim (2). sequence : 5
x_data = np.array([[h,e,l,l,o]], dtype = np.float32)

rnn = layers.SimpleRNN(units=2, return_sequences = True, return_state = True)
outputs, states = rnn(x_data)

print('x_data: {}, shape: {}'.format(x_data, x_data.shape))
print('outputs: {}, shape: {}'.format(outputs, outputs.shape))
print('states: {}, shape: {}'.format(states, states.shape))


