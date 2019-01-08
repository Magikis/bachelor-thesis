import joblib
import json
import numpy as np
import agents.utils as utils
import agents.basicTransmission as basicTransmission
from agents.knn import state_to_vector
from settings import settings


class SingleModelAgent():
    def __init__(self, model_path, **kwargs):
        self.transmission = basicTransmission.Transmssion()
        self.load(model_path)

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        vector_before_norm = state_to_vector(state, self.state_keys)

        state_vector = self.scaler.transform(
            vector_before_norm[np.newaxis, :]
        )
        
        action_id = self.classifier.predict(
            state_vector
        )[0]

        return {
            **response,
            **self.actions[action_id],
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
        self.actions = arrs['actions']
        self.state_keys = arrs['state_keys']
        self.classifier = joblib.load(f'{path}/classifier')
        self.scaler = joblib.load(f'{path}/scaler')
