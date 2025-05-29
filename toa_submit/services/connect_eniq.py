import logging
import os

import pyodbc

logger = logging.getLogger(__name__)


def connect(eniq: str) -> pyodbc.Connection:
    """
    Establish a connection to the ENIQ database server.

    Args:
        eniq (str): The identifier of the ENIQ server ('ENIQ2' or 'ENIQ4').

    Returns:
        pyodbc.Connection or None: A connection object if successful, otherwise None.
    """
    if eniq == 'ENIQ2':
        server = os.getenv('ENIQ_SERVER_2_HOST')
        password = os.getenv('ENIQ_PASSWORD_2')
    elif eniq == 'ENIQ4':
        server = os.getenv('ENIQ_SERVER_4_HOST')
        password = os.getenv('ENIQ_PASSWORD_4')
    else:
        return None
    user_id = os.getenv('ENIQ_USER_ID')
    db = os.getenv('ENIQ_DB')
    port = os.getenv('ENIQ_SERVER_PORT')
    driver = 'FreeTDS'
    try:
        conn = pyodbc.connect(
            driver=driver,
            server=server,
            TDS_Version='4.2',
            database=db,
            port=port,
            UID=user_id,
            password=password,
        )
    except pyodbc.DatabaseError as exc:
        logger.error(f"Ошибка подключения к {eniq}: {exc}")
        return None

    return conn
