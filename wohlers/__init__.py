import pyaudio
import wave

CHUNK = 1024

wf = wave.open('/home/daniel/vintage_microwave_oven.wav', 'rb')

audio = pyaudio.PyAudio()
stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=44100, output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

audio.terminate()