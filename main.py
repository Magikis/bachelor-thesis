import sys
import numpy

from snakeoil.snakeoil import Client
# from agents.lineFolowerContinus import drive
# from agents.lineForowerDiscreate import drive as driveDescrete
from settings import settings
import agents.line_folower as line_folower
import agents.lineForowerDiscreate as discreate
import agents.lineFolowerContinus as continous
import datetime


def drivingLoop(drivingFunc):
    C = Client()
    import csv
    with open(f'logs/{datetime.datetime.now()}', 'w') as f:
        writer = csv.DictWriter(f, settings['log_keys'])
        writer.writeheader()
        while True:
            C.get_servers_input()
            data = C.S.d
            data.update(angle=numpy.degrees(data['angle']))
            response = drivingFunc(data, 0)
            C.R.d = {**response}
            sys.stdout.flush()
            writer.writerow({**data, **response})

            C.respond_to_server()
    C.shutdown()


# ================ MAIN ================
if __name__ == "__main__":

    drivingLoop(
        line_folower.drive
        # discreate.drive
        # continous.drive
    )
