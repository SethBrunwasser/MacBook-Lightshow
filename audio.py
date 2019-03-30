import pyaudio, audioop, wave, sys
from subprocess import run

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
POLL_SPEED = 0.001
channel_map = (0, 1)


stream_info = pyaudio.PaMacCoreStreamInfo(
    flags = pyaudio.PaMacCoreStreamInfo.paMacCorePlayNice,
    channel_map = channel_map)

def get_mic(p):

    print(stream_info)
    stream = p.open(format = FORMAT,
                    rate = RATE,
                    input = True,
                    input_host_api_specific_stream_info = stream_info, # stream_info
                    channels = CHANNELS,
                    frames_per_buffer=CHUNK)
    '''stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)'''
    return stream


def runloop(stream):
    while True:
        data = stream.read(CHUNK, exception_on_overflow = False)
        rms = audioop.rms(data, 2)         # here's where you calculate the volume
        level = rms * 10
        #print(level)
        run(['./kbbutil', str(level)])


if __name__ == '__main__':
    print('[+] Starting...')
    p = pyaudio.PyAudio()
    SPEAKERS = p.get_default_output_device_info()
    print(SPEAKERS)
    stream = get_mic(p)
    try:
        runloop(stream)
    except (KeyboardInterrupt, Exception):
        stream.stop_stream()
        stream.close()
        p.terminate()
        print('[X] Stopped.')

'''
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()
channel_map = (0, 1)

stream_info = pyaudio.PaMacCoreStreamInfo(
    flags = pyaudio.PaMacCoreStreamInfo.paMacCorePlayNice,
    channel_map = channel_map)

stream = p.open(format = FORMAT,
                rate = RATE,
                input = True,
                input_host_api_specific_stream_info = stream_info,
                channels = CHANNELS)

all = []
for i in range(0, RATE / chunk * RECORD_SECONDS):
        data = stream.read(chunk)
        all.append(data)
stream.close()
p.terminate()

'''

