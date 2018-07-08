import snakeoil2015.snakeoil as so
import json

def drive(arg):
    S, R = c.S.d, c.R.d
    return ""

def drivingLoop():
    C = so.Client()
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        print(json.dumps(C))
        raise Exception
        C.respond_to_server()
    C.shutdown()


# ================ MAIN ================
if __name__ == "__main__":
    drivingLoop()
