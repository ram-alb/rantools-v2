import logging
import os
import re
from types import MappingProxyType
from typing import Optional

import enmscripting
import pandas as pd
from ldap3 import ALL, SUBTREE, Connection, Server

from services.db.db import DbConnection, select
from toa_submit.services.connect_eniq import connect

logger = logging.getLogger(__name__)


ATOLL_HOST = os.getenv('ATOLL_HOST')
ATOLL_PORT = os.getenv('ATOLL_PORT')
SERVICE_NAME = os.getenv('SERVICE_NAME')
ATOLL_LOGIN = os.getenv('ATOLL_LOGIN')
ATOLL_PASSWORD = os.getenv('ATOLL_PASSWORD')
TNS_NAME = os.getenv("TNS_NAME")
PQSWEB_LOGIN = os.getenv("PQSWEB_LOGIN")
PQSWEB_PASSWORD = os.getenv("PQSWEB_PASSWORD")
ENM_SERVER_TWO = os.getenv('ENM_SERVER_2')
ENM_SERVER_FOUR = os.getenv('ENM_SERVER_4')
ENM_USERNAME = os.getenv('ENM_LOGIN')
ENM_PASSWORD = os.getenv('ENM_PASSWORD')
ORACLE_CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH")
TNS_ADMIN_PATH = os.getenv("TNS_ADMIN_PATH")

CABINET_TYPE_DICT = MappingProxyType({
    'RBS6630': '44',
    'RBS6101': '29',
    'RBS6101(optic cable)': '31',
    'RBS6102(optic cable)': '25',
    'RBS6601': '33',
    'RBS6601(optic cable)': '35',
    'RBS6648': '48',
    'RBS6641': '50',
    'RBS6631': '55',
    'RBS6102': '15',
    'RBS6201': '16',
    'RBS6201(optic cable)': '26',
    'RBS6150': '47',
    'RANP6651': '57',
    'RANP 6651': '57',
    'BS8700': '21',
    'BS8800': '22',
    'BS8900': '23',
    'BS8900A': '24',
})

attr_delimitter = '/'


def get_site_eniq(sitename):
    """Return Site Eniq Server."""
    command = f'cmedit get {sitename} -t'
    try:
        session = enmscripting.open(ENM_SERVER_FOUR).with_credentials(
            enmscripting.UsernameAndPassword(
                username=ENM_USERNAME,
                password=ENM_PASSWORD,
            ),
        )
        enmcommand = session.command()
        response = enmcommand.execute(command)
        enmdata = response.get_output().groups()[0]
        if enmdata:
            return 'ENIQ4'
    except Exception:
        session = enmscripting.open(ENM_SERVER_TWO).with_credentials(
            enmscripting.UsernameAndPassword(
                username=ENM_USERNAME,
                password=ENM_PASSWORD,
            ),
        )
        enmcommand = session.command()
        response = enmcommand.execute(command)
        enmdata = response.get_output().groups()[0]
        if enmdata:
            return 'ENIQ2'
    finally:
        enmscripting.close(session)


def get_common_data(sitename: str) -> Optional[dict]:
    """Return common IP-related data and cabinet info for the given sitename."""
    eniq = get_site_eniq(sitename)
    common_data = {}

    try:
        connection = connect(eniq)
        if not connection:
            return None

        cursor = connection.cursor()
        cursor.execute(_build_select_tr(), (sitename,))
        rows = cursor.fetchall()

        for tech, raw_ip in rows:
            ip = raw_ip.split(attr_delimitter)[0]
            _map_ip_by_technology(common_data, tech, ip)

        cursor.execute(_build_select_cab(), (sitename,))
        cabinet_info = cursor.fetchone()
        if cabinet_info:
            subnet, pname, serial = cabinet_info
            common_data["SubNetwork"] = subnet
            common_data["PName"] = pname
            common_data["SN"] = serial

        return common_data or None

    except Exception as exc:
        logger.warning("❌ IP addresses data not found: %s", exc)  # noqa: WPS323
        return None


def _map_ip_by_technology(common_data: dict, tech: str, ip: str) -> None:
    """Map technologies to standardized field names."""
    mappings = {
        'NR': 'NR',
        'S1': 'S1',
        'OAM': 'OAM',
        'Abis': 'Abis',
        'Iub': 'Iub',
    }

    for key, name in mappings.items():
        if key in tech:
            common_data[name] = ip
            break


def _build_select_tr() -> str:
    return (
        "SELECT Addressipv4, usedAddress "
        "FROM dc.DC_E_BULK_CM_ADDRESSIPV4_RAW x "
        "WHERE ELEMENT = ? "
        "AND UTC_DATETIME_ID = ("
        "   SELECT MAX(UTC_DATETIME_ID) "
        "   FROM dc.DC_E_BULK_CM_ADDRESSIPV4_RAW y "
        "   WHERE y.ELEMENT = x.ELEMENT AND y.Interfaceipv4 = x.Interfaceipv4)"
    )


