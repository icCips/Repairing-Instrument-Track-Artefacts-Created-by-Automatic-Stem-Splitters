
import os
from pydub import AudioSegment

# Function to resample audio to 16kHz
def resample_to_16kHz(input_path, output_path):
    try:
        audio = AudioSegment.from_file(input_path)
        audio_16kHz = audio.set_frame_rate(16000)
        audio_16kHz.export(output_path, format="wav")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def resample(base_dir, output_base_dir):
    # Base directories
    #base_dir = "datasets/sgmse_vocal"
    #output_base_dir = "datasets/sgmse_vocal_16kHz"

    # Create the new dataset directory structure
    j = 0
    for subdir, _, files in os.walk(base_dir):
        j += 1
        relative_path = os.path.relpath(subdir, base_dir)
        output_subdir = os.path.join(output_base_dir, relative_path)
        
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        
        l = len(files)
        
        for i, file in enumerate(files):
            if file.endswith(".wav"):
                input_file = os.path.join(subdir, file)
                output_file = os.path.join(output_subdir, file)
                print(f"resampling: subdir {j} - {i+1}/{l}")
                resample_to_16kHz(input_file, output_file)