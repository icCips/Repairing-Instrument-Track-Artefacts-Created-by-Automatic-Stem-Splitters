import os
from pydub import AudioSegment

# Function to resample audio to 16kHz and segment into 5s chunks
def resample_and_segment(input_path, output_dir):
    try:
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(16000)

        segment_duration = 5000  # 5 seconds in milliseconds
        num_segments = len(audio) // segment_duration
        
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        for i in range(num_segments + 1):  # +1 to handle the last segment
            start_time = i * segment_duration
            end_time = start_time + segment_duration
            segment = audio[start_time:end_time]

            if len(segment) == 0:
                break  # Stop if there's no more audio to process

            output_filename = f"{base_name}_{i+1}.wav"
            output_path = os.path.join(output_dir, output_filename)
            segment.export(output_path, format="wav")
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def resample_and_chunk(base_dir, output_base_dir):
    # Base directories
    #base_dir = "datasets/sgmse_vocal"
    #output_base_dir = "datasets/sgmse_vocal_16kHz"

    # Create the new dataset directory structure

    for subdir, _, files in os.walk(base_dir):
        relative_path = os.path.relpath(subdir, base_dir)
        output_subdir = os.path.join(output_base_dir, relative_path)
        
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
            print(f"Created directory: {output_subdir}")
        
        l = len(files)
        
        for i, file in enumerate(files):
            if file.endswith(".wav"):
                input_file = os.path.join(subdir, file)
                print(f"resampling and chunking: {output_subdir} - {i+1}/{l}")
                resample_and_segment(input_file, output_subdir)