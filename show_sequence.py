import argparse

from utils.loader import Loader
from utils.modelrenderer import ModelRenderer

import cv2
import os
import numpy as np

from utils.transform import Transform


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

    parser = argparse.ArgumentParser(description='Show sequence')
    parser.add_argument('-o', '--object', help="Object name : dragon|skull|clock|turtle", action="store", default="dragon")
    parser.add_argument('-d', '--dataset', help="Dataset path", action="store", default="./data")
    parser.add_argument('-s', '--save', help="Save results", action="store", default="")
    parser.add_argument('-l', '--load', help="Load results", action="store", default="")

    parser.add_argument('--shader', help="shader path", action="store", default="./shaders")
    parser.add_argument('--fps', help="weight decay", action="store", default=30, type=float)

    arguments = parser.parse_args()
    shader_path = arguments.shader
    model_path = os.path.join(arguments.dataset, "3dmodels", arguments.object)
    sequence_path = os.path.join(arguments.dataset, "sequences", arguments.object)
    save_path = arguments.save
    load_path = arguments.load

    model_geo_path = os.path.join(model_path, "geometry.ply")
    model_ao_path = os.path.join(model_path, "ao.ply")
    fps = 30

    loaded_result = None
    if load_path is not "":
        loaded_result = np.load(load_path)

    dataset = Loader(sequence_path)

    vpRender = ModelRenderer(model_geo_path, shader_path, dataset.camera, [(dataset.camera.width, dataset.camera.height)])
    vpRender.load_ambiant_occlusion_map(model_ao_path)

    gt_parameters = []
    print("Sequence length: {}".format(len(dataset.data_pose)))
    for i, (frame, pose) in enumerate(dataset.data_pose):
        rgb, depth = frame.get_rgb_depth(sequence_path)

        # save data as 6 parameters (tx, ty, tz, rx, ry, rz)
        gt_parameters.append(pose.to_parameters())

        # use load parameters else use dataset ground truth
        if loaded_result is not None:
            loaded_pose = Transform.from_parameters(*loaded_result[i])
            rgb_render, depth_render = vpRender.render_image(loaded_pose)
            blend = image_blend(rgb_render[:, :, ::-1], rgb)
        else:
            rgb_render, depth_render = vpRender.render_image(pose)
            blend = image_blend(rgb_render[:, :, ::-1], rgb)

        cv2.imshow("debug", blend[:, :, ::-1])
        cv2.waitKey(int((1/fps)*1000))

    if save_path is not "":
        np.save(os.path.join(save_path, "sequence_{}.npy".format(arguments.object)), np.array(gt_parameters))



