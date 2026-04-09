# Lennard-Jones Molecular Dynamics Simulation

2D molecular dynamics simulation of particles interacting via the Lennard-Jones potential.
Built for the Particle Methods course, Spring 2026, USI.

## What it does

Simulates N particles bouncing around a 2D square box, attracting and repelling each other
according to the Lennard-Jones potential — the same model used to describe noble gases like Argon.

Two modes:
- **NVE** — fixed number of particles, volume, and energy. No temperature control.
- **NVT** — fixed temperature, controlled by a Berendsen thermostat.

## Project structure

```
├── simulation/
│   ├── state.py        # particle data: positions, velocities, forces
│   ├── init.py         # place particles on a lattice, assign random velocities
│   ├── grid.py         # cell list — finds nearby particle pairs efficiently
│   ├── forces.py       # Lennard-Jones force and potential energy
│   ├── integrator.py   # velocity-Verlet time integration
│   └── thermostat.py   # Berendsen thermostat for temperature control
├── utils/
│   ├── config.py       # simulation parameters
│   └── recorder.py     # track energy, temperature, momentum over time
├── rdf.py              # radial distribution function g(r)
└── main.py             # run NVE and NVT simulations, save plots
```

## Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

Run all simulations (NVE part a + NVT part b):
```bash
python main.py
```

Outputs are saved under `output/nve/`, `output/nvt/`, and `output/animations/`.

## Cases

**Part a — NVE, no thermostat:**

| Case | N | dt |
|------|---|----|
| 1 | 100 | 0.01 |
| 2 | 100 | 0.005 |
| 3 | 100 | 0.001 |
| 4 | 400 | 0.01 |
| 5 | 900 | 0.01 |

**Part b — NVT with Berendsen thermostat:**

| Case | N | T |
|------|---|---|
| 1 | 100 | 0.1 |
| 2 | 100 | 1.0 |
| 3 | 625 | 1.0 |
| 4 | 900 | 1.0 |

## References

- D. Frenkel and B. Smit, *Understanding Molecular Simulation*, 2nd ed., Academic Press, 2002.
  - §4.2.1 Initialization (p. 66)
  - §4.2.2 Force calculation (p. 68)
  - §4.2.3 Velocity-Verlet integration (p. 69)
  - Algorithm 7: Radial distribution function (p. 86)
- Velocity-Verlet algorithm: https://en.wikipedia.org/wiki/Verlet_integration
