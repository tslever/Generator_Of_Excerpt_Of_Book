import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Define parameters for the desired distribution
mode = 350
median = 550
mean = 750

# Generate a skewed normal distribution with skewness to the right
a = 4  # Skewness parameter for right skew
size = 10000  # Number of data points
base_data = stats.skewnorm.rvs(a, loc=0, scale=20, size=size)

# Estimate the mode of the base data using KDE
kde = stats.gaussian_kde(base_data)
x_vals = np.linspace(np.min(base_data), np.max(base_data), 1000)
kde_vals = kde(x_vals)
mode_estimate = x_vals[np.argmax(kde_vals)]

# Shift the data to set the mode at 80
shifted_data = base_data + (mode - mode_estimate)

# Calculate the current median and mean
current_median = np.median(shifted_data)
current_mean = np.mean(shifted_data)

# Scale the data around the mode to set the median at 550
scaling_factor = (median - mode) / (current_median - mode)
shifted_data = (shifted_data - mode) * scaling_factor + mode

# Adjust the mean to be 750
mean_adjustment = mean - np.mean(shifted_data)
shifted_data += mean_adjustment

# Re-estimate the mode
kde = stats.gaussian_kde(shifted_data)
x_vals = np.linspace(np.min(shifted_data), np.max(shifted_data), 1000)
kde_vals = kde(x_vals)
mode_estimate_final = x_vals[np.argmax(kde_vals)]

# Print the estimated mode, median, and mean
print("Estimated Mode:", mode_estimate_final)
print("Median:", np.median(shifted_data))
print("Mean:", np.mean(shifted_data))

# Plot the distribution
plt.figure(figsize=(10, 6))
plt.hist(shifted_data, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black')

# Add a KDE for a smooth curve
kde = stats.gaussian_kde(shifted_data)
x_vals = np.linspace(min(shifted_data), max(shifted_data), 1000)
plt.plot(x_vals, kde(x_vals), color='red', label='KDE')

# Add vertical lines for mode, median, and mean
plt.axvline(mode, color='green', linestyle='--', label=f'Mode = {mode}')
plt.axvline(median, color='blue', linestyle='--', label=f'Median = {median}')
plt.axvline(mean, color='purple', linestyle='--', label=f'Mean = {mean}')

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Right-Skewed Distribution with Mode = 350, Median = 550, and Mean = 750')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()