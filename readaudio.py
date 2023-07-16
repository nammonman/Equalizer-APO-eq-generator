import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

def save_trimmed_audio(filename, trimmed_audio, sample_rate):
    # Save the trimmed audio as a WAV file
    wavfile.write(filename, sample_rate, trimmed_audio)

def trim_audio_section(filename):
    # Load the audio file
    sr, audio = wavfile.read(filename)

    # Compute the time array
    duration = len(audio) / sr
    t = np.linspace(0, duration, len(audio))

    # Plot the waveform
    fig = plt.figure(figsize=(10, 4), tight_layout=True)
    fig.canvas.manager.toolbar.pack_forget()
    ax = fig.add_subplot(111)
    ax.plot(t, audio)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('CLICK THE SPOT AFTER THE FIRST BEEP')

    # Prompt the user to select the start and end points for trimming
    points = plt.ginput(n=1, show_clicks=True)
    plt.close()
    
    # Extract the selected section
    start_time, end_time = points[0][0], points[0][0]+11.6
    start_index = int(start_time * sr)
    end_index = int(end_time * sr)
    trimmed_audio = audio[start_index:end_index]

    # Plot the trimmed section
    '''
    plt.figure(figsize=(10, 4))
    t_trimmed = np.linspace(start_time, end_time, len(trimmed_audio))
    plt.plot(t_trimmed, trimmed_audio)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Trimmed Audio Section')
    plt.show()
    '''
    # Save the trimmed audio as a WAV file
    save_trimmed_audio('trimmed_audio.wav', trimmed_audio, sr)
    

    return trimmed_audio

