"""
Created on Sun Oct 16 19:29:55 2016

@author: Madhatterr
"""

import pyaudio as pa
import wave
from sys import byteorder
from array import array
from scipy.fftpack import fft
import numpy as np

CHUNK = 1024
FORMAT = pa.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "MONO.wav"

def record(audio):
	stream = audio.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	print "###RECORDING###"

	s = array('h')
	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
		snd_data = array('h', data)
		if byteorder == 'big':
			snd_data.byteswap()
		s.extend(snd_data)

	print "###RECORDING DONE###"

	stream.stop_stream()
	stream.close()
	audio.terminate()
	return s, frames

def writeToWav(audio,frames):
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(audio.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	
def getMonotoneFrequency(x):
	X = fft(x)
	freq = (np.abs(X)).argmax() / RECORD_SECONDS + 1
	print "Monotone frequency is:", freq
	return freq
	
audio = pa.PyAudio()
frames = []
audioVector, frames = record(audio)
getMonotoneFrequency(audioVector)
writeToWav(audio,frames)