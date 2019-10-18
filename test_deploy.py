# -*- coding: utf-8 -*-
import argparse

from sagemaker.tensorflow import TensorFlowModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='training script')
    parser.add_argument('--model_path', type=str)

    args = parser.parse_args()

    model_data = args.model_path
    cifar10_estimator = TensorFlowModel(model_data=model_data)

    cifar10_estimator.deploy(initial_instance_count=1,
                             instance_type='ml.m4.xlarge')
