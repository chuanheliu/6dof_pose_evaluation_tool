#!/usr/bin/env python

# Author: Tomas Hodan (hodantom@cmp.felk.cvut.cz)
# Center for Machine Perception, Czech Technical University in Prague

# Comparison of several pose error functions on a synthetic example
# of a rotating cup.

import matplotlib.pyplot as plt
import numpy as np
import error_function as error
import math

from obj_pose_eval import inout, pose_error, renderer, transform

def show(type, t1, t2):
    # Load object model
    model_path = 'cup.ply'
    model = inout.load_ply(model_path)

    # Camera parameters
    K = np.eye(3)
    K[0, 0] = 500.0  # fx
    K[1, 1] = 500.0  # fy
    K[0, 2] = 250.0  # cx
    K[1, 2] = 250.0  # cy
    im_size = (500, 500)

    # Calculate the poses of the rotating cup
    poses = []
    alpha_range = np.linspace(0, 360, 361)
    for alpha in alpha_range:
        def d2r(d): return np.pi * float(d) / 180.0  # Degrees to radians

        R = transform.rotation_matrix(d2r(alpha), [0, 1, 0])[:3, :3]  # Rotation around Y
        R = transform.rotation_matrix(d2r(30), [1, 0, 0])[:3, :3].dot(R)  # Rotation around X
        t = np.array([0.0, 0.0, 180]).reshape((3, 1))

        # Flip Y axis (model coordinate system -> OpenCV coordinate system)
        R = transform.rotation_matrix(np.pi, [1, 0, 0])[:3, :3].dot(R)
        poses.append({'R': R, 't': t})

    # Set and render the ground truth pose
    gt_id = 90  # ID of the ground truth pose
    pose_gt = poses[gt_id]
    pose_gt_indis_set_ids = range(55, 126)  # IDs of poses indistinguishable from the GT pose
    pose_gt_indis_set = [poses[i] for i in pose_gt_indis_set_ids]
    depth_gt = renderer.render(model, im_size, K, pose_gt['R'], pose_gt['t'], 100, 2000, mode='depth')

    # Synthesize the test depth image
    depth_test = np.array(depth_gt)
    depth_test[depth_test == 0] = 1000

    # Available errors: 'vsd', 'acpd', 'mcpd', 'add', 'adi', 'te', 're', 'cou'
    # Errors to be calculated:
    errs_active = [type]

    vsda, ztesta = [], []
    # Calculate the pose errors
    errs = {err: [] for err in errs_active}
    for pose_id, pose in enumerate(poses):
        print 'Processing pose:', pose_id

        # Determine the set of poses that are indistinguishable from the current pose
        if 55 <= pose_id <= 125:
            pose_indis_set = pose_gt_indis_set
        else:
            pose_indis_set = [pose]

        if 'cpr' in errs_active:
            mint = t1
            maxt = t2
            errs['cpr'].append(error.cpr(model, pose_gt, pose, mint, maxt))

        if 'zdd' in errs_active:
            delta = 3
            errs['zdd'].append(error.zdd(pose, pose_gt, model, depth_test, delta, K))


        if 'wivm' in errs_active:
            delta = t1
            errs['wivm'].append(error.wivm(pose, pose_gt, model, depth_test, delta, K, t1, t2))


    for err_name in errs_active:
        plt.figure()
        plt.plot(errs[err_name], c='r', lw='3')
        plt.xlabel('Pose ID')
        plt.ylabel(err_name)
        plt.tick_params(labelsize=16)
        plt.tight_layout()
    plt.show()
