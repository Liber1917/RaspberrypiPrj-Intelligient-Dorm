import tensorflow as tf
import numpy as np
from Gesture.locate_hand import locate_hand
from Gesture.locate_hand import process_mark_data

num_classes = 3

print("11111")
train_features = []
train_labels = []
model1 = locate_hand()
for item in model1:
    label = item[0]
    point_dic = item[1]
    point_dic = process_mark_data(point_dic)
    train_labels.append(label)
    train_features.append(point_dic)
print(train_features)
train_features = np.array(train_features)  # 转换为 NumPy 数组
train_labels = tf.constant(train_labels, dtype=tf.int32)  # 转换为 TensorFlow 张量并设置数据类型
train_labels = tf.one_hot(train_labels, depth=3)
print(train_labels)


model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=64, activation='relu', input_shape=(2, 20, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dense(units=num_classes, activation='softmax')
])

print(train_labels.shape, model.output_shape)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 假设 train_labels 是经过独热编码的标签数据
model.fit(train_features, train_labels, epochs=10, batch_size=32)

test_loss, test_accuracy = model.evaluate(train_features, train_labels)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

tf.saved_model.save(model, 'model/src')
