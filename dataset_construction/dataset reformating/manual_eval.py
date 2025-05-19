from pydub import AudioSegment
from pydub.playback import play
import os
import random
import time

def play_audio(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        play(audio)
    except Exception as e:
        print(f"Error: {e}")
        
def pick_random_file(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            print("No files found in the folder.")
            return None
        return random.choice(files)
    except Exception as e:
        print(f"Error: {e}")
        return None

#clean_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgmse_vocal_16kHz/test/clean"
#noisy_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgmse_vocal_16kHz/test/noisy"
#enhanced_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/enhanced"


#clean_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgsme_vocal_16kHz_5s_chunks_rand/test/clean"
#noisy_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgsme_vocal_16kHz_5s_chunks_rand/test/noisy"
#enhanced_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/enhanced_5s"

clean_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgmse_bass_16kHz_5s_chunks/test/clean"
noisy_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/sgmse_bass_16kHz_5s_chunks/test/noisy"
enhanced_folder_path = "/Volumes/Bank_1/FYP/Model_Architectures/sgmse/datasets/enhanced_pot_bass"

random_file = pick_random_file(clean_folder_path)

if random_file in os.listdir(noisy_folder_path):
    print("Random file:", random_file)
    
else:
    print("Random file not found in noisy folder.")
    exit()
    
play_audio(os.path.join(clean_folder_path, random_file))
time.sleep(1)
play_audio(os.path.join(noisy_folder_path, random_file))
time.sleep(1)
play_audio(os.path.join(enhanced_folder_path, random_file))
