from snakeoil import Client
import json

responseAttr = ['accel',
                'brake',
                'clutch',
                'gear',
                'meta',
                'focus',
                'stear']

x = 100


def drive(state):
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

    global x
    if x <= 250:
        response['accel'] = 1
        response['break'] = 0
    else:
        response['accel'] = 0
        response['brake'] = 1

    x = (x + 1) % 500
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
        C.respond_to_server()
    C.shutdown()


# ================ MAIN ================
if __name__ == "__main__":
    drivingLoop(drive)
