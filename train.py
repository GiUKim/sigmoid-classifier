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
from sigmoid_classifier import SigmoidClassifier

if __name__ == '__main__':
    SigmoidClassifier(
        train_image_path=r'/home3/INCIDENT/cf/big/big_cf/train',
        validation_image_path=r'/home3/INCIDENT/cf/big/big_cf/validation',
        input_shape=(64, 64,3),
        lr=0.003,
        momentum=0.9,
        batch_size=32,
        iterations=1000000,
        showcam=True,
        activation_layer_name='activation_4',
        backprop_last_layer_name='conv2d_6').fit()
