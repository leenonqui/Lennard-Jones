import numpy as np
from dataclasses import dataclass
from simulation.state import ParticleState

@dataclass
class Record:
    E_kin: list
    E_pot: list
    E_tot: list
    T:     list
    p_tot: list

def init_record() -> Record:
    return Record(E_kin=[], E_pot=[], E_tot=[], T=[], p_tot=[])

def record(rec: Record, state: ParticleState, E_pot: float, cfg) -> None:
    E_kin = 0.5 * (state.vel ** 2).sum()  # m=1
    T = (state.vel ** 2).sum() / (2 * cfg.N - 2)  # equipartition, dof=2N-2
    p_tot = np.abs(state.vel.sum(axis=0)).sum()  # should stay ~0

    rec.E_kin.append(E_kin)
    rec.E_pot.append(E_pot)
    rec.E_tot.append(E_kin + E_pot)
    rec.T.append(T)
    rec.p_tot.append(p_tot)
