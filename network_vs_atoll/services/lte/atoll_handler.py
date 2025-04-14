import re


def parse_earfcndl(atoll_earfcndl):
    """
    Parse earfcndl value from atoll data.

    Args:
        atoll_earfcndl (str): an earfcndl data

    Returns:
        str: earfcndl value
    """
    try:
        return re.search(r'(?<=\()\d+(?=\))', atoll_earfcndl).group()
    except AttributeError:
        numbers = re.findall(r'\d+', atoll_earfcndl)
        if numbers:
            return max(numbers, key=len)
        else:
            return None

def parse_rach(atoll_rach):
    """
    Parse rach value from atoll data.

    Args:
        atoll_rach (str): a rach data

    Returns:
        str: rach value
    """
    return atoll_rach.split('-')[0] if atoll_rach else -1


def make_int(parameter):
    """
    Make parameter of int instanse.

    Args:
        parameter (str): a parameter value

    Returns:
        int
    """
    return int(parameter) if parameter == 0 or parameter else -1


def handle_atoll_lte_params(atoll_params):
    """
    Handle all LTE parameters selected from atoll.

    Args:
        atoll_params (list): a list of namedtuples with LTE params

    Returns:
        dict: keys are the cells, values are the dicts with cell parameters
    """
    atoll_params_dict = {}
    for row in atoll_params:
        site = row.lte_sitename if row.lte_sitename else row.sitename
        earfcndl = parse_earfcndl(row.earfcndl)
        rach = parse_rach(row.rach)
        atoll_params_dict[row.cell] = {
            'site': site,
            'tac': make_int(row.tac),
            'cellid': make_int(row.cellid),
            'pci': make_int(row.pci),
            'earfcndl': make_int(earfcndl),
            'rach': make_int(rach),
        }
    return atoll_params_dict


def get_cell_atoll_params(cell, atoll_params):
    """
    Get parameters for one cell from atoll LTE cell data.

    Args:
        cell (str): a cell name
        atoll_params (dict): keys are cells, values are dicts of cell parameters

    Returns:
        dict: dict with parameters if cell found or default values
    """
    try:
        atoll_cell_params = atoll_params[cell]
    except KeyError:
        atoll_cell_params = {
            'site': '',
            'tac': -1,
            'cellid': -1,
            'pci': -1,
            'earfcndl': -1,
            'rach': -1,
        }
    return atoll_cell_params
