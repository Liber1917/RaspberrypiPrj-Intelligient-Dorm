import tensorflow as tf
import numpy as np
from locate_hand import locate_hand
from locate_hand import standardization


print("11111")
train_features = []
train_labels = []
model1 = locate_hand()
print(model1)
for item in model1:
    label = item[0]
    point_dic = item[1]
    point_dic = standardization(point_dic)
    train_labels.append(label)
    train_features.append(point_dic)

train_features = np.array(train_features)  # 转换为 NumPy 数组
train_labels = np.array(train_labels)


model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=64, activation='relu', input_shape=(2, 21, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dense(units=1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_features, train_labels, epochs=10, batch_size=32)

tf.saved_model.save(model, 'model/src')
