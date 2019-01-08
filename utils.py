import argparse
import arrow
import numpy as np
import csv
import json


def generate_id():
    return arrow.now().format('YYYY-MM-DD_HH:mm:ss_SSS')


def logfile_name_agent(id):
    return f'{id}.agent.log'


def logfile_name_torcs(id):
    return f'{id}.torcs.log'


def parse_agent_logfile(id):
    with open(f'logs/{logfile_name_agent(id)}') as f:
        return json.loads(f.read())


def race_first_lap_time(id):
    with open(f'logs/{logfile_name_torcs(id)}') as f:
        results = [
            {
                'laps': (x[1 + x.index('Laps:')]),
                'time': float(x[1 + x.index('Time:')])
            } for x in [x.split() for x in f if 'Sim' in x.split()]
        ]
    if len(results) > 0:
        return results[0]['time']
    return None


def was_agent_late(id):
    late_str = 'Timeout for client answer'
    with open(f'logs/{logfile_name_torcs(id)}') as f:
        return late_str in f.read()


def was_on_track_all_the_time(id):
    log = parse_agent_logfile(id)
    trackPoses = np.array([x['trackPos'] for x in log], dtype='float')
    return np.all(np.abs(trackPoses) < 1.)


class AgentWasLate(Exception):
    pass


def rate_race(id):
    if was_agent_late(id):
        raise AgentWasLate()
    lap_time = race_first_lap_time(id)
    if was_on_track_all_the_time(id) and lap_time is not None:
        return lap_time
    if lap_time is not None:
        return np.inf
    else:
        return np.inf


def activate_parser():
    parser = argparse.ArgumentParser(description='Run driver for Torcs')
    parser.add_argument(
        'driver_type',
        choices=['line-follower', 'tree', 'mlp', 'dma', 'dma-sh', 'sma'],
        default='tree',
        help='Choose agent for driving'
    )
    parser.add_argument(
        '--track'
    )
    # parser.add_argument(
    #     '--'
    # )
    parser.add_argument(
        '--model-path', '-m',
    )
    return vars(parser.parse_args())
