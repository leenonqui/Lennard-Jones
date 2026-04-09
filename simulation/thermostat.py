import numpy as np
from simulation.state import ParticleState

def berendsen(state: ParticleState, T_current: float, cfg) -> ParticleState:
  lmbda = np.sqrt(1 + (cfg.dt/cfg.tau) * (cfg.T/T_current - 1))
  new_vel = state.vel * lmbda
  return ParticleState(state.pos, new_vel, state.force)
