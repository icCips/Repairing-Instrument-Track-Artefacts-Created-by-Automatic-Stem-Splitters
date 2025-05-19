import time_code_util as tcu
import soundfile as sf
import process_track as pt
import numpy as np

def is_file_empty(audio, tolerance=1e-2):

    return np.all(np.abs(audio) < tolerance)

# Load the audio file
filename = '18_LeadVox.wav'  # Replace with your file path
data, samplerate = sf.read(filename)

cut = tcu.cut_audio(data, samplerate, 0, 100000)

if is_file_empty(cut):
    print("The file is considered empty.")
else:
    print("The file is not empty.")
    
norm = pt.normalize_audio(cut, samplerate, -10)

# Define the output file path
output_filename = 'output_file.wav'  # Replace with your desired output file path

# Save the audio data to the new file
sf.write(output_filename, norm, samplerate)
    
