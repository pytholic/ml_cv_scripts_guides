import sys

sys.path.append("droid_slam")

import argparse
from glob import glob
import os
import time
import pathlib

import gc
import cv2
import lietorch
import numpy as np
import torch
import torch.nn.functional as F
from droid import Droid
from torch.multiprocessing import Process
from tqdm import tqdm
import natsort
from datetime import datetime




def tartan(dataset_name, dataset_path):
        root_dir = pathlib.Path(__file__).parent.resolve()
        # Genertate time for filename
        time  = datetime.now().strftime("%Y_%m_%d_%H_%M")
        # Result path directory
        results_path = os.path.join(root_dir,'results',args.dataset_name,time)

        if not os.path.exists(results_path):
            os.makedirs(results_path)

        scences_subfolders = [f.path for f in os.scandir(dataset_path) if f.is_dir()]

        filenames_save = []
        images_dir = []
        
        for sub in scences_subfolders:
            print("")
            print(sub)

            sub_path = os.path.join(root_dir,sub)
            sub_folders_path = [f.path for f in os.scandir(sub_path) if f.is_dir()]
        

            for scenario in sub_folders_path:

                scenario_dir = [f.path for f in os.scandir(scenario) if f.is_dir()]

                for sc in scenario_dir:
                    print(sc)

                    tmp_path = os.path.join(sc,"image*")
                    imagedir = natsort.natsorted(glob(tmp_path))
                    print(imagedir)
                    for imgdir in imagedir:
                   
                        images_dir.append(imgdir)
                        
                        
                        filename = imgdir.split("/")
                        filename = filename[-4:]
                        filename = ','.join(map(str, filename))
                        filename = filename.replace(",","_")

                        filename = time + "_" + filename
                        filename_path = os.path.join(results_path, filename)

                        filenames_save.append(filename_path)

                        if not os.path.exists(filename_path):
                            os.makedirs(filename_path)
        
        
        return images_dir, filenames_save


def show_image(image):
    image = image.permute(1, 2, 0).cpu().numpy()
    cv2.imshow("image", image / 255.0)
    cv2.waitKey(1)


def image_stream(imagedir, calib, stride):
    """image generator"""

    calib = np.loadtxt(calib, delimiter=" ")
    fx, fy, cx, cy = calib[:4]

    K = np.eye(3)
    K[0, 0] = fx
    K[0, 2] = cx
    K[1, 1] = fy
    K[1, 2] = cy

    image_list = sorted(os.listdir(imagedir))[::stride]

    for t, imfile in enumerate(image_list):
        image = cv2.imread(os.path.join(imagedir, imfile))
        if len(calib) > 4:
            image = cv2.undistort(image, K, calib[4:])

        h0, w0, _ = image.shape
        h1 = int(h0 * np.sqrt((384 * 512) / (h0 * w0)))
        w1 = int(w0 * np.sqrt((384 * 512) / (h0 * w0)))
        image = cv2.resize(image, (w1, h1))
        image = image[: h1 - h1 % 8, : w1 - w1 % 8]
        image = torch.as_tensor(image).permute(2, 0, 1)
        intrinsics = torch.as_tensor([fx, fy, cx, cy])
        intrinsics[0::2] *= w1 / w0
        intrinsics[1::2] *= h1 / h0

        yield t, image[None], intrinsics


