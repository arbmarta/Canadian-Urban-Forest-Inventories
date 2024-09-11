import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


def plot_tree_population_curves():
    fig, ax = plt.subplots()

    x = np.linspace(0, 80, 100)

    # Type I (Youthful)
    y_youthful = 0.9585 * np.exp(-6.6757 * (x / 80)) + 0.0341  # Adjusting for new x scale
    ax.plot(x, y_youthful, lw=2, label='Youthful (Type I)', color='blue')

    x_sampled = np.array([
        0, 4.77, 10.44, 15.04, 18.26, 22.79, 30.61, 45.18, 59.09, 80
    ])

    y_sampled = np.array([
        0.5286624181536111, 0.658174130721433, 0.7091295213343511, 0.6454352393328243,
        0.5286624181536111, 0.3736730977500888, 0.22717625497796085, 0.11677287949305219,
        0.05944804318582957, 0.029724079906753857
    ])

    # Type II

    x_spline = np.linspace(min(x_sampled), max(x_sampled), 300)  # Generate more x values for a smooth curve
    spline = make_interp_spline(x_sampled, y_sampled, k=3)  # Cubic spline (k=3)
    y_spline = spline(x_spline)

    ax.plot(x_spline, y_spline, lw=2, label='Maturing (Type II)', color='green')

    # Type III (Mature)
    y_mature = np.full_like(x, 0.5)
    ax.plot(x, y_mature, lw=2, label='Mature (Type III)', color='red')

    ax.set_xlabel('Diameter at Breast Height (cm)')
    ax.set_ylabel('Proportion of Tree Population')

    ax.set_xticks([0, 20, 40, 60, 80])
    ax.set_xticklabels(['0 cm', '20 cm', '40 cm', '60 cm', '80 cm'])

    ax.set_yticks([0, 1])
    ax.set_yticklabels(['', ''])

    ax.set_xlim(0, 80)
    ax.set_ylim(0, 1)

    ax.axvline(x=20, color='black', linestyle='--', lw=1)
    ax.axvline(x=40, color='black', linestyle='--', lw=1)
    ax.axvline(x=60, color='black', linestyle='--', lw=1)

    ax.text(10, 1.05, 'Young', horizontalalignment='center', fontsize=10)
    ax.text(30, 1.05, 'Semi-mature', horizontalalignment='center', fontsize=10)
    ax.text(50, 1.05, 'Mature', horizontalalignment='center', fontsize=10)
    ax.text(70, 1.05, 'Old', horizontalalignment='center', fontsize=10)

    ax.legend()

    plt.savefig("plot.png", dpi=1200)
    fig.savefig('plot.svg', format='svg', dpi=1200)


plot_tree_population_curves()