def _build_select_cab() -> str:
    return (
        "SELECT ELEMENTPARENT, productData_productName AS PNAME, "
        "productData_serialNumber AS SN "
        "FROM DC.DC_E_BULK_CM_CABINET_RAW x "
        "WHERE ELEMENT = ? "
        "AND UTC_DATETIME_ID = ("
        "   SELECT MAX(UTC_DATETIME_ID) "
        "   FROM DC.DC_E_BULK_CM_CABINET_RAW y "
        "   WHERE x.ELEMENT = y.ELEMENT)"
    )


def extract_site_id(sitename):
    """Extract site id by NodeName."""
    match = re.search(r'\d{5}', sitename)
    return match.group(0) if match else None


def get_technology_data(sitename: str, technology: str) -> Optional[dict]:
    """Fetch ENIQ data for 2G or 3G technologies."""
    eniq = get_site_eniq(sitename)
    site = _extract_clean_site_name(sitename)
    technology_data = {}

    try:
        connection = connect(eniq)
        cursor = connection.cursor()

        if technology == "2G":
            _populate_gsm_site_name(cursor, sitename, technology_data)
            site = technology_data.get("SITE_NAME", site)
            _fetch_gsm_parameters(cursor, site, sitename, technology_data)

        elif technology == "3G":
            _fetch_wcdma_parameters(cursor, sitename, technology_data)

        cursor.close()
        return technology_data if technology_data else None

    except Exception as exc:
        logger.warning("❌ ENM Data not found: %s", exc)  # noqa: WPS323
        return None


def _extract_clean_site_name(sitename: str) -> str:
    """Extract normalized site name from sitename string."""
    parts = sitename.split("_")

    if len(parts) == 5:
        first_part, second_part, third_part = parts[1], parts[-2], parts[-1]
        return f"{first_part}_{second_part}_{third_part}"

    if len(parts) == 4:
        first_part, second_part, third_part = parts[0], parts[-2], parts[-1]
        return f"{first_part}_{second_part}_{third_part}"

    return sitename


def _populate_gsm_site_name(cursor, sitename: str, gsm_data: dict) -> None:
    site_id = extract_site_id(sitename)
    query = (
        "SELECT SITE_NAME "
        "FROM DC.DIM_E_GRAN_CELL "
        "WHERE STATUS = 'ACTIVE' AND site_name LIKE ?"
    )
    cursor.execute(query, (f"%{site_id}%",))
    query_result = cursor.fetchone()
    if query_result:
        gsm_data["SITE_NAME"] = query_result[0]


def _fetch_gsm_parameters(cursor, site: str, sitename: str, gsm_data: dict) -> None:
    param_query = (
        "SELECT BSC_NAME, LAC, LIST(CELL_NAME, ',') AS CELLS, "
        "LIST(CELL_ID, ',') AS CELLIDS "
        "FROM DC.DIM_E_GRAN_CELL "
        "WHERE STATUS = 'ACTIVE' AND site_name LIKE ? "
        "GROUP BY BSC_NAME, LAC"
    )
    cursor.execute(param_query, (site,))
    query_result = cursor.fetchone()
    if not query_result:
        return

    bsc, lac, cells, cell_ids = query_result
    gsm_data["NE"] = bsc
    gsm_data["LAC"] = lac
    gsm_data["CLIST"] = cells
    gsm_data["CID"] = cell_ids

    tg_query = (
        "SELECT LIST(TG_NAME, ',') AS TGS "
        "FROM DC.DIM_E_GRAN_TG "
        "WHERE STATUS = 'ACTIVE' AND BTSME LIKE ?"
    )
    cursor.execute(tg_query, (site,))
    tg_result = cursor.fetchone()
    if tg_result:
        gsm_data["TG"] = tg_result[0]

    trx_query = (
        "SELECT COUNT(DISTINCT GSMSECTOR), COUNT(DISTINCT TRX) "
        "FROM DC.DIM_E_GRAN_RADIONODE_TRX "
        "WHERE RADIONODE LIKE ? AND STATUS = 'ACTIVE'"
    )
    cursor.execute(trx_query, (sitename,))
    trx_result = cursor.fetchone()
    if trx_result:
        trx_count = int(trx_result[1])
        sector_count = int(trx_result[0])
        gsm_data["TRX"] = "+".join(str(trx_count) for _ in range(sector_count))
        gsm_data["EDGE"] = get_trx(sitename)


def _fetch_wcdma_parameters(cursor, sitename: str, wcdma_data: dict) -> None:
    query = (
        "SELECT RNC_ID, LAC, LIST(UCELL_NAME, ',') AS CELLS, "
        "LIST(LOCALCellID, ',') AS CELLIDS "
        "FROM DC.DIM_E_RAN_UCELL "
        "WHERE STATUS = 'ACTIVE' AND RBS_ID LIKE ? "
        "GROUP BY RNC_ID, LAC"
    )
    cursor.execute(query, (sitename,))
    query_result = cursor.fetchone()
    if not query_result:
        return

    rnc, lac, cells, cell_ids = query_result
    wcdma_data["NE"] = rnc
    wcdma_data["LAC"] = lac
    wcdma_data["CLIST"] = cells
    wcdma_data["CID"] = cell_ids


