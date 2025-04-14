from collections import namedtuple

from services.db.db import select, DbConnection

def select_network_params():
    """
    Select LTE network parameters.

    Returns:
        list: a list of namedtuples
    """
    sql_command = r"""
        SELECT
            subnetwork,
            sitename,
            cell,
            tac,
            cellid,
            physicalcellid,
            earfcndl,
            rachrootsequence
        FROM network_live.ltecells2
        WHERE oss LIKE 'ENM%'
            AND REGEXP_LIKE(cell, '^\d{5}')
    """

    row_factory = namedtuple(
        'NetworkParams',
        [
            'subnetwork',
            'site',
            'cell',
            'tac',
            'cellid',
            'pci',
            'earfcndl',
            'rach',
        ],
    )
    with DbConnection('oracledb') as conn:
        return select(conn, sql_command, row_factory=row_factory)


def select_atoll_params():
    """
    Select LTE parameters from atoll.

    Returns:
        list: list of namedtuples
    """
    sql_command = r"""
        SELECT
            s.name as sitename,
            s.lte_sitename,
            c.cell_id as cell,
            c.tac,
            c.unique_id as cellid,
            c.pci,
            c.carrier as earfcndl,
            c.prach_rsi_list as rach
        FROM atoll_mrat.xgcellslte c
            LEFT JOIN atoll_mrat.xgtransmitters t
                ON c.tx_id = t.tx_id
            LEFT JOIN atoll_mrat.sites s
                ON t.site_name = s.name
        WHERE c.active = -1
            AND REGEXP_LIKE (c.cell_id, '^\d{5}')
    """

    row_factory = namedtuple(
        'AtollParams',
        [
            'sitename',
            'lte_sitename',
            'cell',
            'tac',
            'cellid',
            'pci',
            'earfcndl',
            'rach',
        ],
    )

    with DbConnection('oracledb') as conn:
        return select(conn, sql_command, row_factory=row_factory)
