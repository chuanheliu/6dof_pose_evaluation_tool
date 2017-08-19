import matplotlib.pyplot as plt
import numpy as np
import obj_pose_eval.misc
import obj_pose_eval.visibility as v
from obj_pose_eval import inout, renderer, transform
import math


def avg(list):
    '''
    get the average of a list,
    which can calculate the average distance of all distance in a list
    :param list: a list
    :return: the average of a list
    '''
    sum = 0
    num = 0
    for d in list:
        sum = sum + d
        num = num + 1
    avg = (float)(sum / num)#sum and num are both interager

    return avg

def dataVisualization(figure):
    '''
    generate the graph
    :param figure: the figure that will show
    :return:
    '''
    plt.figure()
    plt.plot(figure, c='r', lw='3')
    plt.xlabel('pixels ID')
    plt.ylabel('the distance')
    plt.tick_params(labelsize=15)
    plt.tight_layout()
    plt.show()

def diff(pose_id,pose_gt, poses, model, depth_test, delta, tau, K):
    '''
    show the difference between ground truth and estimated pose for all points
    :param pose_id: the degree
    :param pose_gt: the ground truth pose
    :param poses: the estmite pose
    :param model: the model of object
    :param depth_test: depth image for test
    :param delta: tolerance for visibility mask
    :param tau:Misalignment tolerance
    :param K: camera parameter
    :return:
    '''
    pose = poses[pose_id]

    c = calcost(pose, pose_gt, model, depth_test, delta, tau, K)

    dataVisualization(c)

def standard_dev(pose_id,pose_gt, poses, model, depth_test, delta, tau, K):

    pose = poses[pose_id]

    c = calcost(pose, pose_gt, model, depth_test, delta, tau, K)

    standard_dev_c = (c-np.mean(c))**2
    # for i in range(0,len(c)):
    #
    # standard_dev_c.append(math.pow((c[i]-avg(c)),2))
    # print 3
    dataVisualization(standard_dev_c)

def calcost(estmitendPose, groundTruthPose, model, depthImage, delta, tau, K):

    im_size = (depthImage.shape[1], depthImage.shape[0])

    # Render depth images of the model in the estimated and the ground truth pose
    depth_est = renderer.render(model, im_size, K, estmitendPose['R'], estmitendPose['t'],
                                clip_near=100, clip_far=10000, mode='depth')

    depth_gt = renderer.render(model, im_size, K, groundTruthPose['R'], groundTruthPose['t'],
                               clip_near=100, clip_far=10000, mode='depth')

    # Convert depth images to distance images
    dist_test = obj_pose_eval.misc.depth_im_to_dist_im(depthImage, K)
    dist_gt = obj_pose_eval.misc.depth_im_to_dist_im(depth_gt, K)

    dist_est = obj_pose_eval.misc.depth_im_to_dist_im(depth_est, K)

    # Visibility mask of the model in the ground truth pose
    visib_gt = v.estimate_visib_mask_gt(dist_test, dist_gt, delta)

    # Visibility mask of the model in the estimated pose
    visib_est = v.estimate_visib_mask_est(dist_test, dist_est, visib_gt, delta)

    # Intersection and union of the visibility masks
    visib_inter = np.logical_and(visib_gt, visib_est)

    # Pixel-wise matching cost
    costs = np.abs(dist_gt[visib_inter] - dist_est[visib_inter])

    costs *= (1.0 / tau)
    costs[costs > 1.0] = 1.0

    return costs

def show(type, degree):

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

    if type == 'average':
        diff(int(degree),pose_gt, poses, model, depth_test, 3, 30, K)
    elif type == 'standard_deviation':
        standard_dev(int(degree),pose_gt, poses, model, depth_test, 3, 30, K)

