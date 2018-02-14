# deeptrack_dataset
Python3 code to load and evaluate 6DOF tracking dataset from [Deep 6 DoF Tracking](http://vision.gel.ulaval.ca/~jflalonde/projects/deepTracking/index.html)

## Dependencies
- PIL
- vispy
- pyopengl
- opencv

## Download datasets

Script to download/extract the full dataset from the servers. Contains option to skip downloads and to set output paths.
The default path is ./data.
```bash
    python download.py -o ./data
```

## Show sequence

Script to visualize the dataset (sequence only). Serve as an example on how the dataset is loaded in memory. The option
--save will save the ground truth data in the format used for evaluation.
```bash
    python show_sequence --dataset ./data --object dragon
```

To load result instead of ground truth, use --load option:
```bash
    python show_sequence --dataset ./data --load ./sequence_dragon.npy
```

## TODO
- Add support for csv file
- evaluation code