import numpy as np
from collections import namedtuple

import agents.utils as utils
import agents.basicTransmission as basicTransmission
from settings import settings


def get_goal_speed(dist_from_start, speed_limits=None, **kwargs):
    if speed_limits is None:
        speed_limits = settings['speed_limits']

    track_divison = np.linspace(
        0.,
        settings['track_length'],
        len(speed_limits)
    )

    for i, intv in enumerate(zip(track_divison, track_divison[1:])):
        if intv[0] <= dist_from_start < intv[1]:
            return speed_limits[i]
    return speed_limits[-1]


def precisionMode(state, response):
    turningForce = abs(state.angle) * (1 / 45)
    if state.angle < 0:
        response['steer'] = -turningForce
    else:
        response['steer'] = turningForce


def drive(state, **kwargs):
    response = utils.get_default_response()
    state = namedtuple('State', state.keys())(**state)

    response['gear'] = basicTransmission.get_new_gear(state)
    
    goalSpeed = get_goal_speed(state.distFromStart, **kwargs)
    if abs(state.trackPos) > 1:
        goalSpeed = 20

    if state.speedX > goalSpeed:
        if state.speedX > 5. + goalSpeed:
            response['brake'] = 1
        response['accel'] = 0
    else:
        response['accel'] = 1

    if abs(state.trackPos) < 0.2:
        precisionMode(state, response)

    else:
        targetAngle = state.trackPos * 90
        # turningForce = abs(state.angle - targetAngle) * (1 / 45) * 3
        if state.angle < targetAngle:
            response['steer'] = -0.4
        else:
            response['steer'] = 0.4

    # smartPrint('ANGLE: ', targetAngle)
    # smartPrint('TRACK: ', turningForce)
    # smartPrint(step, 100, state.distFromStart)
    return response
