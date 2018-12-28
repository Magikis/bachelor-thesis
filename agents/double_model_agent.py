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

    def load(self, path):
        print('Loading model')
        arrs = np.load(f'{path}/parameters.npz')
        self.speed_actions_labels = arrs['speed_actions_labels']
        self.state_keys = arrs['state_keys']
        self.speed_classifier = joblib.load(f'{path}/speed_classifier')
        self.steer_regressor = joblib.load(f'{path}/steer_regressor')
        self.scaler = joblib.load(f'{path}/scaler')
