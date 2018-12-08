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


def parse_dataset():
    data = []
    logs = glob.glob("important_logs/*.agent.log")
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
    return res


def extract_parameters(data):
    processed = [
        (
            {k: x[k] for k in settings['action_keys']},
            {k: x[k] for k in settings['state_keys']}
        )
        for x in data
        if np.all(np.array(x['track']) >= 0)
        if not (x['speedX'] == 0 and x['accel'] == 0)
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
    knn = KNeighborsClassifier()
    knn = DecisionTreeClassifier()
    # knn = RandomForestClassifier(50)

    def __init__(self):
        self.transmission = basicTransmission.Transmssion()

        data = parse_dataset()
        states, actions = extract_parameters(data)
        # self.actions = actions
        # Reducinf actions set
        self.Y, self.actions = unify_actions(actions)

        self.X = np.array(states)
        self.X_max = self.X.max(axis=0)
        self.X_min = self.X.min(axis=0)
        self.X_normed = (self.X - self.X_min) / (self.X_max - self.X_min)
        self.knn.fit(self.X_normed, self.Y)
        # self.knn = joblib.load('/home/kku/Dropbox/track_2_classifier')
        joblib.dump(self.knn, 'logs/DecisionTreeClassifier')

    def drive(self, state, **kwargs):
        response = utils.get_default_response()

        response['gear'] = self.transmission.get_new_gear(state)

        prepared_state = state_to_vector(
            state,
            keys_list=settings['state_keys']
        )
        state_normed = (prepared_state - self.X_min) / \
            (self.X_max - self.X_min)
        predicted_action = self.actions[
            self.knn.predict([state_normed])[0]
        ]

        return {**response, **predicted_action}


if __name__ == "__main__":
    Knn_agent()
