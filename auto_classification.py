"""
Authors : inzapp

Github url : https://github.com/inzapp/sigmoid-classifier

Copyright 2021 inzapp Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"),
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import shutil as sh
from concurrent.futures import ThreadPoolExecutor
from glob import glob

import numpy as np
import tensorflow as tf
from cv2 import cv2
from tqdm import tqdm


os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
g_unknown_threshold = 0.5


def load_x_image_path(image_path, color_mode, input_size, input_shape):
    data = np.fromfile(image_path, dtype=np.uint8)
    x = cv2.imdecode(data, color_mode)
    x = cv2.resize(x, input_size)
    if input_shape[-1] == 3:
        x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)  # swap rb
    x = np.asarray(x).astype('float32').reshape((1,) + input_shape) / 255.0
    return x, image_path


def auto_classification(model_path, image_path):
    model = tf.keras.models.load_model(model_path, compile=False)
    input_shape = model.input_shape[1:]
    input_size = (input_shape[1], input_shape[0])
    color_mode = cv2.IMREAD_GRAYSCALE if input_shape[-1] == 1 else cv2.IMREAD_COLOR
    image_path = image_path.replace('\\', '/')
    save_path = image_path

    image_paths = glob(f'{image_path}/*.jpg')
    pool = ThreadPoolExecutor(8)
    fs = []
    for image_path in image_paths:
        fs.append(pool.submit(load_x_image_path, image_path, color_mode, input_size, input_shape))

    for f in tqdm(fs):
        x, image_path = f.result()
        y = model.predict_on_batch(x=x)[0]
        class_index = np.argmax(y)
        score = y[class_index]
        if score < g_unknown_threshold:
            save_dir = f'{save_path}/unknown'
            os.makedirs(save_dir, exist_ok=True)
            sh.move(image_path, save_dir)
        else:
            save_dir = f'{save_path}/{class_index}'
            os.makedirs(save_dir, exist_ok=True)
            sh.move(image_path, save_dir)


def main():
    model_path = r'model.h5'
    img_path = r'/home/imagenet'
    auto_classification(model_path, img_path)


if __name__ == '__main__':
    with tf.device('/cpu:0'):
        main()
