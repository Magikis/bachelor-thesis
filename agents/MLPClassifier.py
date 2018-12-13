import numpy as np
import glob
import json
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import agents.utils as utils
import agents.basicTransmission as basicTransmission
from agents.knn import *
from settings import settings


class MLPClassifier_agent():
    def __init__(self, model_path):
        self.transmission = basicTransmission.Transmssion()
        self.load(model_path)

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        prepared_state = state_to_vector(
            state,
            keys_list=self.state_keys
        )

        state_normed = self.scaler.transform([prepared_state])

        predicted_action = self.actions[
            self.classifier.predict([state_normed])[0]
        ]

        return {**response, **predicted_action}

    def load(self, path):
        print('Loading model')
        arrs = np.load(f'{path}/parameters.npz')
        self.actions = arrs['actions']
        self.state_keys = arrs['state_keys']
        self.classifier = joblib.load(f'{path}/classifier')
        self.scaler = joblib.load(f'{path}/scaler')

    # def dump(self):
    #     path = 'saved_model'
    #     print(f'Dumping model to: {path}')
    #     np.savez(
    #         'saved_model/parameters.npz',
    #         **{
    #             'X_max': self.X_max,
    #             'X_min': self.X_min,
    #             'actions': self.actions,
    #             'state_keys': self.state_keys
    #         }
    #     )
    #     joblib.dump(self.knn, 'saved_model/model')

