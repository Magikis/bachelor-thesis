from __future__ import print_function
from snakeoil import Client
import sys
import json

responseAttr = ['accel',
                'brake',
                'clutch',
                'gear',
                'meta',
                'focus',
                'stear']

it = 0


def drive(state):
    response = getDeafaultResponse(state)
    print('anglel: ', state['angle'], 'trackPos: ', state['trackPos'])

    goalSpeed = 150
    if abs(state['trackPos']) > 1:
        goalSpeed = 20

    if state['speedX'] > goalSpeed:
        response['accel'] = 0
    else:
        response['accel'] = 1

    targetAngle = 0
    if state['trackPos'] > 0.01:
        targetAngle = 0.1
    if state['trackPos'] < -0.01:
        targetAngle = -0.1

    if abs(state['angle'] - targetAngle) > 0.025:
        turningForce = 0.4
        if state['angle'] < targetAngle:
            response['steer'] = -turningForce
        else:
            response['steer'] = turningForce

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
    if state['speedX'] > 140:
        response['gear'] = 5
    if state['speedX'] > 170:
        response['gear'] = 6
    return response


def drivingLoop(drivingFunc):
    C = Client()
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        data = C.S.d
        response = drivingFunc(data)
        for k in C.R.d:
            C.R.d[k] = response[k]
        print(C.R.d)
        sys.stdout.flush()
        C.respond_to_server()
    C.shutdown()


# ================ MAIN ================
if __name__ == "__main__":
    drivingLoop(drive)
