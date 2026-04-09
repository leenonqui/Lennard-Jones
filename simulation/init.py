import numpy as np
from simulation.state import ParticleState

def init_state(cfg) -> ParticleState:
  rng = np.random.default_rng(cfg.seed)

  n_side = int(np.sqrt(cfg.N))
  spacing = cfg.L / n_side
  pos = np.array([
  [(i + 0.5) * spacing, (j + 0.5) * spacing]
  for i in range(n_side)
  for j in range(n_side)
  ])

  # uniform random velocities in [-0.5, 0.5] — Frenkel & Smit §4.2.1, Algorithm 4
  # (will relax to Maxwell-Boltzmann on equilibration)
  vel = rng.uniform(-0.5, 0.5, (cfg.N, 2))

  # zero total momentum
  vel -= vel.mean(axis=0)

  # Frenkel & Smit §4.2.1 Algorithm 4: fs = sqrt(ndim * T / sumv2)
  # sumv2 = mean squared velocity per particle
  # ndim=2 because equipartition in 2D: <0.5*m*v²> = ndim/2 * kB*T per particle
  sumv2 = (vel ** 2).sum() / cfg.N  # mean squared velocity
  fs = np.sqrt(2 * cfg.T / sumv2)
  vel *= fs

  force = np.zeros((cfg.N, 2))
  return ParticleState(pos=pos, vel=vel, force=force)
