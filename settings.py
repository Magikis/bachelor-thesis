track = (
    # 'forza'
    # 'e_track_5'
    # 'cg_track_2'
    # 'cg_track_3'
    'const'
)


def get_track():
    return track


settings = {
    'track_length': {
        'forza': 5784.02,
        'cg_track_2': 3185.83,
        'cg_track_3': 2843.1,
        'e_track_5': 1621.73,
        'const': 2000
    }[track],
    'speed_limits': {
        'forza': [300.0, 207.578125, 212.265625, 88.6328125, 300.0, 92.1484375, 124.375, 300.0],
        'e_track_5': [159.53125, 154.84375, 160.703125, 153.671875],
        'cg_track_2': [300.0, 132.578125, 123.203125, 108.5546875, 300.0, 129.0625, 164.21875, 300.0],
        'cg_track_3': [100.3515625, 103.8671875, 122.03125, 144.8828125, 154.84375, 82.7734375, 136.09375, 300.0],
        'const': [80]
    }[track],
    'hard_turn': 0.35,
    'action_keys': [
        'accel',
        'brake',
        'steer',
    ],
    'state_keys': [
        'speedX',
        'speedY',
        'speedZ',
        'angle',
        'trackPos',
        # 'distFromStart',
        'track',
        'wheelSpinVel'
    ],

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
        # 'focus': response['focus'],
        'gear': response['gear'],
        'meta': response['meta'],
        'steer': response['steer'],
    }
