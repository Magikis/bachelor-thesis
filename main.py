import sys
import numpy
import csv
import datetime

from snakeoil.snakeoil import Client
from settings import settings
import agents.line_folower as line_folower
import utils


def drivingLoop(drivingFunc, id, **kwargs):
    try:
        C = Client()
        with open(f'logs/{utils.logfile_name_agent(id)}', 'w') as f:
            writer = csv.DictWriter(f, settings['log_keys'])
            writer.writeheader()
            while True:
                C.get_servers_input()
                data = C.S.d
                data.update(angle=numpy.degrees(data['angle']))
                response = drivingFunc(data, **kwargs)
                C.R.d = {**response}
                sys.stdout.flush()
                writer.writerow({**data, **response})

                C.respond_to_server()
        C.shutdown()
    except Exception as e:
        if str(e) != 'RACE_ENDED':
            raise


def main(id=None, **kwargs):
    drivingLoop(
        line_folower.drive,
        id if id else utils.generate_id(),
        **kwargs
    )


# ================ MAIN ================
if __name__ == "__main__":
    main()