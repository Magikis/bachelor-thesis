import numpy as np
import runPractice
import utils
import json


def bisect(f, a, times, alpha=150):
    F_a = f(a)
    history = [(a, F_a)]
    mem = {a: F_a}
    for i in range(times):
        if (a + alpha) in mem:
            res = mem[a + alpha]
        else:
            res = f(a + alpha)
            mem[a + alpha] = res
        history.append((a + alpha, res))
        if res < F_a:
            a += alpha
            F_a = res
            if a >= 300.:
                return (300., history)
        else:
            if alpha < 1.:
                print(f'{i + 1} times')
                return (a, history)
            alpha /= 2
    print(mem)
    return (a, history)


def main(**args):
    table = np.array([40.] * 8)
    hist = []
    for i, x in enumerate(table):
        speed_limits = table.copy()

        def f(x):
            id = utils.generate_id()
            speed_limits[i] = x
            runPractice.run_practice(id, speed_limits=speed_limits, **args)
            score = utils.rate_race(id)
            print(f'Score: {score}, speed_limits: {speed_limits}, id: {id}')
            return score

        values = bisect(f, x, 20, alpha=150)
        table[i] = values[0]
        hist.append(values)
    print('LEARNIG RESULT:', list(table))
    with open('logs/speed_limits.log', 'w') as f:
        f.write(json.dumps(hist))
        # f.write('\n')


if __name__ == "__main__":
    args = utils.activate_parser()
    main(**args)
