import numpy as np

def compute_rdf(positions, cfg, dr=0.05):
    n_bins = int((cfg.L / 2) / dr)
    rho = cfg.N / cfg.L ** 2

    # all unique pairs — no cutoff restriction
    i_idx, j_idx = np.where(np.arange(cfg.N)[:, None] < np.arange(cfg.N)[None, :])
    dxdy = positions[i_idx] - positions[j_idx]
    dxdy -= cfg.L * np.round(dxdy / cfg.L)
    distances = np.sqrt((dxdy ** 2).sum(axis=1))

    distances = distances[distances < cfg.L / 2]

    bin_edges = np.arange(n_bins + 1) * dr
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    pair_counts, _ = np.histogram(distances, bins=bin_edges)
    pair_counts = pair_counts * 2

    shell_area = np.pi * (bin_edges[1:]**2 - bin_edges[:-1]**2)
    ideal_gas_count = rho * shell_area
    g_r = pair_counts / (cfg.N * ideal_gas_count)

    return bin_centers, g_r
