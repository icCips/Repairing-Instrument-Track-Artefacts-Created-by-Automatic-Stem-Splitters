import subprocess

def predict(input_path, output_path):
    
    subprocess.run([
        "python3", "dataset_construction/Wave_U_Net_Pytorch/predict.py",
        "--load_model", "dataset_construction/Wave_U_Net_Pytorch/checkpoints/waveunet/model",
        "--input", input_path,
        "--output", output_path
    ])