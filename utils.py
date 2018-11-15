import arrow
import numpy as np
import csv


def generate_id():
    return arrow.now().format('YYYY-MM-DD_HH:mm:ss_SSS')


def logfile_name_agent(id):
    return f'{id}.agent.log'


def logfile_name_torcs(id):
    return f'{id}.torcs.log'


def parse_agent_logfile(id):
    with open(f'logs/{logfile_name_agent(id)}') as f:
        reader = csv.DictReader(f)
        return list(reader)


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


def was_on_track_all_the_time(id):
    log = parse_agent_logfile(id)
    trackPoses = np.array([x['trackPos'] for x in log], dtype='float')
    return np.all(np.abs(trackPoses) <= 1.)


def rate_race(id):
    lap_time = race_first_lap_time(id)
    if was_on_track_all_the_time(id) and lap_time is not None:
        return lap_time
    if lap_time is not None:
        return lap_time + 10. ** 5
    else:
        return 10. ** 6
