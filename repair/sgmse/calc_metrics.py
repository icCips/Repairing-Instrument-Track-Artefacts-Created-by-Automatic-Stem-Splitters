from os.path import join, exists
from glob import glob
from argparse import ArgumentParser
from soundfile import read
from tqdm import tqdm
import pandas as pd
import librosa

from sgmse.util.other import energy_ratios, mean_std

if __name__ == '__main__':
    print("no stoi")
    
    parser = ArgumentParser()
    parser.add_argument("--clean_dir", type=str, required=True, help='Directory containing the clean data')
    parser.add_argument("--noisy_dir", type=str, required=True, help='Directory containing the noisy data')
    parser.add_argument("--enhanced_dir", type=str, required=True, help='Directory containing the enhanced data')
    args = parser.parse_args()

    data = {"filename": [], "si_sdr": [], "si_sir": [],  "si_sar": []}

    # Evaluate standard metrics
    noisy_files = []
    noisy_files += sorted(glob(join(args.noisy_dir, '*.wav')))
    noisy_files += sorted(glob(join(args.noisy_dir, '**', '*.wav')))
    for noisy_file in tqdm(noisy_files):
        filename = noisy_file.replace(args.noisy_dir, "")[1:]
        if 'dB' in filename:
            clean_filename = filename.split("_")[0] + ".wav"
        else:
            clean_filename = filename

        clean_path = join(args.clean_dir, clean_filename)
        enhanced_path = join(args.enhanced_dir, filename)

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
        x_hat_16k = librosa.resample(x_hat, orig_sr=sr_x_hat, target_sr=16000) if sr_x_hat != 16000 else x_hat
        x_16k = librosa.resample(x, orig_sr=sr_x, target_sr=16000) if sr_x != 16000 else x
        data["filename"].append(filename)
        data["si_sdr"].append(energy_ratios(x_hat, x, n)[0])
        data["si_sir"].append(energy_ratios(x_hat, x, n)[1])
        data["si_sar"].append(energy_ratios(x_hat, x, n)[2])

    # Save results as DataFrame    
    df = pd.DataFrame(data)

    # Print results
    print("SI-SDR: {:.1f} ± {:.1f}".format(*mean_std(df["si_sdr"].to_numpy())))
    print("SI-SIR: {:.1f} ± {:.1f}".format(*mean_std(df["si_sir"].to_numpy())))
    print("SI-SAR: {:.1f} ± {:.1f}".format(*mean_std(df["si_sar"].to_numpy())))

    # Save average results to file
    log = open(join(args.enhanced_dir, "_avg_results.txt"), "w")
    log.write("SI-SDR: {:.1f} ± {:.2f}".format(*mean_std(df["si_sdr"].to_numpy())) + "\n")
    log.write("SI-SIR: {:.1f} ± {:.1f}".format(*mean_std(df["si_sir"].to_numpy())) + "\n")
    log.write("SI-SAR: {:.1f} ± {:.1f}".format(*mean_std(df["si_sar"].to_numpy())) + "\n")

    # Save DataFrame as csv file
    df.to_csv(join(args.enhanced_dir, "_results.csv"), index=False)