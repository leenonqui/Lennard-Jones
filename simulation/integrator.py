from simulation.state import ParticleState
from simulation.forces import compute_forces

def verlet_step(state: ParticleState, cfg) -> tuple[ParticleState, float]:

    new_pos = (state.pos + state.vel * cfg.dt + 0.5 * state.force * cfg.dt**2) % cfg.L

    tmp = ParticleState(pos=new_pos, vel=state.vel, force=state.force)
    new_state, E_pot = compute_forces(tmp, cfg)

    new_vel = state.vel + 0.5 * (state.force + new_state.force) * cfg.dt

    return ParticleState(pos=new_pos, vel=new_vel, force=new_state.force), E_pot


