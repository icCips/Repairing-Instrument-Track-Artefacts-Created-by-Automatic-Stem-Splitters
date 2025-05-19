import pedalboard as pdlb
import random as r
import csv
from scipy.stats import truncnorm

def generate_truncated_normal(min_val, max_val, mean, std_dev):
    a, b = (min_val - mean) / std_dev, (max_val - mean) / std_dev
    truncated_normal = truncnorm(a, b, loc=mean, scale=std_dev)
    sample = truncated_normal.rvs()
    return sample

def remove_random_elements(lst):
    # Get the length of the list
    n = len(lst)
    
    # Generate a random number of elements to remove (between 0 and n-1)
    num_to_remove = r.randint(0, n-1)
    
    # Get a random sample of indices to remove
    indices_to_remove = r.sample(range(n), num_to_remove)
    
    # Create a new list excluding the elements at the chosen indices
    new_lst = [lst[i] for i in range(n) if i not in indices_to_remove]
    
    return new_lst

# fx

def gate(fx):
    
    thresh = generate_truncated_normal(-50, -20, -40, 10)
    ratio = generate_truncated_normal(8, 12, 10, 1)
    attack = generate_truncated_normal(0.01, 10, 2, 1)
    release = generate_truncated_normal(10, 200, 80, 35)
    
    fx.append(pdlb.NoiseGate(threshold_db=thresh, ratio=ratio, attack_ms=attack, release_ms=release))

#VST3
def invert(fx):
    
    util_phase = pdlb.load_plugin("generate mixes/plugins/MUtility.vst3")

    util_phase.invert_left_channel_basic = True
    util_phase.invert_right_channel_basic = True
    
    fx.append(util_phase)

def pitchshift(fx):
    semitones = generate_truncated_normal(-12, 12, 0, 5)
    fx.append(pdlb.PitchShift())

def hpf(fx):
    cutoff = generate_truncated_normal(50, 500, 150, 100)
    fx.append(pdlb.HighpassFilter(cutoff_frequency_hz=cutoff))

def high_shelf(fx):
    
    freq = generate_truncated_normal(2000, 4000, 3000, 900)
    q = generate_truncated_normal(0.1, 10, 0.8, 3)
    gain = generate_truncated_normal(-6, 6, 0, 8)
    
    fx.append(pdlb.HighShelfFilter(cutoff_frequency_hz=freq, q=q, gain_db=gain))

