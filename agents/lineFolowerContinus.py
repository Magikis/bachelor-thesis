from collections import namedtuple

counter = 0


def smartPrint(*args):
    if counter == 0:
        print(args)


def drive(state):
    response = getDeafaultResponse(state)
    state = namedtuple('State', state.keys())(**state)

    goalSpeed = 150
    if abs(state.trackPos) > 1:
        goalSpeed = 20

    if state.speedX > goalSpeed:
        response['accel'] = 0
    else:
        response['accel'] = 1

    targetAngle = state.trackPos * 45

    turningForce = abs(state.angle - targetAngle) * (1 / 45)
    if state.angle < targetAngle:
        response['steer'] = -min(turningForce, 0.6)
    else:
        response['steer'] = min(turningForce, 0.6)

    smartPrint('ANGLE: ', targetAngle)
    smartPrint('TRACK: ', turningForce)
    global counter
    counter = (counter + 1) % 100
    return response


def getDeafaultResponse(state):
    response = {
        'gear': 1,
        'clutch': 0,
        'focus': [-90, -45, 0, 45, 90],
        'accel': 0,
        'brake': 0,
        'steer': 0,
        'meta': 0
    }
    if state['speedX'] > 50:
        response['gear'] = 2
    if state['speedX'] > 80:
        response['gear'] = 3
    if state['speedX'] > 110:
        response['gear'] = 4
    if state['speedX'] > 145:
        response['gear'] = 5
    if state['speedX'] > 170:
        response['gear'] = 6
    return response
