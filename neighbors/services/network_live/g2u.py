from neighbors.services.network_live.categorize_neighbors import categorize_planned_neighbors
from neighbors.services.network_live.tables import get_network_cells


def categorize_g2u_neighbors(planned_neighbors):
    """Categorize G2U planned neighbors into existing and nonexistent cells."""
    gsm_network_cells = get_network_cells('GSM')
    wcdma_network_cells = get_network_cells('WCDMA')
    return categorize_planned_neighbors(planned_neighbors, gsm_network_cells, wcdma_network_cells)
