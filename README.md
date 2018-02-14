# deeptrack_dataset
Python3 code to load and evaluate 6DOF tracking dataset from [Deep 6 DoF Tracking](http://vision.gel.ulaval.ca/~jflalonde/projects/deepTracking/index.html)

## Dependencies
- PIL
- vispy
- pyopengl
- opencv

## Download datasets

Script to download/extract the full dataset from the servers. Contains option to skip downloads and to set output paths.
The default path is ./data
```bash
    python download.py
```

## Show sequence

Script to visualize the dataset. Serve as an example on how the dataset is loaded in memory.