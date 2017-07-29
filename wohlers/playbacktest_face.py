#!/usr/bin/env python

# playbacktest.py
#
# This is an example of a simple sound playback script.
#
# The script opens an ALSA pcm for sound playback. Set
# various attributes of the device. It then reads data
# from stdin and writes it to the device.
#
# To test it out do the following:
# python recordtest.py out.raw # talk to the microphone
# python playbacktest.py out.raw


# Footnote: I'd normally use print instead of sys.std(out|err).write,
# but we're in the middle of the conversion between python 2 and 3
# and this code runs on both versions without conversion

import sys
import getopt
import alsaaudio
import pifacedigitalio as p


def usage():
    sys.stderr.write('usage: playbacktest.py [-c <card>] <file>\n')
    sys.exit(2)

if __name__ == '__main__':

    card = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for o, a in opts:
        if o == '-c':
            card = a

    if not args:
        usage()

    # Open the device in playback mode. 
    out = alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK, mode=alsaaudio.PCM_NORMAL, card=card)

    # Set attributes: Stereo, 44100 Hz, 16 bit little endian frames
    out.setchannels(2)
    out.setrate(44100)
    out.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    out.setperiodsize(256)
    
    p.init()
    
    p.digital_write(0, 1)
    
    diode = 1
    while True:
        
        if p.digital_read(0) == 1:
            p.digital_write(diode, 1)
            f = open(args[0], 'rb')
            
            # Read data from stdin
            data = f.read(1024)
            while data:
                data = data.rjust(1024, data[-1])
                out.write(data)
                data = f.read(1024)

            p.digital_write(diode, 0)
            f.close()
            diode += 1
            if diode == 8:
                diode = 1
            
        if p.digital_read(1) == 1:
            p.digital_write(0, 0)
            sys.exit(0)
