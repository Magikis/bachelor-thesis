from collections import namedtuple
from agents.lineForowerDiscreate import getDeafaultResponse


def smartPrint(step, howOften, *args):
    if step % howOften == 0:
        print(args)


def precisionMode(state, response):
    turningForce = abs(state.angle) * (1 / 45)
    if state.angle < 0:
        response['steer'] = -turningForce
    else:
        response['steer'] = turningForce


def drive(state, step):
    response = getDeafaultResponse(state)
    state = namedtuple('State', state.keys())(**state)

    goalSpeed = 90
    if abs(state.trackPos) > 1:
        goalSpeed = 20

    if state.speedX > goalSpeed:
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
