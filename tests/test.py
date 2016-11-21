import pyaudio
import wave
from time import gmtime, strftime
import sys
import select
import os

# Name of sub-directory where WAVE files are placed
current_experiment_path = os.path.dirname(os.path.realpath(__file__))
# subdir_recording = '/recording/'
subdir_recording = '/'

# print current_experiment_path + subdir_recording

# Variables for Pyaudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANGELS = 1
RATE = 44100

# Set variable for the labelling of the recorded WAVE file.
# timestamp = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
# wave_output_filename = '%s.wav' % self.get('subject_nr')
# wave_output_filename = '%s.wav' % timestamp
wave_output_filename = 'out.wav'

print(current_experiment_path + subdir_recording + wave_output_filename)

# pyaudio recording stuff
p = pyaudio.PyAudio()

for x in range(p.get_device_count()):
    info = p.get_device_info_by_index(x)
    if info['maxInputChannels'] > 0:
        print('---------------------------------')
        print(str(x) + str(info))
        print('---------------------------------')
        # USB Audio Device / Airmouse: USB Audio
        if info['name'].startswith('default'):
            INPUT_DEVICE_INDEX = info['index']
            RATE = int(info['defaultSampleRate'])
            CHANNELS = int(info['maxInputChannels'])

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=INPUT_DEVICE_INDEX)

print("* recording")

# Create an empty list for audio recording
all = []

# Record audio until Enter is pressed
i = 0
while True:
    # os.system('cls' if os.name == 'nt' else 'clear')
    print(
        "Recording Audio. Press Enter to stop recording and save file.")
    print(i)
    data = stream.read(CHUNK)
    all.append(data)
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        break
    i += 1

print("* done recording")

# Close the audio recording stream
# stream.stop_stream()
stream.close()
p.terminate()

# write data to WAVE file
wf = wave.open(
    current_experiment_path + subdir_recording + wave_output_filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(all))
wf.close()