def high_mid(fx):
    
    freq = r.randrange(2000, 4000)
    gain = generate_truncated_normal(-6, 6, 0, 6)
    q = generate_truncated_normal(0.1, 10, 0.8, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def mid(fx):
    
    freq = r.randrange(800, 2000)
    gain = generate_truncated_normal(-6, 6, 0, 6)
    q = generate_truncated_normal(0.1, 10, 0.8, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def low_mid(fx):
    
    freq = r.randrange(300, 800)
    gain = generate_truncated_normal(-6, 6, 0, 6)
    q = generate_truncated_normal(0.1, 10, 0.8, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def lpf(fx):
    cutoff = generate_truncated_normal(3000, 10000, 5300, 900)
    fx.append(pdlb.LowpassFilter(cutoff_frequency_hz=cutoff))


def low_shelf(fx):
    
    freq = generate_truncated_normal(100, 300, 200, 100)
    q = generate_truncated_normal(0.1, 10, 0.8, 3)
    gain = generate_truncated_normal(-6, 6, 0, 8)
    
    fx.append(pdlb.HighShelfFilter(cutoff_frequency_hz=freq, q=q, gain_db=gain))

def soft_comp(fx):
    
    thresh = generate_truncated_normal(-40, -12, -30, 7)
    ratio = generate_truncated_normal(1, 5, 2, 1)
    attack = generate_truncated_normal(1, 30, 15, 6)
    release = generate_truncated_normal(10, 200, 120, 35)
    
    fx.append(pdlb.Compressor(threshold_db=thresh, ratio=ratio, attack_ms=attack, release_ms=release))
    
    fx.append(pdlb.Gain(2))
    
def hard_comp(fx):
    
    thresh = generate_truncated_normal(-40, -12, -30, 7)
    ratio = generate_truncated_normal(4, 10, 5, 2)
    attack = generate_truncated_normal(0.01, 10, 2, 1)
    release = generate_truncated_normal(10, 200, 40, 35)
    
    fx.append(pdlb.Compressor(threshold_db=thresh, ratio=ratio, attack_ms=attack, release_ms=release))
    
    fx.append(pdlb.Gain(4))

def dist(fx):
    drive = generate_truncated_normal(0.1, 0.9, 0.5, 0.12)
    fx.append(pdlb.Distortion(drive_db=drive))


def clipping(fx):
    thresh = generate_truncated_normal(-25, -11, -15, 3)
    fx.append(pdlb.Clipping(threshold_db=thresh))


#VST3  
def saturator(fx):
    
    saturator = pdlb.load_plugin("generate mixes/plugins/MSaturator.vst3")
    
    saturator.gain = generate_truncated_normal(5, 24, 15, 5)
    saturator.output_gain = -(saturator.gain)
    
    fx.append(saturator)
    
def gain_plus(fx):
    gain = generate_truncated_normal(0, 10, 6, 2)
    fx.append(pdlb.Gain(gain_db=gain))
    
def gain_minus(fx):
    gain = generate_truncated_normal(-12, 0, -6 ,2)
    fx.append(pdlb.Gain(gain_db=gain))

def chorus(fx):
    rate = generate_truncated_normal(0.1, 10, 1.5, 2)
    depth = generate_truncated_normal(0.1, 1, 0.3, 0.2)
    centre_delay = generate_truncated_normal(0, 14, 7, 1)
    feedback = generate_truncated_normal(0, 1, 0, 0.2)
    mix = generate_truncated_normal(0.15, 0.5, 0.3, 0.063)
    fx.append(pdlb.Chorus(rate_hz=rate, depth=depth, centre_delay_ms=centre_delay, feedback=feedback, mix=mix))


def phaser(fx):
    rate = generate_truncated_normal(0.1, 10, 1.5, 2)
    depth = generate_truncated_normal(0.1, 1, 0.3, 0.2)
    centre_freq = generate_truncated_normal(800, 2000, 1300, 180)
    feedback = generate_truncated_normal(0, 1, 0, 0.2)
    mix = generate_truncated_normal(0.15, 0.5, 0.3, 0.063)
    fx.append(pdlb.Phaser(rate_hz=rate, depth=depth, centre_frequency_hz=centre_freq, feedback=feedback, mix=mix))


#VST3
def tremolo(fx):
    
    trem = pdlb.load_plugin("generate mixes/plugins/MTremolo.vst3")
        
    trem.depth = generate_truncated_normal(20, 100, 75, 30)
    trem.rate = generate_truncated_normal(0.2, 10, 1, 2)
    
    fx.append(trem)

#VST3      
def autopan(fx):
    
    autopan = pdlb.load_plugin("generate mixes/plugins/MAutopan.vst3")
    
    autopan.depth = generate_truncated_normal(20, 100, 75, 30)
    autopan.rate = generate_truncated_normal(0.2, 10, 1, 2)
    
    fx.append(autopan)

#VST3
def vibrato(fx):
    
    vibrato = pdlb.load_plugin("generate mixes/plugins/MVibrato.vst3")
    
    vibrato.depth = generate_truncated_normal(1, 40, 15, 5)
    vibrato.rate = generate_truncated_normal(0.2, 10, 1, 2)
    
    fx.append(vibrato)

def delay(fx):
    delay = generate_truncated_normal(0.1, 3, 0.2, 0.3)
    feedback = generate_truncated_normal(0, 1, 0.3, 0.2)
    mix = generate_truncated_normal(0.15, 0.5, 0.3, 0.063)
    fx.append(pdlb.Delay(delay_seconds=delay, feedback=feedback, mix=mix))


def reverb_short(fx):
    
    size = generate_truncated_normal(0, 0.5, 0.15, 0.1)
    damping = generate_truncated_normal(0.5, 1, 0.8, 0.15)
    wet = generate_truncated_normal(0.15, 0.4, 0.25, 0.063)
    dry = wet + 0.5
    width = generate_truncated_normal(0, 1, 0.4, 0.25)
    
    fx.append(pdlb.Reverb(room_size=size, damping=damping, wet_level=wet, dry_level=dry, width=width))

def reverb_long(fx):
    
    size = generate_truncated_normal(0.4, 1, 0.6, 0.2)
    damping = generate_truncated_normal(0, 0.5, 0.4, 0.15)
    wet = generate_truncated_normal(0.15, 0.5, 0.3, 0.063)
    dry = wet + 0.4
    width = generate_truncated_normal(0, 1, 0.6, 0.25)
    
    fx.append(pdlb.Reverb(room_size=size, damping=damping, wet_level=wet, dry_level=dry, width=width))

#VST3
def pan(fx):
    
    util_pan = pdlb.load_plugin("generate mixes/plugins/MUtility.vst3")
    
    pan_percent = generate_truncated_normal(0, 100, 60 ,40)
    
    l_r = r.random()
    
    if l_r <= 0.5:
        
        pan = f'{round(pan_percent)}% left'
    
    else:
        
        pan = f'{round(pan_percent)}% right'
    
    util_pan.panorama_basic = pan
    
    fx.append(util_pan)

def limit(fx):
    
    thresh = generate_truncated_normal(-18, -10, -12, 3)
    release = generate_truncated_normal(0.01, 10, 0.1, 0.063)
    
    fx.append(pdlb.Limiter(threshold_db=thresh, release_ms=release))

def m_lo(fx):
    
    freq = r.randrange(60, 300)
    gain = generate_truncated_normal(-1.5, 1.5, 0, 0.4)
    q = generate_truncated_normal(0.4, 10, 2.5, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def m_lm(fx):
    
    freq = r.randrange(300, 800)
    gain = generate_truncated_normal(-1.5, 1.5, 0, 0.4)
    q = generate_truncated_normal(0.4, 10, 2.5, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def m_m(fx):
    
    freq = r.randrange(800, 2000)
    gain = generate_truncated_normal(-1.5, 1.5, 0, 0.4)
    q = generate_truncated_normal(0.4, 10, 2.5, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def m_hm(fx):
    
    freq = r.randrange(2000, 4000)
    gain = generate_truncated_normal(-1.5, 1.5, 0, 0.4)
    q = generate_truncated_normal(0.4, 10, 2.5, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def m_hi(fx):
    
    freq = r.randrange(4000, 8000)
    gain = generate_truncated_normal(-1.5, 1.5, 0, 0.4)
    q = generate_truncated_normal(0.4, 10, 2.5, 0.8)
    
    fx.append(pdlb.PeakFilter(cutoff_frequency_hz=freq, gain_db=gain, q=q))

def m_comp(fx):
    
    thresh = generate_truncated_normal(-13, -11, -11.7, 0.8)
    ratio = generate_truncated_normal(1, 5, 1.5, 0.8)
    attack = generate_truncated_normal(1, 30, 15, 6)
    release = generate_truncated_normal(10, 200, 120, 35)
    
    fx.append(pdlb.Compressor(threshold_db=thresh, ratio=ratio, attack_ms=attack, release_ms=release))

effects_functions = {
    "gate": gate,
    "invert": invert,
    "pitchshift": pitchshift,
    "hpf": hpf,
    "high_shelf": high_shelf,
    "high_mid": high_mid,
    "mid": mid,
    "low_mid": low_mid,
    "lpf": lpf,
    "low_shelf": low_shelf,
    "soft_comp": soft_comp,
    "hard_comp": hard_comp,
    "dist": dist,
    "clipping": clipping,
    "saturator": saturator,
    "gain_plus": gain_plus,
    "gain_minus": gain_minus,
    "chorus": chorus,
    "phaser": phaser,
    "tremolo": tremolo,
    "autopan": autopan,
    "vibrato": vibrato,
    "delay": delay,
    "reverb_short": reverb_short,
    "reverb_long": reverb_long,
    "pan": pan,
    "limit": limit,
    "m_lo": m_lo,
    "m_lm": m_lm,
    "m_m": m_m,
    "m_hm": m_hm,
    "m_hi": m_hi,
    "m_comp": m_comp
}


def read_csv_to_adjacency_list(csv_file_path):
    adjacency_list = {}
    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        
        # Extract the header row (column names)
        column_names = next(csv_reader)[1:]  # Skip the first cell and take the rest as column names
        
        # Initialize the dictionary with empty lists
        for column_name in column_names:
            adjacency_list[column_name] = []
        
        # Iterate over the rest of the rows
        for row in csv_reader:
            row_name = row[0]  # The first cell in the row is the row name
            values = row[1:]   # The rest are the 'x' marks
            
            for col_name, value in zip(column_names, values):
                if value == 'x':
                    # Append the corresponding function object to the list
                    adjacency_list[col_name].append(effects_functions[row_name])
    
    return adjacency_list

fx_map = read_csv_to_adjacency_list("generate mixes/data/fx.csv")

print("effect map loaded")

def generate_random_pdlb(inst_cat):
    
    fx = pdlb.Pedalboard()
    
    fx_list = fx_map[inst_cat]
    
    dropped_list = remove_random_elements(fx_list)
    
    for f in dropped_list:
        
        f(fx)
    
    return fx