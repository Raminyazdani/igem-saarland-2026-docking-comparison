"""Model 2 - signal to reporter output, CFP/YFP FRET sensor in E. coli.

Input:  illustrative Kd ladder (same as Model 3), literature-order expression
        and maturation rates. No fitted parameters - this is a structural model
        of the reporter chain, not a calibration.
Output: model2_reporter.png
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import odeint

KD = {"pyrene": 100.0, "phenanthrene": 300.0, "naphthalene": 5000.0}
ALPHA, DELTA_M = 1.0, np.log(2) / 5          # mRNA synthesis, 5 min half-life
BETA = 2.0                                    # protein per mRNA per min
K_MAT = np.log(2) / 30                        # 30 min YFP maturation half-life
MU0, NMAX = np.log(2) / 40, 1.0               # 40 min doubling, logistic cap
DELTA_P, BASAL = np.log(2) / (24 * 60), 0.02  # 24 h sensor turnover; stationary promoter floor
KON = 6e-4                                    # nM^-1 min^-1 (1e-5 nM^-1 s^-1)
R_FREE, R_BOUND = 1.00, 1.60                  # FRET ratio, apo and holo
READ_T = 20 * 60                              # wet-lab reading at 20 h

def expression(y, t):
    N, m, I, S = y
    mu = MU0 * (1 - N / NMAX)
    a = ALPHA * (BASAL + (1 - BASAL) * mu / MU0)
    return [mu * N, a - DELTA_M * m, BETA * m - (K_MAT + mu + DELTA_P) * I,
            K_MAT * I - (mu + DELTA_P) * S]

t = np.linspace(0, 24 * 60, 2000)
N, m, I, S = odeint(expression, [0.01, 0, 0, 0], t).T
frac = S / S.max()
tpk = t[np.argmax(S)] / 60
print(f"sensor peaks at {tpk:.1f} h; at 20 h it is {np.interp(READ_T, t, frac)*100:.1f}% of peak")

def ratio(L, kd):
    return R_FREE + (R_BOUND - R_FREE) * L / (kd + L)

print(f"\nFRET ratio at 20 h (ratiometric, independent of sensor level)")
print(f"{'ligand':<15}{'Kd (nM)':>9}{'20 nM':>9}{'100 nM':>9}{'1 uM':>9}")
for lig, kd in KD.items():
    print(f"{lig:<15}{kd:>9.0f}{ratio(20,kd):>9.3f}{ratio(100,kd):>9.3f}{ratio(1000,kd):>9.3f}")

print("\nsignal at the top of the typical surface-water range (4 nM):")
for lig, kd in KD.items():
    r = ratio(4, kd)
    print(f"  {lig:<14} ratio {r:.4f}  ({100*(r-R_FREE)/(R_BOUND-R_FREE):.1f}% of full scale)")
print("Kd would need to be ~4 nM for half-maximal signal at that concentration.")

def step_response(L, kd, tt):
    kobs = KON * L + KON * kd
    return 1 - np.exp(-kobs * tt)

tt = np.linspace(0, 120, 400)
print(f"\ntime to 95% of new ratio after a pollutant step at 20 h")
for lig, kd in KD.items():
    for L in (20, 200):
        tau = 1 / (KON * L + KON * kd)
        print(f"  {lig:<14} [L]={L:>4} nM   tau {tau:>5.1f} min   95% {3*tau:>5.1f} min")

fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
ax[0].plot(t / 60, frac, "k-", lw=2, label="mature sensor")
ax[0].plot(t / 60, I / S.max(), color="0.6", lw=1, label="immature")
ax[0].axvline(20, ls=":", color="#b00020")
ax[0].text(20.3, 0.25, "wet-lab read\n20 h", fontsize=8, color="#b00020")
ax[0].set(xlabel="time after induction (h)", ylabel="fraction of peak",
          title="(a) Sensor accumulation", xlim=(0, 24), ylim=(0, 1.05))
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)

L = np.logspace(-1, 5, 400)
for lig, kd in KD.items():
    ax[1].semilogx(L, ratio(L, kd), label=f"{lig} (Kd {kd:g} nM)")
ax[1].axvspan(1e-3, 4, color="tab:green", alpha=0.15)
ax[1].text(0.15, 1.52, "typical surface-water\nPAH levels", fontsize=8)
ax[1].set(xlabel="free PAH (nM)", ylabel="YFP/CFP ratio",
          title="(b) Dose-response at 20 h", ylim=(0.98, 1.65))
ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3, which="both")

for lig, kd in KD.items():
    ax[2].plot(tt, step_response(20, kd, tt), label=f"{lig}, 20 nM")
ax[2].axhline(0.95, ls="--", lw=0.9, color="0.35")
ax[2].text(118, 0.90, "95%", fontsize=8, ha="right", color="0.35")
ax[2].set(xlabel="time after pollutant step (min)", ylabel="approach to new ratio",
          title="(c) Response time, sensor already expressed", ylim=(0, 1.02))
ax[2].legend(fontsize=8); ax[2].grid(alpha=0.3)

fig.tight_layout()
fig.savefig("model2_reporter.png", dpi=200)
print("\nwrote model2_reporter.png")
print("The ratio in (b) does not depend on sensor concentration, so the 20 h wait")
print("sets signal-to-noise, not the measured value. Once expressed, the sensor")
print("tracks a change in pollutant within an hour - the slow step is expression,")
print("which happens once, not the binding, which happens on every reading.")
