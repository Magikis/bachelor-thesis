from main import main
import utils
import subprocess
import numpy as np
import os
import settings


def run_practice(id, verbose=False, **kwargs):
    if verbose:
        print(f'Id of run: {id}')
    subprocess.run([
        'pkill',
        'torcs'
    ])

    with open(f'logs/{utils.logfile_name_torcs(id)}', 'w') as torcs_log:
        torcs_instance = subprocess.Popen(
            [
                'torcs',
                '-r', f'{os.getcwd()}/tracks/{settings.track}_practice.xml',
            ],
            stdout=torcs_log
        )

        main(id, **kwargs)

        torcs_instance.wait()


if __name__ == "__main__":
    id = utils.generate_id()
    run_practice(id, verbose=True)
    print(f'Race rating: {utils.rate_race(id)}')
