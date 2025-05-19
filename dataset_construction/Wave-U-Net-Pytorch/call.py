import subprocess

def predict(input_path, output_path):
    subprocess.run([
        "python3", "predict.py",
        "--load_model", "checkpoints/waveunet/model",
        "--input", input_path,
        "--output", output_path
    ])