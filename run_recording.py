from main import drivingLoop
from agents.human_recorder import HumanDrive
import utils
from agents.utils import HumanInput
import os
import sys
from distutils.util import strtobool


def prompt(query):
    sys.stdout.write('%s [y/n]: ' % query)
    val = input()
    try:
        ret = strtobool(val)
    except ValueError:
        sys.stdout.write('Please answer with a y/n\n')
        return prompt(query)
    return ret


if __name__ == "__main__":
    # hi = HumanInput()
    # while True:
    #     pass
    id = utils.generate_id()
    drivingLoop(
        HumanDrive(),
        id
    )
    print(f'Id of run was: {id}')
    log_file_name = utils.logfile_name_agent(id)
    dir_name = 'temp_saved_data'
    if prompt(f'Do you want to save recording to "{dir_name}"?'):
        os.system(' '.join([
            'cp',
            f'logs/{log_file_name}',
            f'{dir_name}/{log_file_name}'
        ]))
