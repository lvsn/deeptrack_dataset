import os
import json

from utils.frame import FrameNumpy, Frame, FrameHdf5
from utils.camera import Camera
from utils.transform import Transform


class Loader:
    def __init__(self, root):
        self.root = root
        self.data_pose = []
        self.load(self.root)

    def load(self, path):
        """
        Load a viewpoints.json to dataset's structure
        Todo: datastructure should be more similar to json structure...
        :return: return false if the dataset is empty.
        """
        # Load viewpoints file and camera file
        with open(os.path.join(path, "viewpoints.json")) as data_file:
            data = json.load(data_file)
        self.camera = Camera.load_from_json(path)
        self.metadata = data["metaData"]
        self.set_save_type(self.metadata["save_type"])
        count = 0
        # todo change json datastructure... it is not relevant now and makes the code unclean
        while True:
            try:
                id = str(count)
                pose = Transform.from_parameters(*[float(data[id]["vector"][str(x)]) for x in range(6)])
                self.add_pose(None, None, pose)
                count += 1
            except KeyError:
                break

    def from_index(self, index):
        raise RuntimeError("Not Implemented")

    def load_image(self, index):
        frame, pose = self.data_pose[index]
        rgb, depth = frame.get_rgb_depth(self.root)
        return rgb, depth, pose

    def size(self):
        return len(self.data_pose)

    def add_pose(self, rgb, depth, pose):
        index = self.size()
        frame = self.frame_class(rgb, depth, str(index))
        self.data_pose.append([frame, pose])
        return index

    def set_save_type(self, frame_class):
        if frame_class == "numpy":
            self.frame_class = FrameNumpy
        elif frame_class == "hdf5":
            self.frame_class = FrameHdf5
        else:
            self.frame_class = Frame
