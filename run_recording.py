from main import drivingLoop
from agents.human_recorder import HumanDrive
import utils
from agents.utils import HumanInput

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
