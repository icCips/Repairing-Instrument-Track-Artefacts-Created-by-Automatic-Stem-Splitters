# Dataset Construction

To generate the CMS-MixR-U dataset, run ``build_dataset.py``. The dataset directory may be changed by changing the `dataset_path` variable. The ``build_dataset.py`` script takes very long to execute. As such, consider running one function at a time.


# MixR

To modify the MixR effects matrix, modify ``MixR/data/fx.csv``

To modify the MixR effects distributions, modify the values passed to the `generate_truncated_normal` functions in ``MixR/pedalboard_util.py``.