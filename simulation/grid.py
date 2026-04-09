import numpy as np

def build_cell_list(pos, cfg):
    nc = int(cfg.L / cfg.rc)
    cell_size = cfg.L / nc
    ci = (pos[:, 0] / cell_size).astype(int) % nc
    cj = (pos[:, 1] / cell_size).astype(int) % nc
    cell_id = ci * nc + cj  # (N,)
    return cell_id, nc

def get_neighbor_cells(cell_id, nc):
    # for each particle get its 9 neighboring cell ids — (N, 9)
    ci = cell_id // nc
    cj = cell_id % nc
    offsets = np.array([[di, dj] for di in [-1,0,1] for dj in [-1,0,1]])
    ci_nb = (ci[:, None] + offsets[:, 0]) % nc
    cj_nb = (cj[:, None] + offsets[:, 1]) % nc
    return ci_nb * nc + cj_nb  # (N, 9)

def get_pairs(pos, cfg):
    cell_id, nc = build_cell_list(pos, cfg)
    nb_ids = get_neighbor_cells(cell_id, nc)  # (N, 9)

    # in_neighborhood[i, j] = True if j is in any neighbor cell of i
    in_neighborhood = (cell_id[None, :] == nb_ids[:, :, None]).any(axis=1)  # (N, N)

    # unique pairs i < j only
    i_idx, j_idx = np.where(np.tril(in_neighborhood, k=-1))

    # distance cutoff with minimum image
    dr = pos[i_idx] - pos[j_idx]
    dr -= cfg.L * np.round(dr / cfg.L)
    r2 = (dr ** 2).sum(axis=1)
    mask = r2 <= cfg.rc ** 2

    return i_idx[mask], j_idx[mask]
