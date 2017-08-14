# Author: Tomas Hodan (hodantom@cmp.felk.cvut.cz)
# Center for Machine Perception, Czech Technical University in Prague

import math

import numpy as np
from scipy import spatial

from obj_pose_eval import misc
from obj_pose_eval import renderer
from obj_pose_eval import visibility as v
from tool import cetain as c


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
def dist(p1,p2):
    '''
    get the distance of two 3D points
    :param p1: the coordiante of point1 which is a 3D point including x,y,z
    :param p2: the coordiante of point1 which is a 3D point including x,y,z
    :return: the distance of p1 and p2
    '''
    assert len(p1) == 3 & len(p2) == 3,'not a point'
    temp = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
    d = math.sqrt(temp)
    return d
def groundTruthMask(depth, model, groundTruthP, K, maskT):
    '''
    get the visibility mask of the ground truth pose
    :param depth: the depth image of the test image
    :param model: the object model given by a dictionary where 'pts'
    :param groundTruthP: the ground truth pose
    :param K: from the camera
    :param maskT: the tolerate that can influence the result.
    :return: visiable mask of ground truth
    '''

    im_size = (depth.shape[1], depth.shape[0])

    # Render depth images of the model in the ground truth pose

    groundTruthDepth = renderer.render(model, im_size, K, groundTruthP['R'], groundTruthP['t'], mode='depth')

    # Convert depth images to distance images
    distance = misc.depth_im_to_dist_im(depth, K)
    groundTruthDistance = misc.depth_im_to_dist_im(groundTruthDepth, K)

    # Get the mask of ground truth.
    mask = v.estimate_visib_mask_gt(distance, groundTruthDistance, maskT)

    return mask

def estmatedMask(depth, model,groundTruthP, estimatedP, K, maskT):

    '''
    get the visibility mask of the estimate pose
    :param depth: the depth image of ground truth
    :param model: the object model given by a dictionary where 'pts'
    :param groundTruthP: the ground truth pose
    :param estimatedP: the estimate pose
    :param K: from the camera
    :param maskT: the tolerate that allow for mask calculate.
    :return: visiable mask of ground truth
    '''

    im_size = (depth.shape[1], depth.shape[0])

    # Render depth images of the model in the estimated and the ground truth pose
    estimatedDepth = renderer.render(model, im_size, K, estimatedP['R'], estimatedP['t'], mode='depth')

    # Convert depth images to distance images
    distance = misc.depth_im_to_dist_im(depth, K)
    estimatedDistance = misc.depth_im_to_dist_im(estimatedDepth, K)

    # Visibility mask of the model in the estimated pose
    mask = v.estimate_visib_mask_est(distance,
                                     estimatedDistance,
                                     groundTruthMask(depth, model, groundTruthP, K, maskT),
                                     maskT)
    return mask

def ztest(pose_est, pose_gt, model, depth_test, delta, K):
    """
    Visible Surface Discrepancy.

    :param pose_est: Estimated pose given by a dictionary:
    {'R': 3x3 rotation matrix, 't': 3x1 translation vector}.
    :param pose_gt: The ground truth pose given by a dictionary (as pose_est).
    :param model: Object model given by a dictionary where item 'pts'
    is nx3 ndarray with 3D model points.
    :param depth_test: Depth image of the test scene.
    :param delta: Tolerance used for estimation of the visibility masks.
    :param tau: Misalignment tolerance.
    :return: Error of pose_est w.r.t. pose_gt.
    """

    im_size = (depth_test.shape[1], depth_test.shape[0])

    # Render depth images of the model in the estimated and the ground truth pose
    depth_est = renderer.render(model, im_size, K, pose_est['R'], pose_est['t'],
                                clip_near=100, clip_far=10000, mode='depth')

    depth_gt = renderer.render(model, im_size, K, pose_gt['R'], pose_gt['t'],
                               clip_near=100, clip_far=10000, mode='depth')

    # Convert depth images to distance images
    dist_test = misc.depth_im_to_dist_im(depth_test, K)
    dist_gt = misc.depth_im_to_dist_im(depth_gt, K)

    dist_est = misc.depth_im_to_dist_im(depth_est, K)


    # Visibility mask of the model in the ground truth pose
    gt = groundTruthMask(depth_test, model, pose_gt, K, delta)

    # Visibility mask of the model in the estimated pose
    est = estmatedMask(depth_test, model,pose_gt, pose_est, K, delta)

    # Pixel-wise matching cost
    sampleEST = dist_est[est]
    sampleGT = dist_gt[gt]

    avgEST = (float)(sampleEST.mean())
    avgGT = (float)(sampleGT.mean())
    standardDeviationEST, standardDeviationGT = 0.0, 0.0
    for i in range(0, len(sampleEST)):
        standardDeviationEST += math.pow((sampleEST[i] - avgEST), 2)
    for i in range(0, len(sampleGT)):
        standardDeviationGT += math.pow((sampleGT[i] - avgGT), 2)

    z = (avgEST - avgGT) / math.sqrt((standardDeviationEST/len(sampleEST)) + (standardDeviationGT)/len(sampleGT))

    return z

def rate(model, groundTruthP, estimatedP, mint, maxt):

    count1 = len(c.getEstUncetain(model, groundTruthP, estimatedP, maxt))
    count2 = len(c.getEstCetain(model, groundTruthP, estimatedP, mint))
    e = 0.0
    if count2 != 0:
        e = count1/count2
    return e

def add(estmitedP, groundTrouthP, model):

    #get the points of the ground trouth.
    groundTrouthPoints = misc.transform_pts_Rt(model['pts'], groundTrouthP['R'], groundTrouthP['t'])

    #get the points of the estimated location.
    estmitedPoints = misc.transform_pts_Rt(model['pts'], estmitedP['R'], estmitedP['t'])

    #calculate the distance for the relative points.
    dists = np.linalg.norm(estmitedPoints - groundTrouthPoints, axis=1)

    #get the average of distance.
    eADD = avg(dists)


    #return the average distance.
    return eADD

def adi(estmitedP, groundTrouthP, model):

    # get the points of the ground trouth.
    groundTrouthPoints = misc.transform_pts_Rt(model['pts'], groundTrouthP['R'], groundTrouthP['t'])

    # get the points of the estimated location.
    estmitedPoints = misc.transform_pts_Rt(model['pts'], estmitedP['R'], estmitedP['t'])

    # Calculate distances to the nearest neighbors from pts_gt to pts_est
    tree = spatial.cKDTree(estmitedPoints)
    minDis, ii = tree.query(groundTrouthPoints, k=1)

    eADI = avg(minDis)

    return eADI