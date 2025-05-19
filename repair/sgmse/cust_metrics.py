from os.path import join, exists
from glob import glob
from soundfile import read
from tqdm import tqdm
import pandas as pd
import librosa

from sgmse.util.other import energy_ratios, mean_std

# Set your paths here
clean_dir = "datasets/sgmse_vocal_16kHz_5s_chunks/test/clean"
noisy_dir = "datasets/sgmse_vocal_16kHz_5s_chunks/test/noisy"
enhanced_dir = "datasets/enhanced_vocal"

data = {
    "filename": [],
    "si_sdr_noisy": [], "si_sir_noisy": [], "si_sar_noisy": [], "si_snr_noisy": [],
    "si_sdr_enhanced": [], "si_sir_enhanced": [], "si_sar_enhanced": [], "si_snr_enhanced": []
}

# Evaluate metrics
noisy_files = []
noisy_files += sorted(glob(join(noisy_dir, '*.wav')))
noisy_files += sorted(glob(join(noisy_dir, '**', '*.wav')))
for noisy_file in tqdm(noisy_files):
    filename = noisy_file.replace(noisy_dir, "")[1:]
    if 'dB' in filename:
        clean_filename = filename.split("_")[0] + ".wav"
    else:
        clean_filename = filename

    clean_path = join(clean_dir, clean_filename)
    enhanced_path = join(enhanced_dir, filename)

    if not exists(clean_path):
        print(f"Clean file missing: {clean_path}")
        continue
    if not exists(enhanced_path):
        print(f"Enhanced file missing: {enhanced_path}")
        continue

    x, sr_x = read(clean_path)
    y, sr_y = read(noisy_file)
    x_hat, sr_x_hat = read(enhanced_path)

    assert sr_x == sr_y == sr_x_hat
    n = y - x

    # Resample to 16 kHz if needed
    x_16k = librosa.resample(x, orig_sr=sr_x, target_sr=16000) if sr_x != 16000 else x
    y_16k = librosa.resample(y, orig_sr=sr_y, target_sr=16000) if sr_y != 16000 else y
    x_hat_16k = librosa.resample(x_hat, orig_sr=sr_x_hat, target_sr=16000) if sr_x_hat != 16000 else x_hat

    # Compute metrics
    data["filename"].append(filename)

    si_sdr_n, si_sir_n, si_sar_n, si_snr_n = energy_ratios(y, x, n)
    si_sdr_e, si_sir_e, si_sar_e, si_snr_e = energy_ratios(x_hat, x, n)

    data["si_sdr_noisy"].append(si_sdr_n)
    data["si_sir_noisy"].append(si_sir_n)
    data["si_sar_noisy"].append(si_sar_n)
    data["si_snr_noisy"].append(si_snr_n)

    data["si_sdr_enhanced"].append(si_sdr_e)
    data["si_sir_enhanced"].append(si_sir_e)
    data["si_sar_enhanced"].append(si_sar_e)
    data["si_snr_enhanced"].append(si_snr_e)

# Save results as DataFrame
df = pd.DataFrame(data)

# Print results
for metric in ["si_sdr", "si_sir", "si_sar", "si_snr"]:
    print(f"Noisy {metric.upper()}: {{:.1f}} ± {{:.1f}}".format(*mean_std(df[f"{metric}_noisy"].to_numpy())))
    print(f"Enhanced {metric.upper()}: {{:.1f}} ± {{:.1f}}".format(*mean_std(df[f"{metric}_enhanced"].to_numpy())))

# Save average results to file
with open(join(enhanced_dir, "_avg_results.txt"), "w") as log:
    for metric in ["si_sdr", "si_sir", "si_sar", "si_snr"]:
        log.write(f"Noisy {metric.upper()}: {{:.1f}} ± {{:.1f}}\n".format(*mean_std(df[f"{metric}_noisy"].to_numpy())))
        log.write(f"Enhanced {metric.upper()}: {{:.1f}} ± {{:.1f}}\n".format(*mean_std(df[f"{metric}_enhanced"].to_numpy())))

# Save DataFrame as csv file
df.to_csv(join(enhanced_dir, "_results.csv"), index=False)