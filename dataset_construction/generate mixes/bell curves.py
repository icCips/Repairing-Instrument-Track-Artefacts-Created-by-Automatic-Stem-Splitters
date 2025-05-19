import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

# Function to generate samples from a truncated normal distribution
def generate_truncated_normal(min_val, max_val, mean, std_dev, num_samples):
    # Calculate a, b to be used with truncnorm
    a, b = (min_val - mean) / std_dev, (max_val - mean) / std_dev
    truncated_normal = truncnorm(a, b, loc=mean, scale=std_dev)
    samples = truncated_normal.rvs(size=num_samples)
    return samples

# Parameters for the function
min_val, max_val, mean, std_dev = 1, 5, 1.5, 0.8

# Number of samples
num_samples = 1000000

# Generate samples
samples = generate_truncated_normal(min_val, max_val, mean, std_dev, num_samples)

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.hist(samples, bins=30, edgecolor='black', alpha=0.7)
plt.title('Histogram of Truncated Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
