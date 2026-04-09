import numpy as np
from simulation.state import ParticleState
from simulation.grid import get_pairs

def compute_forces(state: ParticleState, cfg) -> tuple[ParticleState, float]:
  force = np.zeros((cfg.N, 2))
  E_pot = .0

  i_idx, j_idx = get_pairs(state.pos, cfg)
  dr = state.pos[i_idx] - state.pos[j_idx]
  dr -= cfg.L * np.round(dr / cfg.L) # minimum img convention
  r2 = (dr ** 2).sum(axis=1)

  r2i = 1.0 / r2
  r6i = r2i ** 3
  ff = 48 * r2i * r6i * (r6i - 0.5)

  f_ij = ff[:, np.newaxis] * dr
  # accumulate forces at each index (force i -> j = - force j -> i)
  np.add.at(force, i_idx, f_ij)
  np.add.at(force, j_idx, -f_ij)

  ecut = 4 * (1/cfg.rc**12 - 1/cfg.rc**6)
  E_pot = (4 * r6i * (r6i - 1) - ecut).sum()

  return ParticleState(pos=state.pos, vel=state.vel, force=force), E_pot
