import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson
from scipy.ndimage import gaussian_filter1d
from scipy.stats import lognorm, beta


def generate_youthful_curve(x, a=0.9585, b=-6.6757, c=0.0341):
    return a * np.exp(b * (x / 80)) + c

def generate_mature_curve(x, value=0.33):
    return np.full_like(x, value)

from scipy.stats import beta

def skewed_gaussian(x, mean, std_dev, skew_factor):
    # Generate a Gaussian curve and apply a skew factor to make it right-skewed
    gauss = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    skew = (1 - skew_factor * (x - mean) / std_dev)
    y = gauss * skew
    return y

def adjust_y_with_conditions(x, y, c=0.02, x_peak=30, decay_length=10):
    # Apply c when x < x_peak
    y[x < x_peak] += c

    # For x >= x_peak, apply a diminishing addition of c over the decay_length
    mask = (x >= x_peak) & (x <= x_peak + decay_length)
    diminishing_factor = 1 - ((x[mask] - x_peak) / decay_length)
    diminishing_factor = np.maximum(diminishing_factor, 0)  # Ensure no negative values

    y[mask] += c * diminishing_factor

    return y

def generate_maturing_curve(x, c=0.02, y_max=1.0, x_peak=30):
    # Generate skewed Gaussian curve for Type II maturing curve
    mean = x_peak  # Peak at x = 30
    std_dev = 10  # Standard deviation, adjust to control spread
    skew_factor = 0.25  # Adjust to control the amount of right skew

    y = skewed_gaussian(x, mean, std_dev, skew_factor)

    # Apply adjustment conditions
    y = adjust_y_with_conditions(x, y, c=c, x_peak=x_peak)

    # Normalize the curve to ensure it's comparable as proportions (set y at x=0 to c and y at x=80 to 0)
    y = y - np.min(y)  # Shift to start from 0
    y = y / np.max(y)  # Normalize to max value of 1
    y = y_max * y  # Scale to y_max

    # Apply smoothing to the final curve using Gaussian filter
    y_smoothed = gaussian_filter1d(y, sigma=2)  # Adjust sigma for more or less smoothing

    return y_smoothed




def plot_tree_population_curves():
    fig, ax = plt.subplots()

    x = np.linspace(0, 80, 300)

    # Type I (Youthful)
    y_youthful = generate_youthful_curve(x)
    y_youthful_normalized = y_youthful / simpson(y=y_youthful, x=x)
    ax.plot(x, y_youthful_normalized, lw=2, label='Youthful (Type I)', color='blue')

    # Type II (Maturing)
    y_maturing = generate_maturing_curve(x)
    y_maturing_normalized = y_maturing / simpson(y=y_maturing, x=x)
    ax.plot(x, y_maturing_normalized, lw=2, label='Maturing (Type II)', color='green')

    # Type III (Mature)
    y_mature = generate_mature_curve(x)
    y_mature_normalized = y_mature / simpson(y=y_mature, x=x)
    ax.plot(x, y_mature_normalized, lw=2, label='Mature (Type III)', color='red')

    # Labels, ticks, and formatting
    ax.set_xlabel('Diameter at Breast Height (cm)')
    ax.set_ylabel('Proportion of Tree Population')

    ax.set_xticks([0, 20, 40, 60, 80])
    ax.set_xticklabels(['0 cm', '20 cm', '40 cm', '60 cm', '80 cm'])

    ax.set_xlim(0, 80)

    ax.axvline(x=20, color='black', linestyle='--', lw=1)
    ax.axvline(x=40, color='black', linestyle='--', lw=1)
    ax.axvline(x=60, color='black', linestyle='--', lw=1)

    ax.text(10, 1.05, 'Young', horizontalalignment='center', fontsize=10)
    ax.text(30, 1.05, 'Semi-mature', horizontalalignment='center', fontsize=10)
    ax.text(50, 1.05, 'Mature', horizontalalignment='center', fontsize=10)
    ax.text(70, 1.05, 'Old', horizontalalignment='center', fontsize=10)

    ax.legend()

    plt.tight_layout()
    plt.savefig("plot.png", dpi=1200)
    fig.savefig('plot.svg', format='svg', dpi=1200)

plot_tree_population_curves()