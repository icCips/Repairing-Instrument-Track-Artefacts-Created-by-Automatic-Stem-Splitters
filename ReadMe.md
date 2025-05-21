# Repairing Instrument Track Artefacts Created by Automatic Stem Splitters: A Deep Learning Approach

To keep the size of this code submission reasonable, models are omitted. This file contains instructions for obtaining and placing model files

**Wave-U-Net Model**

## Downloading our pretrained models

Download our pretrained model [here](https://www.dropbox.com/s/r374hce896g4xlj/models.7z?dl=1).
Extract the archive into the ``checkpoints`` subfolder in this repository, so that you have one subfolder for each model (e.g. ``REPO/checkpoints/waveunet``)

*These instructions are taken from dataset_construction/Wave-U-Net-Pytorch/README.md*

**SGMSE Datasets**

Training datasets are available [here](https://drive.google.com/drive/folders/18C3gyV-FvNuby-3GfJvr676MgSl4PJCn?usp=sharing)
Extract the zip files to ``repair/sgmse/datasets``

Evaluation datasets, along with the obtained results are available [here](https://drive.google.com/drive/folders/1Uhfy7u3NBZeP_TQcs-mvUzU14MXM1JPG?usp=sharing)

**SGMSE Pretrained Models**

Pretrained models may be downloaded [here](https://drive.google.com/drive/folders/15jORVCDG76O6MF3FoeuvYwFNNO7A7Ef-?usp=sharing)
Extract the zip files to ``repair/sgmse/models``