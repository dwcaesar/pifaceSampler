import thread
import time
import playbacktest

__author__ = 'daniel'

thread.start_new_thread(playbacktest.play, ('/home/daniel/vintage_microwave_oven.wav',))
time.sleep(0.1)
thread.start_new_thread(playbacktest.play, ('/home/daniel/vintage_microwave_oven.wav',))
time.sleep(0.1)
thread.start_new_thread(playbacktest.play, ('/home/daniel/vintage_microwave_oven.wav',))

time.sleep(2)
