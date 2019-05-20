import pandas as pd
import numpy as np
import tensorflow as tf
# import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

print(tf.__version__)
from tensorflow import keras
from sklearn.utils import shuffle

filename = 'video_stats.csv'
content = pd.read_csv(filename, encoding='utf8')
content = shuffle(content)
train_labels = content['Pts'][:-300]
test_labels = content['Pts'][-300:]

# for i in content:
#     print(i)

train_data = [[content['View'][idx], content['Danmaku'][idx], content['Reply'][idx], content['Favorite'][idx],
               content['Coin'][idx], content['Share'][idx], content['Like'][idx]
               ] for idx, val in enumerate(content['Pts'][:-300])]

test_data = [[content['View'][idx], content['Danmaku'][idx], content['Reply'][idx], content['Favorite'][idx],
              content['Coin'][idx], content['Share'][idx], content['Like'][idx]
              ] for idx, val in enumerate(content['Pts'][-300:])]

train_data = np.array(train_data)
test_data = np.array(test_data)

mean = train_data.mean(axis=0)
std = train_data.std(axis=0)

train_data = (train_data - mean) / std
test_data = (test_data - mean) / std
print(train_data[0])


def build_model():
    model = keras.Sequential([
        keras.layers.Dense(64, activation=tf.nn.relu, input_shape=(7,)),
        keras.layers.Dense(64, activation=tf.nn.relu),
        keras.layers.Dense(1)
    ])
    optimizer = tf.train.RMSPropOptimizer(0.001)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae'])
    return model


model = build_model()
model.summary()


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')


EPOCHS = 500

history = model.fit(train_data, train_labels, epochs=EPOCHS, validation_split=0.2, verbose=0, callbacks=[PrintDot()])


def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [1000$]')
    plt.plot(history.epoch, np.array(history.history['mean_absolute_error']), label='Train Loss')
    plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']), label='Val Loss')
    plt.legend()
    plt.ylim([0, 5])


plot_history(history)

model = build_model()
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20)
history = model.fit(train_data, train_labels, epochs=EPOCHS, validation_split=0.2, verbose=0,
                    callbacks=[early_stop, PrintDot()])

[loss, mae] = model.evaluate(test_data, test_labels, verbose=0)
print("Testing ser Mean Abs Error: ${:7.2f}".format(mae))

test_predictions = model.predict(test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.axis('equal')
plt.xlim(plt.xlim())
plt.ylim(plt.ylim())
_ = plt.plot([-100, 100], [-100, 100])
error = test_predictions - test_labels
plt.hist(error, bins=50)
plt.xlabel("Prediction Error")
_ = plt.ylabel("Count")

test_predictions = model.predict(test_data)

diffs = []

for idx, val in enumerate(test_labels):
    diff = val - test_predictions[idx] / 2
    diffs.append(diff)
    print(val, test_predictions[idx] / 2, diff)
print('!!!!!!!!!!!!!!!!!!!!')
print(max(diffs), min(diffs))
