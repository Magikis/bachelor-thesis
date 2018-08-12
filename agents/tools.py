from snakeoil.client import automatic_transimission


def my_transimission(state, response, target_speed):
    R['gear'], R['clutch'] = automatic_transimission(
        P,
        state['rpm'],
        state['gear'],
        R['clutch'],
        state['rpm'],
        state['speedX'],
        target_speed,
        tick
    )
