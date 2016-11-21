from asyncore import file_dispatcher, loop
from evdev import InputDevice
dev = InputDevice('/dev/input/event18')


class InputDeviceDispatcher(file_dispatcher):
    def __init__(self, device):
        self.device = device
        file_dispatcher.__init__(self, device)

    def recv(self, ign=None):
        return self.device.read()

    def handle_read(self):
        for event in self.recv():
            print(repr(event))


# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
    InputDeviceDispatcher(dev)
    loop()

    # item = sys.argv[1]
    # print('item to precess: ' + item)

if __name__ == '__main__':
    main()
