from bts_files.services.atoll.gsm import GsmRowFactory
from bts_files.services.atoll.lte import LteRowFactory
from bts_files.services.atoll.main import CellRowFactory
from bts_files.services.atoll.nr import NrRowFactory
from bts_files.services.atoll.wcdma import WcdmaRowFactory
from bts_files.services.filter_cells import AllTechPolygon
from bts_files.services.utils import DEFAULT_WIDTH, calc_azimut_beam


def _get_lte_carrier(carrier: str) -> str:
    """Extract the LTE carrier from a given carrier string."""
    carr = carrier.split('(')[-1]
    return carr[:-1]


def _get_nr_carrier(carrier: str) -> str:
    """Extract the NR carrier from a given carrier string."""
    carrier_data = carrier.split(' ')[-1]

    if '(' in carrier_data:
        return carrier_data.split('(')[0]

    return carrier_data


def _get_common_part(cell: CellRowFactory) -> str:
    common_params = [
        cell.site,
        str(cell.latitude),
        str(cell.longitude),
        cell.cell,
    ]
    return ';'.join(common_params)


def _replace_none(params_list: list) -> list:
    return [
        '' if param_item is None else param_item
        for param_item in params_list
    ]


def _get_gsm_uniq(cell: GsmRowFactory) -> str:
    uniq_params = [
        str(cell.bcch),
        str(cell.bsic),
        str(cell.cid),
        '',
        str(cell.lac),
        '',
        str(cell.azimut),
        str(DEFAULT_WIDTH),
    ]
    return ';'.join(_replace_none(uniq_params))


def _get_wcdma_uniq(cell: WcdmaRowFactory) -> str:
    uniq_params = [
        str(cell.carrier),
        '',
        str(cell.cid),
        '',
        str(cell.lac),
        str(cell.psc),
        str(cell.azimut),
        str(DEFAULT_WIDTH),
    ]
    return ';'.join(_replace_none(uniq_params))


def _get_lte_uniq(cell: LteRowFactory) -> str:
    carrier = _get_lte_carrier(cell.carrier)
    azimut, beam_width = calc_azimut_beam(cell)
    uniq_params = [
        carrier,
        '',
        cell.cid,
        str(cell.pci),
        '',
        '',
        str(azimut),
        str(beam_width),
    ]
    return ';'.join(_replace_none(uniq_params))


def _get_nr_uniq(cell: NrRowFactory) -> str:
    carrier = _get_nr_carrier(cell.carrier)
    uniq_params = [
        carrier,
        '',
        cell.cid,
        str(cell.pci),
        '',
        '',
        str(cell.azimut),
        str(DEFAULT_WIDTH),
    ]
    return ';'.join(_replace_none(uniq_params))


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
    elif technology == 'NR':
        nr_uniq = _get_nr_uniq(cell)  # type: ignore
        row = f'NR;{common};{nr_uniq};'

    return row


def make_nbf_content(cell_data: AllTechPolygon) -> str:
    """Generate NBF content from the given cell data for different technologies."""
    nbf_content = 'SYSTEM;SITE;LAT;LON;CELL;CH;BSIC;CID;PCI;LAC;SCR;DIR;BEAM;'

    for tech, tech_data in cell_data.items():
        if tech == 'sites':
            continue
        for cell in tech_data:  # type: ignore
            nbf_content = nbf_content + '\n{row}'.format(row=_get_tech_row(cell, tech))

    return nbf_content
