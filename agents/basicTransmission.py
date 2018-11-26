

class Transmssion():
    def __init__(self):
        pass
    
    _current_gear = 1

    def get_new_gear(self, state):
        new_gear = self._current_gear

        if self._current_gear == 1:
            if state['speedX'] > 50:
                new_gear = self._current_gear + 1
            elif False:
                new_gear = self._current_gear - 1
        elif self._current_gear == 2:
            if state['speedX'] > 80:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 45:
                new_gear = self._current_gear - 1
        elif self._current_gear == 3:
            if state['speedX'] > 110:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 75:
                new_gear = self._current_gear - 1
        elif self._current_gear == 4:
            if state['speedX'] > 140:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 105:
                new_gear = self._current_gear - 1
        elif self._current_gear == 5:
            if state['speedX'] > 170:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 135:
                new_gear = self._current_gear - 1
        elif self._current_gear == 6:
            if False:
                new_gear = self._current_gear + 1
            elif state['speedX'] <= 165:
                new_gear = self._current_gear - 1

        self._current_gear = new_gear
        return new_gear
