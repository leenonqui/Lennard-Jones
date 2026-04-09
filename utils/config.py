from dataclasses import dataclass

@dataclass
class SimConfig:
  L:       float # domain size
  N:       int   # number of particles
  T:       float # target temperature
  dt:      float # time step
  rc:      float # cell radius (interactions)
  n_steps: int   # total number of stpes
  tau:     float # Berendsen relaxation time (dt/tau = 0.0025)
  seed:    int   # RNG

def nve_case(N=256, T=0.5, dt=0.01, n_steps=5000, seed=42) -> SimConfig:
    return SimConfig(L=30.0, N=N, T=T, dt=dt, rc=2.5, n_steps=n_steps, tau=dt/0.0025, seed=seed) # flexible config for part a) of assignment

def nvt_n100_t01() -> SimConfig:
    return SimConfig(L=30.0, N=100, T=0.1, dt=0.01, rc=2.5, n_steps=10000, tau=0.01/0.0025, seed=42)

def nvt_n100_t10() -> SimConfig:
    return SimConfig(L=30.0, N=100, T=1.0, dt=0.01, rc=2.5, n_steps=10000, tau=0.01/0.0025, seed=42)

def nvt_n625_t10() -> SimConfig:
    return SimConfig(L=30.0, N=625, T=1.0, dt=0.01, rc=2.5, n_steps=10000, tau=0.01/0.0025, seed=42)

def nvt_n900_t10() -> SimConfig:
    return SimConfig(L=30.0, N=900, T=1.0, dt=0.01, rc=2.5, n_steps=10000, tau=0.01/0.0025, seed=42)

