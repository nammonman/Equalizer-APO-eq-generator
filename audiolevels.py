import soundfile as sf
import numpy as np

def calculate_average_volume(file_path="trimmed_audio.wav"):
    audio_data, sample_rate = sf.read(file_path)

    # Convert audio data to mono if it has multiple channels
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)

    # Calculate the root mean square (RMS) of the audio data
    rms = np.sqrt(np.mean(audio_data ** 2))

    # Calculate the average volume (in dB) using the sample rate
    average_volume = 20 * np.log10(rms)

    return average_volume


def calculate_average_volume_segments(file_path="trimmed_audio.wav" , segment_duration=0.2):
    audio_data, sample_rate = sf.read(file_path)

    # Convert audio data to mono if it has multiple channels
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)

    segment_samples = int(segment_duration * sample_rate)
    total_samples = len(audio_data)
    num_segments = total_samples // segment_samples

    average_volume_list = []
    for i in range(num_segments):
        segment_start = i * segment_samples
        segment_end = (i + 1) * segment_samples
        segment = audio_data[segment_start:segment_end]

        # Calculate the root mean square (RMS) of the segment
        rms = np.sqrt(np.mean(segment ** 2))

        # Calculate the average volume (in dB) using the sample rate
        average_volume = 20 * np.log10(rms)
        average_volume_list.append(average_volume)

    return average_volume_list

'''
# avg volume
average_volume = calculate_average_volume()
print(f"Average Volume: {average_volume} dB")

# each frequency
average_volume_list = calculate_average_volume_segments()
'''

def calculate_eq(average_volume_list, average_volume, bass_extension, intensity):
    output_text = ""
    freq_list = []
    delta_volume_list = []

    for j in range(35,151,5):
        freq_list.append(j)

    for j in range(160,331,10):
        freq_list.append(j)

    for j in range(400,1001,100):
        freq_list.append(j)

    for j in range(2000,5001,1000):
        freq_list.append(j)

    for j in range(6000,10001,2000):
        freq_list.append(j)

    for j in [15000,18000]:
        freq_list.append(j)
    
    for i, volume in enumerate(average_volume_list):
        #print(f"Segment {i + 1}: {volume} dB")
        if freq_list[i] < bass_extension:
            delta_volume_list.append((average_volume-volume)/4)
        else:
            delta_volume_list.append((average_volume-volume))
    
    #normalize eq
    highest_band = max(delta_volume_list)
    if highest_band > 0:
        for i in range(len(delta_volume_list)):
            delta_volume_list[i] = delta_volume_list[i] - highest_band
    
    for i, volume in enumerate(delta_volume_list):
        output_text += " " + str(freq_list[i]) + " " + str(volume*intensity)
        if i != 57:
            output_text += ';'
        
    return output_text