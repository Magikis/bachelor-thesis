import joblib
import json
import numpy as np
import agents.utils as utils
import agents.basicTransmission as basicTransmission
from agents.line_folower import Drive
from agents.double_model_agent import DoubleModelAgent
from settings import settings


def extract_state(data_sample, state_keys, data_is_array=False):
    if data_is_array:
        return [extract_state(x, state_keys) for x in data_sample]
    state_vector = []
    for key in state_keys:
        if key == 'angle':
            state_vector += [
                np.sin(np.deg2rad(data_sample[key])),
                np.cos(np.deg2rad(data_sample[key]))
            ]
        elif isinstance(data_sample[key], list):
            state_vector += data_sample[key]
        else:
            state_vector.append(data_sample[key])
    return state_vector


class TripleModelAgent(DoubleModelAgent):
    def load(self, path, **kwargs):
        super().load(path)
        self.steer_classifier = joblib.load(f'{path}/steer_classifier')
        self.sl_agent = Drive(**kwargs)

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        state_vector = self.scaler.transform(
            [extract_state(state, self.state_keys)]
        )

        steer_direction = self.steer_classifier.predict(
            state_vector
        )[0]

        steer_magnitude = self.steer_regressor.predict(
            state_vector
        )[0]

        # if steer_direction == 0 and steer_magnitude > 0.05:
        #     print(
        #         'steer_direction', steer_direction, 'steer_magnitude', steer_magnitude
        #     )

        if steer_direction < 0 and steer_magnitude > 0:
            steer_val = 0
        elif steer_direction > 0 and steer_magnitude < 0:
            steer_val = 0
        elif steer_direction == 0:
            steer_val = steer_magnitude / 3
        else:
            steer_val = steer_magnitude

        state_vector = np.hstack((state_vector, [[steer_val]]))

        speed_action_index = self.speed_classifier.predict(
            state_vector
        )[0]

        response = {
            **response,
            'steer': steer_val,
            **self.speed_actions_labels[speed_action_index],
        }

        # self.apply_speed_limit(state, response)
        # self.manage_start_accel(state, response)
        return response

    isStart = True

    def manage_start_accel(self, state, response):
        if self.isStart:
            if state['distFromStart'] > 1 and state['speedX'] < 50:
                response['accel'] = 1
                response['brake'] = 0
            else:
                self.isStart = False

    def apply_speed_limit(self, state, response, goalSpeed=135):
        resp = self.sl_agent.drive(state)
        for key in ['accel', 'brake']:
            response[key] = resp[key]

        # if state['speedX'] > goalSpeed:
        #     if state['speedX'] > 5. + goalSpeed:
        #         response['brake'] = 1
        #     response['accel'] = 0
        # else:
        #     response['accel'] = 1
