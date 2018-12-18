def get_default_response():
    response = {
        'gear': 1,
        'clutch': 0,
        'focus': [-90, -45, 0, 45, 90],
        'accel': 0,
        'brake': 0,
        'steer': 0,
        'meta': 0
    }
    return response


class HumanInput():
    def __init__(self, verbose=True):
        import pynput
        self.state = {k: False for k in self.cmds.values()}
        self.listener = pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        # self.listener.wait()
        # self.listener.join()

        if verbose:
            print('Controls:')
            for k, cmd in self.cmds.items():
                print(f'{cmd}: {k}')

    cmds = {
        'l': 'accel',
        'k': 'brake',
        'a': 'left',
        'd': 'right',
    }

    def on_press(self, key):
        if key.char in self.cmds.keys():
            self.state[self.cmds[key.char]] = True

    def on_release(self, key):
        if key.char in self.cmds.keys():
            self.state[self.cmds[key.char]] = False

    def get_state(self):
        return self.state

    def restart_state(self):
        for x in self.cmds.values():
            self.state[x] = False

    def shutdown(self):
        self.listener.stop()
