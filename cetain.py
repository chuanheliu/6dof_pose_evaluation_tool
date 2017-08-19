import math
import obj_pose_eval.misc
import numpy as np

def dist(p1, p2):
    '''
    get the distance of two 3D points
    :param p1: the coordiante of point1 which is a 3D point including x,y,z
    :param p2: the coordiante of point1 which is a 3D point including x,y,z
    :return: the distance of p1 and p2
    '''
    assert len(p1) == 3 & len(p2) == 3, 'not a point'
    temp = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
    d = math.sqrt(temp)
    return d


def getCertain(model, groundTruthP, estimatedP, tolerate):
    """
    get the list for points True for right False for wrong
    :param model: Object model given by a dictionary where item 'pts' is nx3 ndarray with 3D model points.
    :param estimatePose: Estimated pose given by a dictionary:
            {'R': 3x3 rotation matrix, 't': 3x1 translation vector}.
    :param groundTruthPose: The ground truth pose given by a dictionary
    :param tolerate: the right tolerate
    :return: a list
    """
    # get the points of the ground trouth.
    groundTruthPoints = obj_pose_eval.misc.transform_pts_Rt(model['pts'], groundTruthP['R'], groundTruthP['t'])

    # get the points of the estimated location.
    estmitedPoints = obj_pose_eval.misc.transform_pts_Rt(model['pts'], estimatedP['R'], estimatedP['t'])

    assert (len(groundTruthPoints) == len(estmitedPoints))

    cetain = []
    i = 0
    for i in range(0, len(groundTruthPoints)):

        d = dist(groundTruthPoints[i],estmitedPoints[i])
        if d < tolerate:
            cetain.append(True)
        if d >= tolerate:
            cetain.append(False)

    return cetain


def getGTCetain(model, groundTruthP, estimatedP, tolerate):
    """
    get the ground truth points that is considered right
    :param model: Object model given by a dictionary where item 'pts' is nx3 ndarray with 3D model points.
    :param estimatePose: Estimated pose given by a dictionary:
                {'R': 3x3 rotation matrix, 't': 3x1 translation vector}.
    :param groundTruthPose: The ground truth pose given by a dictionary
    :param tolerate: the right tolerate
    :return: an array
    """
    cetain = getCertain(model, groundTruthP, estimatedP, tolerate)

    # get the points of the ground trouth.
    groundTruthPoints = obj_pose_eval.misc.transform_pts_Rt(model['pts'], groundTruthP['R'], groundTruthP['t'])

    GTCertain = []
    for i in range(0, len(groundTruthPoints)):
        if cetain[i] == True:
            GTCertain.append(groundTruthPoints[i])

    return np.array(GTCertain)

def getGTUncertain(model, groundTruthP, estimatedP, tolerate):
    """
    get the ground truth points that is considered wrong
    :param model: Object model given by a dictionary where item 'pts' is nx3 ndarray with 3D model points.
    :param estimatePose: Estimated pose given by a dictionary:
            {'R': 3x3 rotation matrix, 't': 3x1 translation vector}.
    :param groundTruthPose: The ground truth pose given by a dictionary
    :param tolerate: the wrong tolerate
    :return: an array
    """
    cetain = getCertain(model, groundTruthP, estimatedP, tolerate)

    # get the points of the ground trouth.
    groundTruthPoints = obj_pose_eval.misc.transform_pts_Rt(model['pts'], groundTruthP['R'], groundTruthP['t'])

    GTUncertain = []
    for i in range(0, len(groundTruthPoints)):
        if cetain[i] == False:
            GTUncertain.append(groundTruthPoints[i])

    return np.array(GTUncertain)

def getEstCetain(model, groundTruthP, estimatedP, tolerate):
    """
    get the estimated points that is considered right
    :param model: Object model given by a dictionary where item 'pts' is nx3 ndarray with 3D model points.
    :param estimatePose: Estimated pose given by a dictionary:
                {'R': 3x3 rotation matrix, 't': 3x1 translation vector}.
    :param groundTruthPose: The ground truth pose given by a dictionary
    :param tolerate: the right tolerate
    :return: an array
    """
    cetain = getCertain(model, groundTruthP, estimatedP, tolerate)

    # get the points of the estimated location.
    estmitedPoints = obj_pose_eval.misc.transform_pts_Rt(model['pts'], estimatedP['R'], estimatedP['t'])

    EstCertain = []

    for i in range(0, len(estmitedPoints)):
        if cetain[i] == True:
            EstCertain.append(estmitedPoints[i])

    return np.array(EstCertain)


def getEstUncetain(model, groundTruthP, estimatedP, tolerate):
    """
     get the estimated points that is considered wrong
     :param model: Object model given by a dictionary where item 'pts' is nx3 ndarray with 3D model points.
     :param estimatePose: Estimated pose given by a dictionary:
                 {'R': 3x3 rotation matrix, 't': 3x1 translation vector}.
     :param groundTruthPose: The ground truth pose given by a dictionary
     :param tolerate: the right tolerate
     :return: an array
     """
    cetain = getCertain(model, groundTruthP, estimatedP, tolerate)

    # get the points of the estimated location.
    estmitedPoints = obj_pose_eval.misc.transform_pts_Rt(model['pts'], estimatedP['R'], estimatedP['t'])

    EstUncertain = []

    for i in range(0, len(estmitedPoints)):
        if cetain[i] == False:
            EstUncertain.append(estmitedPoints[i])

    return np.array(EstUncertain)