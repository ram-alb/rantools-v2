from bts_files.services.atoll.gsm import GsmRowFactory
from bts_files.services.atoll.lte import LteRowFactory
from bts_files.services.atoll.main import CellRowFactory
from bts_files.services.atoll.wcdma import WcdmaRowFactory
from bts_files.services.filter_cells import AllTechPolygon


def _get_lte_carrier(carrier: str) -> str:
    """Extract the LTE carrier from a given carrier string."""
    carr = carrier.split('(')[-1]
    return carr[:-1]


def _get_common_part(cell: CellRowFactory) -> str:
    common_params = [
        cell.site,
        str(cell.latitude),
        str(cell.longitude),
        cell.cell,
    ]
    return ';'.join(common_params)


def _get_gsm_uniq(cell: GsmRowFactory) -> str:
    uniq_params = [
        str(cell.bcch),
        str(cell.bsic),
        str(cell.cid),
        '',
        str(cell.lac),
        '',
        str(cell.azimut),
    ]
    return ';'.join(uniq_params)


def _get_wcdma_uniq(cell: WcdmaRowFactory) -> str:
    uniq_params = [
        str(cell.carrier),
        '',
        str(cell.cid),
        '',
        str(cell.lac),
        str(cell.psc),
        str(cell.azimut),
    ]
    return ';'.join(uniq_params)


def _get_lte_uniq(cell: LteRowFactory) -> str:
    carrier = _get_lte_carrier(cell.carrier)
    uniq_params = [
        carrier,
        '',
        cell.cid,
        str(cell.pci),
        '',
        '',
        str(cell.azimut),
    ]
    return ';'.join(uniq_params)


def _get_tech_row(cell: CellRowFactory, technology: str) -> str:
    """Construct a row string for a given cell and technology."""
    common = _get_common_part(cell)

    if technology == 'GSM':
        gsm_uniq = _get_gsm_uniq(cell)  # type: ignore
        row = f'GSM;{common};{gsm_uniq};'
    elif technology == 'WCDMA':
        wcdma_uniq = _get_wcdma_uniq(cell)  # type: ignore
        row = f'UMTS;{common};{wcdma_uniq};'
    elif technology == 'LTE':
        lte_uniq = _get_lte_uniq(cell)  # type: ignore
        row = f'LTE;{common};{lte_uniq};'

    return row


def make_nbf_content(cell_data: AllTechPolygon) -> str:
    """Generate NBF content from the given cell data for different technologies."""
    nbf_content = 'SYSTEM;SITE;LAT;LON;CELL;CH;BSIC;CID;PCI;LAC;SCR;DIR;'

    for tech, tech_data in cell_data.items():
        if tech in {'sites', 'NR'}:
            continue
        for cell in tech_data:  # type: ignore
            nbf_content = nbf_content + '\n{row}'.format(row=_get_tech_row(cell, tech))

    return nbf_content
