# Repair

## Training

To train the model, run

```bash
python train.py --base_dir <dataset> --devices 1 --nolog --batch_size 8 --max_epochs 50
```

Replace ``<dataset>`` with the dataset path, which should be located in the ``datasets`` directory.

*Note: training was carried out on Google Colab. Therefore, this code is not guaranteed to work elsewhere*

## Evaluation and Inference

For inference, run

```bash
python enhancement.py --test_dir <input> --enhanced_dir <output> --ckpt <model>
```

Where ``input`` should be replaced with a directory containing file/s to be enhanced, and ``output`` should be replaced with an output directory where the enhanced files will be placed. ``model`` should be replaced with the relative path to the ``.ckpt`` model file.

To evaluate using SI-SDR, SI-SIR, SI-SAR and SI-SNR, run

```bash
python cust_metrics.py --test_dir <input> --enhanced_dir <output>
```

where ``input`` and ``output`` correspond to the same folders as before.