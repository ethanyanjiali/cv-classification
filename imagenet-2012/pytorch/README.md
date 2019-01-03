# ImageNet ILSVRC2012 - PyTorch

This directory contains the PyTorch code to replicate famous cliassification models with public ImageNet ILSVRC2012 dataset

## Directory Structure

```
pytorch
|__notebooks        // Jupyter notebooks to visualize the model inference
|__logs             // training logs for the models I trained
|__test_images      // test images for inference visuliazation
|__models           // model network structure pytorch implementations
|__data_load.py     // data loader
|__train.py         // single machine training script
|__train_dist.py    // distributed training script
```

## Set Up Dataset

Follow the instruction here [DATASET.md](../DATASET.md) to download the ILSVRC2012 dataset first.

## System Requirement

I'm training all these models with 8 vCPU, 24GB RAM and one Nvidia P100 GPU (~16G). If you have different hardware, you might need to change some parameters to fit model with your hardware, especially batch size (when memory exceed) and num_workers (for multi-thread loading).

## Start Training

This repo implements many different models. Once you have the dataset ready, you can start the training code by running tasks in the Makefile. I trained some of the implemented models, and provided the training log and model file for your reference.

There're few tips before you acutally start training:

- I use Python 3 for this project
- Make sure you have set up virtual environment and also installed dependencies by `pip install -r requirements.in`
- There're multiple options defined in `train.py`. For example, model to train `-m`, and checkpoint file to use `-c`.
- There're also some examples for how to resume previous paused training in the Makefile.
- To run the notebook, please download the pretrained model to `saved_model` directory first.

## AlexNet
Training Command for V1 and V2:
```
make train_alexnet1
make train_alexnet2
```

Among two versions, I trained AlexNet V2 which achieves 50.98% top 1 accuracy. Some training notes:

- I manually changed learning rate multiple times through training. But used a LR scheduler to in the final version with milestone of 30, 45, 80, 95 epochs and 0.1 decay.
- With default weight init from PyTorch, the loss will stop decreasing around 4.5 so I used Kaiming init instead.
- Data augmentation part is not exactly same with the original paper.
- I modified the log format few times during training, so the log file is not consistent everywhere.

**Training Log**: [alexnet2.txt](logs/alexnet2.txt)

**Pretrained Model File**: [alexnet_v2_yanjiali_12_26_18.pt](https://drive.google.com/file/d/1EGYtcLsEV2ZFv6sSCKNd_fSFxtwI2cYV/view?usp=sharing)

**Notebook Visualization**: [alexnet.ipynb](notebooks/alexnet.ipynb)

## VGG
Training Command for 16 and 19:
```
make train_vgg16
make train_vgg19
```