"""
Model 1: ligand-receptor binding for PahP + PAHs
iGEM Saarland 2026

Input:  MM-GBSA binding free energies from 100 ns MD (this work)
Output: model1_binding.png
"""
import numpy as np
import matplotlib.pyplot as plt

RT = 0.001987 * 310.0

MMGBSA = {"pyrene": (-13.88, 4.21), "phenanthrene": (-18.12, 4.41)}
VINA = {"pyrene": -8.02, "phenanthrene": -7.45, "naphthalene": -6.05}

def kd_nM(dg):
    return np.exp(dg / RT) * 1e9

print("MM-GBSA free energies -> Kd   (RT = %.3f kcal/mol at 310 K)\n" % RT)
print(f"{'ligand':<15}{'dG':>8}{'Kd (nM)':>13}{'-1 SD':>13}{'+1 SD':>13}")
for lig, (dg, sd) in MMGBSA.items():
    print(f"{lig:<15}{dg:>8.2f}{kd_nM(dg):>13.2e}{kd_nM(dg-sd):>13.2e}{kd_nM(dg+sd):>13.2e}")

dg, sd = MMGBSA["pyrene"]
print(f"\nThe +/- 1 SD window spans {kd_nM(dg+sd)/kd_nM(dg-sd):.0e}-fold in Kd.")
print("MM-GBSA omits configurational entropy, so these absolute values")
print("overestimate affinity. They are used below as a RANKING; the curves")
print("are drawn over a plausible Kd range instead of a single value.\n")

L = np.logspace(-2, 6, 400)

def theta(L, Kd):
    return L / (Kd + L)

fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))

for Kd in [1, 10, 100, 1000, 10000]:
    ax[0].semilogx(L, theta(L, Kd), label=f"Kd = {Kd:g} nM")
ax[0].axhspan(0.1, 0.9, color="grey", alpha=0.10)
ax[0].text(3e-2, 0.5, "useful\nworking\nrange", fontsize=8, va="center")
ax[0].set(xlabel="free PAH (nM)", ylabel="fraction of receptor bound",
          title="(a) Dose-response vs Kd", ylim=(0, 1))
ax[0].legend(fontsize=8)
ax[0].grid(alpha=0.3)

kd_axis = np.logspace(0, 5, 200)
ax[1].loglog(kd_axis, kd_axis / 9, "k-", lw=2)
ax[1].axhspan(1e-3, 4, color="tab:green", alpha=0.15)
ax[1].text(1.5, 1.3, "typical surface-water\nPAH levels", fontsize=8)
ax[1].set(xlabel="Kd (nM)", ylabel="[PAH] giving 10% occupancy (nM)",
          title="(b) What Kd does the sensor need?")
ax[1].grid(alpha=0.3, which="both")

dg_axis = np.linspace(-20, -5, 200)
ax[2].semilogy(dg_axis, kd_nM(dg_axis), "k-", lw=1)
for lig, colour in [("pyrene", "tab:blue"), ("phenanthrene", "tab:orange")]:
    d, s = MMGBSA[lig]
    ax[2].errorbar(d, kd_nM(d),
                   yerr=[[kd_nM(d) - kd_nM(d - s)], [kd_nM(d + s) - kd_nM(d)]],
                   fmt="o", color=colour, capsize=4, label=f"{lig} MM-GBSA")
for lig, colour in [("pyrene", "tab:blue"), ("phenanthrene", "tab:orange"),
                    ("naphthalene", "tab:green")]:
    ax[2].plot(VINA[lig], kd_nM(VINA[lig]), "s", mfc="none", color=colour,
               label=f"{lig} Vina")
ax[2].set(xlabel="binding free energy (kcal/mol)", ylabel="Kd (nM)",
          title="(c) Both methods on one axis")
ax[2].legend(fontsize=7)
ax[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("model1_binding.png", dpi=150)
print("wrote model1_binding.png\n")

print("Time to equilibrium (k_on = 1e-5 nM^-1 s^-1, slow hydrophobic binder):")
print(f"{'Kd (nM)':>9}{'[L] (nM)':>10}{'tau':>12}{'~95% eq':>12}")
kon = 1e-5
for Kd in [1, 100, 1000]:
    for conc in [1, 100]:
        tau = 1.0 / (kon * conc + Kd * kon)
        print(f"{Kd:>9g}{conc:>10g}{tau/60:>9.1f} min{3*tau/60:>9.1f} min")

print("\nTight binders at low concentration equilibrate over hours; at Kd ~1 uM")
print("it is minutes. The reporter chain (Model 2) adds hours on top, so it")
print("usually sets the overall response time, not the binding step.")
