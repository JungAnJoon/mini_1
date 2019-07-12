import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# Importing the dataset
dataset = pd.read_csv("/Users/hongbeomchoe/Desktop/capstone/data/plus/v1/seongsan_1_2014.csv")
X = dataset.iloc[:, 2:-1].values
y = dataset.iloc[:, -1:].values
