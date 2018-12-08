track = (
    # 'forza'
    # 'short',
    'track_2'
)

settings = {
    'track_length': {
        'forza': 5784.02,
        'short': 1621.73,
        'track_2': 3185.83,
    }[track],
    'speed_limits': {
        'forza': [300.0, 199.375, 209.921875, 93.3203125, 300.0, 107.3828125, 104.453125, 300.0],
        'short': [159.53125, 154.84375, 160.703125, 153.671875],
        'track_2': [300.0, 132.578125, 123.203125, 107.3828125, 300.0, 199.375, 93.90625, 300.0],
    }[track],
    'hard_turn': 0.35

}


def gen_log_object(state, response):
    return {
        'angle': state['angle'],
        'curLapTime': state['curLapTime'],
        'damage': state['damage'],
        'distFromStart': state['distFromStart'],
        'distRaced': state['distRaced'],
        'focus': state['focus'],
        'fuel': state['fuel'],
        'gear': state['gear'],
        'lastLapTime': state['lastLapTime'],
        'opponents': state['opponents'],
        'pitch': state['pitch'],
        'racePos': state['racePos'],
        'roll': state['roll'],
        'rpm': state['rpm'],
        'speedGlobalX': state['speedGlobalX'],
        'speedGlobalY': state['speedGlobalY'],
        'speedX': state['speedX'],
        'speedY': state['speedY'],
        'speedZ': state['speedZ'],
        'track': state['track'],
        'trackPos': state['trackPos'],
        'wheelSpinVel': state['wheelSpinVel'],
        'x': state['x'],
        'y': state['y'],
        'yaw': state['yaw'],
        'z': state['z'],
        'accel': response['accel'],
        'brake': response['brake'],
        'clutch': response['clutch'],
        'focus': response['focus'],
        'gear': response['gear'],
        'meta': response['meta'],
        'steer': response['steer'],
    }
