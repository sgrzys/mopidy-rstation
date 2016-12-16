import evdev


def main():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        print(device.fn, device.name, device.phys)


if __name__ == '__main__':
    main()
