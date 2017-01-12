from array import array
import struct
import pyaudio
import requests
import math

THRESHOLD = .09
CHUNK_SIZE = 512
FORMAT = pyaudio.paInt16
RATE = 16000
SHORT_NORMALIZE = (1.0/32768.0)
access_key = 'MEN4GZIFBTCEVKCMETRNYPYJBZXMGAMI'


# Returns if the RMS of block is less than the threshold
def is_silent(block):
    count = len(block)/2
    form = "%dh" % (count)
    shorts = struct.unpack(form, block)
    sum_squares = 0.0

    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    rms_value = math.sqrt(sum_squares / count)
    return rms_value, rms_value <= THRESHOLD


# Returns as many (up to returnNum) blocks as it can.
def returnUpTo(iterator, values, returnNum):
    if iterator+returnNum < len(values):
        return (iterator + returnNum,
                "".join(values[iterator:iterator + returnNum]))

    else:
        temp = len(values) - iterator
        return (iterator + temp + 1, "".join(values[iterator:iterator + temp]))


# Python generator- yields roughly 512k to generator.
def gen(p, stream):
    num_silent = 0
    snd_started = False
    counter = 0
    print("Microphone on!")
    i = 0
    data = []

    while 1:
        rms_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        snd_data = array('i', rms_data)
        for d in snd_data:
            data.append(struct.pack('<i', d))
        rms, silent = is_silent(rms_data)

        if silent:
            num_silent += 1
            print('silent: ' + str(num_silent))
        else:
            print('NO silent: ' + str(num_silent))

        if silent and snd_started:
            # num_silent += 1
            pass

        elif not silent and not snd_started:
            i = len(data) - CHUNK_SIZE*2  # Set the counter back a few seconds
            if i < 0:                     # so we can hear the start of speech.
                i = 0
            snd_started = True
            print("TRIGGER at " + str(rms) + " rms.")

        elif not silent and snd_started and not i >= len(data):
            i, temp = returnUpTo(i, data, 512)
            yield temp
            num_silent = 0

        # if snd_started and num_silent > 20:
        #    print("Stop Trigger")
        #    break

        if counter > 75:  # Slightly less than 10 seconds.
            print("Timeout, Stop Trigger")
            break

        if snd_started:
            counter = counter + 1

    # Yield the rest of the data.
    print("Pre-streamed " + str(i) + " of " + str(len(data)) + ".")
    while (i < len(data)):
        i, temp = returnUpTo(i, data, 512)
        yield temp
    print("Swapping to thinking.")


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=True,
                    frames_per_buffer=CHUNK_SIZE, input_device_index=8)

    headers = {'Authorization': 'Bearer ' + access_key,
               'Content-Type': 'audio/raw; encoding=signed-integer; bits=16;' +
               ' rate=16000; endian=little', 'Transfer-Encoding': 'chunked'}
    url = 'https://api.wit.ai/speech'

    foo = requests.post(url, headers=headers, data=gen(p, stream))
    stream.stop_stream()
    stream.close()
    p.terminate()
    print(foo.text)
    print("Done.")
