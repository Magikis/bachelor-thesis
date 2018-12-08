import numpy as np
from collections import namedtuple

import agents.utils as utils
import agents.basicTransmission as basicTransmission
from settings import settings


class HumanDrive():
    def __init__(self, **kwargs):
        self.transmission = basicTransmission.Transmssion()
        self.HumanInput = utils.HumanInput()
        self.hs_counter = {
            'left': 0,
            'right': 0
        }

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        human_state = self.HumanInput.get_state()
        for k in self.hs_counter:
            if human_state[k]:
                self.hs_counter[k] += 1
            else:
                self.hs_counter[k] = max(self.hs_counter[k] - 2, 0)
        if human_state['accel']:
            response['accel'] = 1

        if human_state['brake']:
            response['brake'] = 1
            response['accel'] = 0

        if human_state['left']:
            response['steer'] = np.clip(
                self.hs_counter['left'] * 0.015, 0.0, 1.0)
        if human_state['right']:
            response['steer'] = - \
                np.clip(self.hs_counter['right'] * 0.015, 0.0, 1.0)
        return response