def get_data(sitename):
    """Fetch and Get GSM Site Trx AbisTsState."""
    eniq = get_site_eniq(sitename)
    if eniq == 'ENIQ2':
        enm_server = ENM_SERVER_TWO
    elif eniq == 'ENIQ4':
        enm_server = os.getenv('ENM_SERVER_4')
    else:
        return None
    try:
        session = enmscripting.open(enm_server).with_credentials(
            enmscripting.UsernameAndPassword(
                username=ENM_USERNAME,
                password=ENM_PASSWORD,
            ),
        )
        enmcommand = session.command()
        response = enmcommand.execute(f'cmedit get {sitename} Trx.(abisTsState) -t')
        return response.get_output().groups()[0]
    except Exception as exc:
        logger.warning("❌ ENM Data not found: %s", exc)  # noqa: WPS323
        return None
    finally:
        enmscripting.close(session)


def get_trx(sitename):
    """Fetch and get GSM site Trxs."""
    site_data = get_data(sitename)
    if site_data is None:
        return 'NO CONNECTION BY ENM2'
    try:
        df = pd.DataFrame(site_data, columns=['siteId', 'opState', 'sector', 'trxId', 'state'])
        df['trxId'] = df['trxId'].apply(str)
        filter_df = df.loc[df['trxId'] == '0'].copy()
        filter_df['sector'] = filter_df['sector'].apply(str)
        filter_df['siteId'] = filter_df['siteId'].apply(str)

        response_data = filter_df.groupby('sector').agg({
            'siteId': 'first',
            'state': list,
        }).reset_index()

        state_length = len(str((response_data['state'][0])).split(','))
        num_sector = response_data['sector'].nunique()
        return '+'.join(str(state_length) for _ in range(num_sector))
    except Exception as exc:
        logger.warning("❌ ENM Data not found: %s", exc)  # noqa: WPS323
        return 'NOT DATA FOUND'


def get_site_name(sitename: str):
    """Fetch sitename by 2G."""
    eniq = get_site_eniq(sitename)
    try:
        connection = connect(eniq)
        cursor = connection.cursor()
        site_id = extract_site_id(sitename)
        query = (
            "SELECT SITE_NAME "
            "FROM DC.DIM_E_GRAN_CELL "
            "WHERE STATUS = 'ACTIVE' "
            "AND site_name LIKE ?"
        )
        cursor.execute(query, (f"%{site_id}%"))
        query_result = cursor.fetchone()
        return query_result[0] if query_result else sitename
    except Exception as exc:
        logger.warning("❌ Exception by ENIQ: %s", exc)  # noqa: WPS323
        return sitename


def row_to_dict(name, latitude, longitude, address):
    """Row Factory for site information."""
    return {
        'name': name,
        'latitude': latitude,
        'longitude': longitude,
        'address': address,
    }


def get_site_information(sitename: str):
    """Get site data from Oracle and format into dict."""
    query = """
        SELECT NAME, LATITUDE, LONGITUDE, nvl(SITE_ADRESS, 'no address by ATOLL')
        from atoll_mrat.sites
        where name =:site_name
        """
    site_name = {"site_name": sitename}

    with DbConnection('oracledb') as connection:
        site_data = select(connection, query, sql_params=site_name, row_factory=row_to_dict)

    return site_data[0] if site_data else None


def get_subordinates(manager_dn, conn):
    """Fetch subordinates name and phone."""
    subordinates = []
    conn.search(
        search_base='OU=KCELL,dc=kcell,dc=kz',
        search_filter=f'(&(manager={manager_dn})(objectClass=person))',
        search_scope=SUBTREE,
        attributes=['cn', 'mobile', 'manager'],
    )

    for entry in conn.entries:
        subordinate = {
            'name': entry.cn.value,
            'mobile': entry.mobile.value if entry.mobile and entry.mobile.value else 'not number',
        }
        subordinates.append(subordinate)
        subordinates += get_subordinates(entry.entry_dn, conn)

    return subordinates


def get_dictionary_by_ldap():
    """Fetch and sort LDAP subordinates by name."""
    server = Server('ldap://192.168.190.5', get_info=ALL)
    try:
        conn = Connection(server, 'anpusr@kcell.kz', 'NZJ*vfH29ep9', auto_bind=True)
        manager_dn = (
            "CN=Azamat Galiulla,"
            "OU=Users,"
            "OU=Information and Communication Technologies Dpt.,"
            "OU=KCELL,"
            "DC=kcell,DC=kz"
        )

        all_subordinates = get_subordinates(manager_dn, conn)
        return sorted(all_subordinates, key=lambda entry: entry['name'])
    except Exception as exc:
        logger.warning("❌ LDAP lookup failed: %s", exc)  # noqa: WPS323
        return []
