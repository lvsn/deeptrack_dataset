import argparse

from utils.loader import Loader
from utils.modelrenderer import ModelRenderer

import cv2
import os
import numpy as np


def image_blend(foreground, background):
    """
    Uses pixel 0 to compute blending mask
    :param foreground:
    :param background:
    :return:
    """
    if len(foreground.shape) == 2:
        mask = foreground[:, :] == 0
    else:
        mask = foreground[:, :, 0] == 0
        mask = mask[:, :, np.newaxis]
    return background * mask + foreground


if __name__ == '__main__':
    """
    Check if all detections in sequence are as expected
    """

    parser = argparse.ArgumentParser(description='Train DeepTrack')
    parser.add_argument('-o', '--output', help="Output path", action="store", default="data")
    parser.add_argument('--skip_models', help="Skip 3D model downloads", action="store_true")
    parser.add_argument('--skip_raw', help="Skip Raw training data", action="store_true")
    parser.add_argument('--skip_sequences', help="Skip Sequence data", action="store_true")
    parser.add_argument('--skip_occlusion', help="Skip Occlusion data", action="store_true")

    arguments = parser.parse_args()
    skip_models = arguments.skip_models
    skip_raw = arguments.skip_raw
    skip_sequences = arguments.skip_sequences
    skip_occlusion = arguments.skip_occlusion
    output_path = arguments.output
    # Populate important data from config file
    SEQUENCE_PATH = "/home/mathieu/source/deeptrack_dataset/data/sequences/dragon"
    MODEL_PATH = "/home/mathieu/source/deeptrack_dataset/data/3dmodels/dragon"
    MODEL_GEO_PATH = os.path.join(MODEL_PATH, "geometry.ply")
    MODEL_AO_PATH = os.path.join(MODEL_PATH, "ao.ply")
    SHADER_PATH = "shaders"
    fps = 30
    dataset = Loader(SEQUENCE_PATH)

    vpRender = ModelRenderer(MODEL_GEO_PATH, SHADER_PATH, dataset.camera, [(dataset.camera.width, dataset.camera.height)])
    vpRender.load_ambiant_occlusion_map(MODEL_AO_PATH)
    print("Sequence length: {}".format(len(dataset.data_pose)))
    for i, (frame, pose) in enumerate(dataset.data_pose):
        rgb, depth = frame.get_rgb_depth(SEQUENCE_PATH)
        rgb_render, depth_render = vpRender.render_image(pose)
        blend = image_blend(rgb_render[:, :, ::-1], rgb)
        cv2.imshow("debug", blend[:, :, ::-1])
        cv2.waitKey(int((1/fps)*1000))



