# ⚛️ Rutherford Scattering — Forward and Inverse Problem

Simulating alpha particles scattering off a gold nucleus with Monte Carlo methods 
and then running the experiment backwards: recovering an unknown element's atomic 
number Z from nothing but noisy measured angles.

## 🔬 Background

In 1909, Hans Geiger and Ernest Marsden, working in Rutherford's laboratory, fired alpha particles at thin metal foils, including gold. Most passed through with little deflection, but a tiny fraction scattered backwards by more than 90°. In 1911, Rutherford explained these surprising results by proposing that an atom's positive charge and most of its mass are concentrated in a tiny, dense nucleus.

The physics of a single particle is simple. A particle aimed with **impact parameter b** 
(its miss distance from the nucleus) is deflected by the angle:

**θ = 2 · arctan(a / b),  where  a = k · Z_alpha · Z · e² / (2E)**

- a larger Z or a lower energy E → a larger a → stronger scattering
- a large b → a gentle deflection, a small b → a violent one

**Monte Carlo idea:** a real beam is spread evenly over an area, so every particle gets 
a random impact parameter drawn uniformly over the beam's area (**b = b_max · √u**, 
with u uniform in [0, 1]). The angle distribution then emerges from many particles — 
the angle is never chosen, it is the *outcome*.

**Physical setup:** 5 MeV alpha particles on gold (Z = 79), lengths in femtometers:

- a ≈ 22.8 fm, so the closest approach head-on is 2a ≈ 45.5 fm
- the gold nucleus radius is ≈ 7.0 fm
- the alpha never reaches the nucleus → pure Coulomb (Rutherford) scattering is valid

## 📊 Results

### Forward Problem: Predicting the Scattering Distribution

![Rutherford Scattering](results/02_particle_scattering.png)

- 10,000 alpha particles on a gold nucleus
- **97.97%** scatter below 30° → most particles barely deflect
- Large-angle events are rare but not impossible (log scale)
- **Theory check:** a particle scatters beyond 90° exactly when b < a, so the expected 
  fraction is (a / b_max)². Simulation: **16 events** vs theory **16 ± 4** 
  (+0.1 std) → the simulation matches the exact result
- The ± is the typical random fluctuation of a count (1 standard deviation)

### Inverse Problem: Recovering Z from Noisy Angles

![Inverse Scattering](results/02_inverse_scattering.png)

- A mystery material (silver, Z = 47) is simulated and its Z is **hidden**
- Detector noise: Gaussian, 5°. The notebook also compares lower noise (1°) and higher noise (10°).
- The estimator only sees the measured angles — never the impact parameters, which no real experiment can measure
- **Method — simulation matching:**
  1. For every candidate Z (1 to 118), simulate the same experiment with the same 
     noise and record the median measured angle (a calibration curve)
  2. Take the median angle of the mystery data
  3. Pick the Z whose predicted median is closest
- Because the calibration includes the noise, the estimator is close to unbiased under the tested conditions

### How Reliable Is One Experiment?

![Distribution of the recovered Z](results/02_inverse_distribution.png)

- The experiment is repeated **500 times** and every recovered Z is collected
- The estimates are centered on the true Z (mean ≈ 47.05) with a spread of σ ≈ 0.76
- The red curve is a normal distribution **fitted** to the results, (mean and std taken 
  from the data) not predicted from theory
- In this run, 96% of experiments recovered Z within ±1
- These results are Monte Carlo estimates; changing the random seed or sample sizes can shift them slightly

### Effect of Detector Noise

| Detector Noise | Std of Recovered Z | Exactly Right | Within ±1 |
|---|---|---|---|
| 1° | 0.26 | 93% | 100% |
| 5° | 0.83 | 45% | 95% |
| 10° | 1.42 | 31% | 76% |

- Z is recovered well in the low-noise (1°) case and degrades as noise grows
- The typical deflection in this setup is only ≈ 6°, so 10° of noise is larger than 
  the signal itself — the method still works, with a visibly wider spread

## 🧪 Model Assumptions

- Point nucleus, infinitely heavy target (no recoil), non-relativistic, single scattering
- No electron screening and no energy loss in the foil
- Beam radius b_max is a toy choice (a / b_max ≈ 0.04), making large-angle events visible in a 10,000-particle simulation  
- This is not a realistic model of the beam geometry in an actual gold-foil experiment
- Detector noise is modeled as Gaussian on the measured angle, clipped to the physical range

## ✅ Tests

The simulation and estimator live in a module, `scattering.py`, covered by 8 pytest tests:

- **Physics helper** — a scales linearly with Z and inversely with energy
- **Physical range** — scattering angles stay between 0 and π, even with 10° noise
- **Reproducibility** — the same random seed gives identical angles
- **Theory check** — the fraction of particles beyond 90° matches (a / b_max)² within 4 std
- **Inverse problem** — Z is recovered within ±2 at 1° noise for Z = 30, 47, 79 and 100

## 🧠 Physics Concepts Demonstrated

- **Rutherford scattering** — deflection angle from the Coulomb force of a point nucleus
- **Monte Carlo sampling** — random impact parameters, uniform over the beam's area
- **Validation against theory** — simulated counts checked against an exact analytic result
- **Inverse problems** — inferring a hidden property (Z) from indirect, noisy measurements
- **Simulation-based estimation** — calibrating an estimator by simulating the experiment itself
- **Statistical uncertainty** — the spread of repeated estimates quantifies how far 
  a single measurement can be trusted
  
## 💡 Key Takeaways

- The forward model reproduces an exact analytic prediction within random fluctuation
- An honest inverse problem may only use what a detector can measure — using the true 
  impact parameters would give the right answer for any noise level, and prove nothing
- Reporting the **spread** of the estimate matters as much as the estimate itself
- Noise comparable to the typical deflection limits how precisely Z can be recovered

## 🌍 Real World Applications

The same forward-and-inverse logic is used in:
- Rutherford backscattering spectrometry — identifying elements in thin films
- Particle physics — inferring structure from scattering patterns
- Medical imaging — reconstructing the inside of the body from indirect measurements
- Geophysics — inferring Earth's structure from seismic signals

## 🛠️ Tech Stack

- Python 3.12, 3.13, and 3.14 (CI-tested)
- NumPy
- Matplotlib
- pytest
- Jupyter Notebook