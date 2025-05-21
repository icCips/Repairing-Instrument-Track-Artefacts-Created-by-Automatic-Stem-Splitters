import numpy as np
import MixR.pedalboard_util as pu
import random as r
import MixR.time_code_util as tcu
import soundfile as sf
from pydub import AudioSegment
from pydub.effects import high_pass_filter
import pedalboard as pdlb

def get_max_db(data):

    peak_amplitude = np.max(np.abs(data))
    
    max_db = 20 * np.log10(peak_amplitude)
    
    return max_db

def is_empty(audio, tolerance=1e-2):
    
    if audio is None:
        
        return True

    return np.all(np.abs(audio) < tolerance)

def is_white_noise(audio_file, start_time_ms = 10000, duration_ms = 3000, volume_threshold=-20.0):
    audio = AudioSegment.from_file(audio_file)
    
    end_time_ms = start_time_ms + duration_ms
    audio_slice = audio[start_time_ms:end_time_ms]
    
    audio_filtered = high_pass_filter(audio_slice, 7000)
    
    loudness = audio_filtered.dBFS
    
    return loudness > volume_threshold

def track_type_mapping(file_name, folder):
    lcfn = file_name.lower()

    if folder.lower() == "drums":
        
        if "snare" in lcfn:
            return "snare"
        if "kick" in lcfn or "bd" in lcfn or "bassdrum" in lcfn:
            return "kick"
        if "tom" in lcfn:
            return "tom"
        if "hat" in lcfn or "hh" in lcfn:
            return "hi-hat"
        if "oh" in lcfn or "overheads" in lcfn:
            return "oh"
        if "ride" in lcfn or "crash" in lcfn:
            return "cymbal"
        
        return "perc"
        
    if folder.lower() == "bass":
        
        if "di" in lcfn:
            return "bass_di"
        if "amp" in lcfn:
            return "bass_amp"
        if "double" in lcfn or "upright" in lcfn:
            return "double_bass"
        if "synth" in lcfn:
            return "synth_bass"
        
        return "bass"
        
    if folder.lower() == "vocals":
        
        if "main" in lcfn or "lead" in lcfn:
            return "main_vox"
    
        return "vox"
        
    if folder.lower() == "other":
        if "elec" in lcfn and ("gtr" in lcfn or "guit" in lcfn) or "rhythm" in lcfn and ("gtr" in lcfn or "guit" in lcfn):
            return "elec_gtr"
        if "gtr" in lcfn or "guit" in lcfn:
            return "gtr"
        if "lead" in lcfn and ("gtr" in lcfn or "guit" in lcfn):
            return "lead_gtr"
        if "piano" in lcfn:
            return "piano"
        if "synth" in lcfn:
            return "synth"
        if "organ" in lcfn:
            return "organ"
        if "wurl" in lcfn or "rho" in lcfn or ("elec" in lcfn and "piano" in lcfn):
            return "elec_piano"
        if "sax" in lcfn or "tru" in lcfn or "trom" in lcfn or "trm" in lcfn:
            return "brass"
        if "vio" in lcfn or "cel" in lcfn:
            return "strings"
        if "banjo" in lcfn:
            return "banjo"
        
        return "other"

    return "other"

def dropout():
    
    p = 0.15
    
    if r.random() < p:
        
        return True
    
    else:
        
        return False


def normalize_audio(data, samplerate, target_dBFS=-10.0):
    
    max_dBFS = get_max_db(data)
    
    gain_amt = target_dBFS - max_dBFS
    
    gain = pdlb.Gain(gain_amt)
    
    normalized_audio = gain(data, samplerate)
    
    return normalized_audio

def process(track_name, audio, sr, start = -1, end = -1, track_folder = ""):
    
    if track_name == "_master" and track_folder == "":
        
        track_cat = track_name
        
    else:

        track_cat = track_type_mapping(track_name, track_folder)

    if start != -1 and end != -1:

        cut_audio = tcu.cut_audio(audio, sr, start, end)
        
    else:
        
        cut_audio = audio
        
    if is_empty(cut_audio):
        
        print("empty file, skipping")
        
        return -1, -2
    
    if isinstance(audio, np.ndarray):

        norm_audio = normalize_audio(cut_audio, sr, -10)
        
    else:
        
        return -1, -2

    board = pu.generate_random_pdlb(track_cat)

    processed_audio = board(norm_audio, sr)

    return processed_audio, sr