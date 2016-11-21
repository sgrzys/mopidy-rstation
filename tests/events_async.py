import asyncio
import evdev


@asyncio.coroutine
def print_events(device):
    while True:
        events = yield from device.async_read()
        for event in events:
            print(device.fn, evdev.categorize(event), sep=': ')

mouse = evdev.InputDevice('/dev/input/eventX')
keybd = evdev.InputDevice('/dev/input/eventY')

for device in mouse, keybd:
    asyncio.async(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()
