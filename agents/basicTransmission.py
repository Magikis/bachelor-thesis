

class Transmssion():
    def __init__(self):
        pass
    
    _current_gear = 1

    def get_new_gear(self, state):
        new_gear = self._current_gear

        if self._current_gear == 1:
            if state['rpm'] > 9000.0 and state['speedX'] > 10:
                new_gear = self._current_gear + 1
            elif False:
                new_gear = self._current_gear - 1
        elif self._current_gear == 2:
            if state['rpm'] > 9000.0:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 35:
                new_gear = self._current_gear - 1
        elif self._current_gear == 3:
            if state['rpm'] > 9000.0:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 100:
                new_gear = self._current_gear - 1
        elif self._current_gear == 4:
            if state['rpm'] > 9000.0:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 150:
                new_gear = self._current_gear - 1
        elif self._current_gear == 5:
            if state['rpm'] > 9000.0:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 200:
                new_gear = self._current_gear - 1
        elif self._current_gear == 6:
            if False:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 240:
                new_gear = self._current_gear - 1

        self._current_gear = new_gear
        return new_gear