def save_reconstruction(droid, reconstruction_path):

    import random
    import string
    from pathlib import Path

    t = droid.video.counter.value
    tstamps = droid.video.tstamp[:t].cpu().numpy()
    images = droid.video.images[:t].cpu().numpy()
    disps = droid.video.disps_up[:t].cpu().numpy()
    poses = droid.video.poses[:t].cpu().numpy()
    intrinsics = droid.video.intrinsics[:t].cpu().numpy()

    Path("reconstructions/{}".format(reconstruction_path)).mkdir(
        parents=True, exist_ok=True
    )
    np.save("{}/tstamps.npy".format(reconstruction_path), tstamps)
    np.save("{}/images.npy".format(reconstruction_path), images)
    np.save("{}/disps.npy".format(reconstruction_path), disps)
    np.save("{}/poses.npy".format(reconstruction_path), poses)
    np.save("{}/intrinsics.npy".format(reconstruction_path), intrinsics)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, default="tartan")
    parser.add_argument("--dataset_path", type=str)
    parser.add_argument("--process_dataset", default=False, type=bool)



    parser.add_argument("--imagedir", type=str, help="path to image directory")
    parser.add_argument("--calib", type=str, help="path to calibration file")
    parser.add_argument("--t0", default=0, type=int, help="starting frame")
    parser.add_argument("--stride", default=3, type=int, help="frame stride")
    parser.add_argument("--weights", default="droid.pth")
    parser.add_argument("--buffer", type=int, default=512)
    parser.add_argument("--image_size", default=[240, 320])
    parser.add_argument("--disable_vis", action="store_true")
    parser.add_argument(
        "--beta",
        type=float,
        default=0.3,
        help="weight for translation / rotation components of flow",
    )
    parser.add_argument(
        "--filter_thresh",
        type=float,
        default=2.4,
        help="how much motion before considering new keyframe",
    )
    parser.add_argument("--warmup", type=int, default=8, help="number of warmup frames")
    parser.add_argument(
        "--keyframe_thresh",
        type=float,
        default=4.0,
        help="threshold to create a new keyframe",
    )
    parser.add_argument(
        "--frontend_thresh",
        type=float,
        default=16.0,
        help="add edges between frames whithin this distance",
    )
    parser.add_argument(
        "--frontend_window", type=int, default=25, help="frontend optimization window"
    )
    parser.add_argument(
        "--frontend_radius",
        type=int,
        default=2,
        help="force edges between frames within radius",
    )
    parser.add_argument(
        "--frontend_nms", type=int, default=1, help="non-maximal supression of edges"
    )

    parser.add_argument("--backend_thresh", type=float, default=22.0)
    parser.add_argument("--backend_radius", type=int, default=2)
    parser.add_argument("--backend_nms", type=int, default=3)
    parser.add_argument("--upsample", action="store_true")
    parser.add_argument("--reconstruction_path", help="path to saved reconstruction")
    args = parser.parse_args()

    process_dataset = args.process_dataset
    dataset_name = args.dataset_name
    dataset_path = args.dataset_path

    ########
    args.stereo = False
    torch.multiprocessing.set_start_method("spawn")

    droid = None

    if process_dataset:

        if dataset_name=='tartan':


            images_dir, filenames_save = tartan(dataset_name, dataset_path)
            
            for i in range(len(images_dir)):
                print("---")
                print(images_dir[i])
                args.imagedir = images_dir[i]
                args.reconstruction_path = filenames_save[i]

                # need high resolution depths
                if args.reconstruction_path is not None:
                    args.upsample = True

                tstamps = []
                for (t, image, intrinsics) in tqdm(
                    image_stream(args.imagedir, args.calib, args.stride)
                ):
                    if t < args.t0:
                        continue

                    if droid is None:
                        args.image_size = [image.shape[2], image.shape[3]]

                        droid = Droid(args)

                    droid.track(t, image, intrinsics=intrinsics)

                if args.reconstruction_path is not None:
                    save_reconstruction(droid, args.reconstruction_path)

                traj_est = droid.terminate(image_stream(args.imagedir, args.calib, args.stride))

                droid.visualizer.terminate()
                gc.collect()
                torch.cuda.empty_cache()
                droid = None



    else:

        
        droid = None
        # need high resolution depths
        if args.reconstruction_path is not None:
            args.upsample = True

        tstamps = []
        for (t, image, intrinsics) in tqdm(
            image_stream(args.imagedir, args.calib, args.stride)
        ):
            if t < args.t0:
                continue

            if droid is None:
                args.image_size = [image.shape[2], image.shape[3]]
                # Shape define in image_stream function -> 400 * 550

                droid = Droid(args)

            droid.track(t, image, intrinsics=intrinsics)

        if args.reconstruction_path is not None:
            save_reconstruction(droid, args.reconstruction_path)

        traj_est = droid.terminate(image_stream(args.imagedir, args.calib, args.stride))

        droid.visualizer.terminate()
        torch.cuda.empty_cache()
