import numpy as np
import glob
import json
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import agents.utils as utils
import agents.basicTransmission as basicTransmission
from settings import settings


def parse_dataset(dataset_path='important_logs', files_limit=None):
    data = []
    logs = glob.glob(f"{dataset_path}/*.agent.log")

    if files_limit is not None:
        logs = logs[:files_limit]

    for l in logs:
        with open(l) as f:
            data += json.loads(f.read())
    return data


def state_to_vector(s, keys_list=None):
    res = []
    if keys_list is None:
        generator = s.values()
    else:
        generator = (s[k] for k in keys_list)
    for v in generator:
        if isinstance(v, list):
            res += v
        else:
            res.append(v)
    return np.array(res)


def extract_parameters(
    data,
    action_keys=settings['action_keys'],
    state_keys=settings['state_keys']
):
    processed = [
        (
            {k: x[k] for k in action_keys},
            {k: x[k] for k in state_keys}
        )
        for x in data
        # if np.all(np.array(x['track']) >= 0)
        # if not (x['speedX'] == 0 and x['accel'] == 0)
    ]
    actions, states = zip(*processed)
    return list(map(state_to_vector, states)),  actions


def unify_actions(actions):
    a_set = set((tuple(a.items()) for a in actions))
    actions_mapping = {
        a: i
        for i, a in enumerate(a_set)
    }

    actions_labels = [actions_mapping[tuple(a.items())] for a in actions]
    return actions_labels, [dict(a) for a in actions_mapping.keys()]


class Knn_agent():
    # knn = KNeighborsClassifier()
    knn = DecisionTreeClassifier()
    # knn = RandomForestClassifier(50)

    def __init__(self, model_path=None, dump_after=True, **kwargs):
        self.transmission = basicTransmission.Transmssion()

        if model_path is None:
            self.state_keys = settings['state_keys']
            data = parse_dataset()
            states, actions = extract_parameters(data)
            # self.actions = actions
            # Reducinf actions set
            Y, self.actions = unify_actions(actions)

            X = np.array(states)
            self.X_max = X.max(axis=0)
            self.X_min = X.min(axis=0)
            X_normed = (X - self.X_min) / (self.X_max - self.X_min)
            self.knn.fit(X_normed, Y)

            if dump_after:
                self.dump()

        else:
            self.load(model_path)

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        prepared_state = state_to_vector(
            state,
            keys_list=self.state_keys
        )
        state_normed = (prepared_state - self.X_min) / \
            (self.X_max - self.X_min)
        predicted_action = self.actions[
            self.knn.predict([state_normed])[0]
        ]

        return {**response, **predicted_action}

    def load(self, path):
        print('Loading model')
        arrs = np.load(f'{path}/parameters.npz')
        self.X_max = arrs['X_max']
        self.X_min = arrs['X_min']
        self.actions = arrs['actions']
        self.state_keys = arrs['state_keys']
        self.knn = joblib.load(f'{path}/model')

    def dump(self):
        path = 'saved_model'
        print(f'Dumping model to: {path}')
        np.savez(
            'saved_model/parameters.npz',
            **{
                'X_max': self.X_max,
                'X_min': self.X_min,
                'actions': self.actions,
                'state_keys': self.state_keys
            }
        )
        joblib.dump(self.knn, 'saved_model/model')


if __name__ == "__main__":
    Knn_agent(dump_after=True)
