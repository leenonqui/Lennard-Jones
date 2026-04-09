from dataclasses import dataclass
import numpy as np

@dataclass
class ParticleState:
    pos:   np.ndarray  # (N, 2)
    vel:   np.ndarray  # (N, 2)
    force: np.ndarray  # (N, 2)
