import math
import matplotlib.pyplot as plt

# =========================================================
# PART A & B: DENSITY OF WATER
# =========================================================

# ---------- Raw lab data ----------
# Part A: 100 mL graduated cylinder (tare mass = 44.236 g)
cylinder_tare = 44.236
trial_A_mass = [52.684, 62.529, 73.183, 82.832, 92.878]
trial_A_vol  = [10.0, 20.0, 30.0, 40.0, 50.0]

# Part B: 50 mL beaker (tare mass = 29.150 g)
beaker_tare = 29.150
trial_B_mass = [40.096, 50.084, 60.016, 70.082, 80.001]
trial_B_vol  = [10.0, 20.0, 30.0, 40.0, 50.0]

true_density_water = 0.998  # accepted density of water near 21-22 C (g/mL)

# Recorded water temperature for each part
temperature_A = 21.5  # deg C
temperature_B = 22.0  # deg C

# ---------- Instrument uncertainties (used for error bars) ----------
balance_uncertainty = 0.001   # g, digital balance readability
cylinder_uncertainty = 0.1    # mL, graduated cylinder readability
beaker_uncertainty = 5.0      # mL, beaker readability (coarser graduations)


def calc_water_densities(masses, volumes, tare):
    densities = []
    for mass, vol in zip(masses, volumes):
        water_mass = mass - tare
        densities.append(water_mass / vol)
    return densities


def calc_water_density_errors(masses, volumes, tare, vol_uncertainty):
    """Propagate instrument uncertainty from mass and volume readings into
    an uncertainty on each calculated density value."""
    errors = []
    mass_diff_uncertainty = math.sqrt(balance_uncertainty ** 2 + balance_uncertainty ** 2)
    for mass, vol in zip(masses, volumes):
        water_mass = mass - tare
        density = water_mass / vol
        rel_mass_err = mass_diff_uncertainty / water_mass
        rel_vol_err = vol_uncertainty / vol
        rel_density_err = math.sqrt(rel_mass_err ** 2 + rel_vol_err ** 2)
        errors.append(density * rel_density_err)
    return errors


# =========================================================
# PART C: DENSITY OF A PENNY
# =========================================================

# ---------- Raw lab data (4 trials on the same penny) ----------
penny_diameter = [1.85, 1.85, 1.85, 1.85]   # cm
penny_edge     = [0.10, 0.10, 0.10, 0.10]   # cm (thickness)
penny_mass     = [2.508, 2.510, 2.512, 2.512]  # g

# Accepted density of a modern (post-1982) US penny: ~97.5% zinc core, 2.5% copper
# plating. Change this if your teacher wants pure copper (8.96 g/cm^3) instead.
true_density_penny = 7.14  # g/cm^3

# ---------- Instrument uncertainties (caliper + balance) ----------
caliper_uncertainty = 0.01   # cm, digital caliper readability (diameter & edge)


def calc_penny_densities(diameters, edges, masses):
    densities = []
    for d, h, m in zip(diameters, edges, masses):
        radius = d / 2
        volume = math.pi * (radius ** 2) * h  # cylinder volume
        densities.append(m / volume)
    return densities


def calc_penny_density_errors(diameters, edges, masses):
    errors = []
    for d, h, m in zip(diameters, edges, masses):
        radius = d / 2
        volume = math.pi * (radius ** 2) * h
        density = m / volume
        rel_diameter_err = caliper_uncertainty / d   # radius error scales the same way
        rel_edge_err = caliper_uncertainty / h
        rel_mass_err = balance_uncertainty / m
        # volume ~ d^2 * h, so the diameter term is doubled
        rel_density_err = math.sqrt((2 * rel_diameter_err) ** 2 + rel_edge_err ** 2 + rel_mass_err ** 2)
        errors.append(density * rel_density_err)
    return errors


# =========================================================
# PLOTTING (all three parts as one figure, three panels)
# =========================================================

def plot_density_bar(ax, densities, errors, true_density, title, bar_color):
    trial_labels = [f"Trial {i + 1}" for i in range(len(densities))]
    avg_density = sum(densities) / len(densities)

    bars = ax.bar(trial_labels, densities, yerr=errors, capsize=6,
                   color=bar_color, edgecolor="black", width=0.6,
                   error_kw={"ecolor": "black", "elinewidth": 1.5})

    # average and true density reference lines
    ax.axhline(avg_density, color="green", linestyle="--", linewidth=2,
               label=f"Average ({avg_density:.3f})")
    ax.axhline(true_density, color="red", linestyle="-", linewidth=2,
               label=f"True/accepted ({true_density:.3f})")

    # bar value labels (placed above the error bar cap)
    for bar, val, err in zip(bars, densities, errors):
        ax.text(bar.get_x() + bar.get_width() / 2, val + err + 0.01, f"{val:.3f}",
                 ha="center", va="bottom", fontsize=8)

    ax.set_xlabel("Trial")
    ax.set_ylabel("Density")
    ax.set_title(title, fontsize=10)
    ax.set_ylim(0, max(max(densities), true_density) + max(errors) + 0.5)
    ax.legend(fontsize=8)

    print(title)
    print("Densities:", densities)
    print("Error bars (+/-):", errors)
    print("Average density:", avg_density)
    print()


# ---- Compute all three parts ----
density_A = calc_water_densities(trial_A_mass, trial_A_vol, cylinder_tare)
error_A = calc_water_density_errors(trial_A_mass, trial_A_vol, cylinder_tare, cylinder_uncertainty)

density_B = calc_water_densities(trial_B_mass, trial_B_vol, beaker_tare)
error_B = calc_water_density_errors(trial_B_mass, trial_B_vol, beaker_tare, beaker_uncertainty)

density_C = calc_penny_densities(penny_diameter, penny_edge, penny_mass)
error_C = calc_penny_density_errors(penny_diameter, penny_edge, penny_mass)

# ---- One figure, three side-by-side panels ----
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

plot_density_bar(ax1, density_A, error_A, true_density_water,
                  f"Part A: Water (100 mL Cylinder) at {temperature_A}\u00b0C", "#4C72B0")
plot_density_bar(ax2, density_B, error_B, true_density_water,
                  f"Part B: Water (50 mL Beaker) at {temperature_B}\u00b0C", "#DD8452")
plot_density_bar(ax3, density_C, error_C, true_density_penny,
                  "Part C: Penny", "#55A868")

fig.suptitle("Measurements Lab: Density Results", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("density_bar_graphs_all.png", dpi=200)
plt.show()