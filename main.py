import os
import numpy as np
import matplotlib.pyplot as plt
from utils.config import SimConfig, nve_case
from utils.recorder import Record, init_record, record
from simulation.init import init_state
from simulation.forces import compute_forces
from simulation.integrator import verlet_step
from simulation.thermostat import berendsen
from rdf import compute_rdf

def run_nve(cfg) -> Record:
    state = init_state(cfg)
    state, E_pot = compute_forces(state, cfg)  # compute initial forces
    rec = init_record()

    for step in range(cfg.n_steps):
        state, E_pot = verlet_step(state, cfg)
        record(rec, state, E_pot, cfg)

    return rec

def plot_nve(rec: Record, label: str) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)

    axes[0].plot(rec.E_tot, label='E_tot')
    axes[0].plot(rec.E_kin, label='E_kin')
    axes[0].plot(rec.E_pot, label='E_pot')
    axes[0].set_ylabel('Energy')
    axes[0].legend()

    axes[1].plot(rec.T)
    axes[1].set_ylabel('Temperature')

    axes[2].plot(rec.p_tot)
    axes[2].set_ylabel('Total momentum')
    axes[2].set_xlabel('Step')

    fig.suptitle(label)
    plt.tight_layout()

    filename = label.replace(' ', '_').replace(',', '').replace('=', '') + '.png'
    os.makedirs('output/nve', exist_ok=True)
    plt.savefig(f'output/nve/{filename}')
    plt.close()
    print(f'Saved output/nve/{filename}')

def run_nvt(cfg, equilibration_steps=2000) -> tuple[Record, np.ndarray, np.ndarray]:
    state = init_state(cfg)
    state, E_pot = compute_forces(state, cfg)
    rec = init_record()

    for step in range(cfg.n_steps):
        state, E_pot = verlet_step(state, cfg)
        T_current = (state.vel ** 2).sum() / (2 * cfg.N - 2)
        state = berendsen(state, T_current, cfg)
        record(rec, state, E_pot, cfg)

    r_bins, g_r = compute_rdf(state.pos, cfg)
    return rec, r_bins, g_r

def plot_nvt(rec: Record, r_bins, g_r, label: str) -> None:
    fig, axes = plt.subplots(4, 1, figsize=(8, 10), sharex=False)

    axes[0].plot(rec.E_tot, label='E_tot')
    axes[0].plot(rec.E_kin, label='E_kin')
    axes[0].plot(rec.E_pot, label='E_pot')
    axes[0].set_ylabel('Energy')
    axes[0].legend()

    axes[1].plot(rec.T)
    axes[1].axhline(y=np.mean(rec.T[-1000:]) if len(rec.T) > 1000 else rec.T[-1],
                color='r', linestyle='--', label=f'mean T={np.mean(rec.T[-1000:]):.3f}')
    axes[1].set_ylabel('Temperature')
    axes[1].legend()

    axes[2].plot(rec.p_tot)
    axes[2].set_ylabel('Total momentum')

    axes[3].plot(r_bins, g_r)
    axes[3].axhline(y=1.0, color='r', linestyle='--')
    axes[3].set_ylabel('g(r)')
    axes[3].set_xlabel('r')

    fig.suptitle(label)
    plt.tight_layout()

    filename = label.replace(' ', '_').replace(',', '').replace('=', '') + '.png'
    os.makedirs('output/nvt', exist_ok=True)
    plt.savefig(f'output/nvt/{filename}')
    plt.close()
    print(f'Saved output/nvt/{filename}')

def main() -> None:
    dt = 0.01
    nve_cases = [
        (nve_case(N=100, dt=0.01),  'N=100, dt=0.01'),
        (nve_case(N=100, dt=0.005), 'N=100, dt=0.005'),
        (nve_case(N=100, dt=0.001), 'N=100, dt=0.001'),
        (nve_case(N=400, dt=0.01),  'N=400, dt=0.01'),
        (nve_case(N=900, dt=0.01),  'N=900, dt=0.01'),
    ]

    for cfg, label in nve_cases:
        print(f'Running {label}...')
        rec = run_nve(cfg)
        plot_nve(rec, label)

    # part b
    dt = 0.01
    nvt_cases = [
        (SimConfig(L=30.0, N=100, T=0.1, dt=dt, rc=2.5, n_steps=20000, tau=dt/0.0025, seed=42), 'N=100, T=0.1'),
        (SimConfig(L=30.0, N=100, T=1.0, dt=dt, rc=2.5, n_steps=5000, tau=dt/0.0025, seed=42), 'N=100, T=1.0'),
        (SimConfig(L=30.0, N=625, T=1.0, dt=dt, rc=2.5, n_steps=5000, tau=dt/0.0025, seed=42), 'N=625, T=1.0'),
        (SimConfig(L=30.0, N=900, T=1.0, dt=dt, rc=2.5, n_steps=5000, tau=dt/0.0025, seed=42), 'N=900, T=1.0'),
    ]

    for cfg, label in nvt_cases:
        print(f'Running {label}...')
        rec, r_bins, g_r = run_nvt(cfg)
        plot_nvt(rec, r_bins, g_r, label)

if __name__ == '__main__':
    main()
