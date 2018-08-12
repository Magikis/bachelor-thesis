import sys
import numpy

from snakeoil.snakeoil import Client
# from agents.lineFolowerContinus import drive
# from agents.lineForowerDiscreate import drive as driveDescrete
import agents.line_folower as line_folower
import agents.lineForowerDiscreate as discreate
import agents.lineFolowerContinus as continous

def drivingLoop(drivingFunc):
    C = Client()
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        data = C.S.d
        data.update(angle=numpy.degrees(data['angle']))

        response = drivingFunc(data, step)
        C.R.d = {**response}
        sys.stdout.flush()

        C.respond_to_server()
    C.shutdown()


# ================ MAIN ================
if __name__ == "__main__":

    drivingLoop(
        line_folower.drive
        # discreate.drive
        # continous.drive
    )
