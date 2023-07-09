import pyaudio
import numpy as np
import math


def sine_sound(wave):
    # Set up parameters
    sample_rate = 44100

    # Open a new audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Play the sine wave
    stream.write(wave.astype(np.float32).tobytes())

    # Close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()


def play_sine(amplitude):
    duration=0.2
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    initial_t = np.linspace(0, 1, num_samples, endpoint=False)
    wave = np.sin(2 * math.pi * 440 * initial_t)*amplitude*1.5

    for i in range(35,151,5):
        tempwave =  np.sin(2 * math.pi * i * t)*amplitude
        wave = np.concatenate((wave, tempwave))

    for i in range(160,331,10):
        tempwave =  np.sin(2 * math.pi * i * t)*amplitude
        wave = np.concatenate((wave, tempwave))

    for i in range(400,1001,100):
        tempwave =  np.sin(2 * math.pi * i * t)*amplitude
        wave = np.concatenate((wave, tempwave))
    
    for i in range(2000,5001,1000):
        tempwave =  np.sin(2 * math.pi * i * t)*amplitude
        wave = np.concatenate((wave, tempwave))

    for i in range(6000,10001,2000):
        tempwave =  np.sin(2 * math.pi * i * t)*amplitude
        wave = np.concatenate((wave, tempwave))

    for i in [15000,18000]:
        tempwave =  np.sin(2 * math.pi * i * t)*amplitude
        wave = np.concatenate((wave, tempwave))

    sine_sound(wave)
