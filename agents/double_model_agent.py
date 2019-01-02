import joblib
import json
import numpy as np
import agents.utils as utils
import agents.basicTransmission as basicTransmission
from settings import settings


def extract_state(data_sample, state_keys, data_is_array=False):
    if data_is_array:
        return [extract_state(x, state_keys) for x in data_sample]
    state_vector = []
    for key in state_keys:
        if isinstance(data_sample[key], list):
            state_vector += data_sample[key]
        else:
            state_vector.append(data_sample[key])
    return state_vector


class DoubleModelAgent():
    def __init__(self, model_path, **kwargs):
        self.transmission = basicTransmission.Transmssion()
        self.load(model_path)

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        state_vector = self.scaler.transform(
            [extract_state(state, self.state_keys)]
        )

        steer_val = self.steer_regressor.predict(
            state_vector
        )[0]

        state_vector = np.hstack((state_vector, [[steer_val]]))

        speed_action_index = self.speed_classifier.predict(
            state_vector
        )[0]

        return {
            **response,
            'steer': steer_val,
            **self.speed_actions_labels[speed_action_index],
        }

    isStart = True

    def manage_start_accel(self, state, response):
        if self.isStart:
            if state['distFromStart'] > 1 and state['speedX'] < 50:
                response['accel'] = 1
                response['brake'] = 0
            else:
                self.isStart = False

    def load(self, path):
        print('Loading model')
        arrs = np.load(f'{path}/parameters.npz')
        self.speed_actions_labels = arrs['speed_actions_labels']
        self.state_keys = arrs['state_keys']
        self.speed_classifier = joblib.load(f'{path}/speed_classifier')
        self.steer_regressor = joblib.load(f'{path}/steer_regressor')
        self.scaler = joblib.load(f'{path}/scaler')


class DoubleModelAgentWithStatesHistory(DoubleModelAgent):
    states_history = []

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        extracted_state = extract_state(state, self.state_keys)
        if len(self.states_history) == 0:
            self.states_history.append(
                np.concatenate((
                    extracted_state,
                    (0, 0)
                ))
            )

        regressor_input = self.scaler.transform(
            [
                np.concatenate((
                    extracted_state,
                    self.states_history[-1]
                ))
            ]
        )

        steer_val = self.steer_regressor.predict(
            regressor_input
        )[0]

        classifier_input = np.concatenate((
            regressor_input[0],
            [steer_val]
        ))

        speed_action_index = self.speed_classifier.predict(
            [classifier_input]
        )[0]

        self.states_history.append(
            np.array([
                *extracted_state,
                steer_val,
                speed_action_index,
            ])
        )

        total_response = {
            **response,
            'steer': steer_val,
            **self.speed_actions_labels[speed_action_index],
        }

        self.manage_start_accel(state, total_response)
        return total_response
