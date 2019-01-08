from main import main
import utils
import subprocess
import numpy as np
import os
import settings


def run_practice(
    id,
    verbose=False,
    track=settings.get_track(),
    **kwargs
):
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
                '-t', '100000',
                '-r', f'{os.getcwd()}/tracks/{track}.xml',
            ],
            stdout=torcs_log
        )

        main(id, **kwargs)

        torcs_instance.wait()


if __name__ == "__main__":
    args = utils.activate_parser()
    id = utils.generate_id()
    run_practice(id, verbose=True, **args)
    print(f'Race rating: {utils.rate_race(id)}')
