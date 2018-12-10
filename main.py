import sys
import numpy
import csv
import datetime

from snakeoil.snakeoil import Client
from settings import (settings, gen_log_object)
import agents.line_folower as line_folower
import agents.knn as knn_agent
import utils
import json
import time
import gc
C_maxSteps = 100000

# def save_log()


def drivingLoop(drivingClass, id, **kwargs):
    longets_time = 0
    try:
        logs = [None for i in range(C_maxSteps)]
        C = Client()
        gc.disable()
        for i in range(C.maxSteps):
            C.get_servers_input()
            start_time = time.time()
            data = C.S.d
            data.update(angle=numpy.degrees(data['angle']))
            response = drivingClass.drive(data, **kwargs)
            C.R.d = response
            logs[i] = gen_log_object(data, response)
            elapsed_time = time.time() - start_time
            C.respond_to_server()
            longets_time = max(elapsed_time, longets_time)

        C.shutdown()
    except Exception as e:
        if str(e) != 'RACE_ENDED':
            raise
    gc.enable()
    with open(f'logs/{utils.logfile_name_agent(id)}', 'w') as f:
        f.write(
            json.dumps(
                [
                    x for x in logs if x
                ]
            )
        )
    print(f'Longest time frame: {longets_time * 1000:.2f}ms')


def main(id=None, driver_type='line-follower', **kwargs):
    if id is None:
        id = utils.generate_id()

    if driver_type == 'line-follower':
        drive_fun = line_folower.Drive(**kwargs)
    elif driver_type == 'tree':
        drive_fun = knn_agent.Knn_agent(**kwargs)

    drivingLoop(
        drive_fun,
        id,
        **kwargs
    )


# ================ MAIN ================

if __name__ == "__main__":
    args = utils.activate_parser()
    main(**args)
    pass
