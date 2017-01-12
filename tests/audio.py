import pyaudio
import wave


CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "/home/pi/mopidy-rstation/tests/output.wav"
INPUT_DEVICE_INDEX = 0


p = pyaudio.PyAudio()
for x in range(p.get_device_count()):
    info = p.get_device_info_by_index(x)
    if info['maxInputChannels'] > 0:
        print('---------------------------------')
        print(str(x) + str(info))
        print('---------------------------------')
        # USB Audio Device / Airmouse: USB Audio / HDA Intel
        if info['name'].startswith('default'):
            INPUT_DEVICE_INDEX = info['index']
            RATE = int(info['defaultSampleRate'])
            # CHANNELS = int(info['maxInputChannels'])
            CHANNELS = 1

print('selected device index: ' + str(INPUT_DEVICE_INDEX))
print('selected device rate: ' + str(RATE))
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    input_device_index=INPUT_DEVICE_INDEX)

print("* recording")
all = []
for i in range(0, RATE / CHUNK * RECORD_SECONDS):
    data = stream.read(CHUNK)
    all.append(data)
print("* done recording")

stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(all))
wf.close()
