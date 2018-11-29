import numpy as np
from collections import namedtuple

import agents.utils as utils
import agents.basicTransmission as basicTransmission
from settings import settings
import keyboard


class Drive():
    def __init__(self, **kwargs):
        # self.speed_limits = speed_limits
        # self.track_divison = track_divison = np.linspace(
        #     0.,
        #     settings['track_length'],
        #     len(self.speed_limits) + 1
        # )
        # self.is_starting = True
        self.transmission = basicTransmission.Transmssion()
        self.keys = {
            'w': False,
            's': False,
            'a': False,
            'd': False,
        }

    def drive(self, state, **kwargs):
        if self.is_starting:
            if state['distFromStart'] < 20.:
                self.is_starting = False

        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        goalSpeed = self.get_goal_speed(state['distFromStart'], **kwargs)
        if abs(state['trackPos']) > 1:
            goalSpeed = 20

        if state['speedX'] > goalSpeed:
            if state['speedX'] > 5. + goalSpeed:
                response['brake'] = 1
            response['accel'] = 0
        else:
            response['accel'] = 1

        if abs(state['trackPos']) < 0.2:
            self.precisionMode(state, response)

        else:
            targetAngle = state['trackPos'] * 90
            # turningForce = abs(state['angle'] - targetAngle) * (1 / 45) * 3
            if state['angle'] < targetAngle:
                response['steer'] = -settings['hard_turn']
            else:
                response['steer'] = settings['hard_turn']

        return response

    def get_goal_speed(self, dist_from_start, **kwargs):
        if self.is_starting:
            return 300.

        for i, intv in enumerate(zip(self.track_divison, self.track_divison[1:])):
            if intv[0] <= dist_from_start < intv[1]:
                return self.speed_limits[i]
        return self.speed_limits[-1]

    def precisionMode(self, state, response):
        turningForce = abs(state['angle']) * (1 / 45)
        if state['angle'] < 0:
            response['steer'] = -turningForce
        else:
            response['steer'] = turningForce
