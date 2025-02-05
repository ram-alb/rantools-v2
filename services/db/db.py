import os
from contextlib import AbstractContextManager
from typing import Any, List, Optional, Union

import cx_Oracle  # type: ignore
import oracledb  # type: ignore

ATOLL_HOST = os.getenv('ATOLL_HOST')
ATOLL_PORT = os.getenv('ATOLL_PORT')
SERVICE_NAME = os.getenv('SERVICE_NAME')
ATOLL_LOGIN = os.getenv('ATOLL_LOGIN')
ATOLL_PASSWORD = os.getenv('ATOLL_PASSWORD')

Connection = Union[cx_Oracle.Connection, oracledb.Connection]


def _get_cx_oracle_connection() -> cx_Oracle.Connection:
    """Create a connection to the database using the cx_Oracle library."""
    dsn = cx_Oracle.makedsn(
        ATOLL_HOST,
        ATOLL_PORT,
        service_name=SERVICE_NAME,
    )
    return cx_Oracle.connect(
        user=ATOLL_LOGIN,
        password=ATOLL_PASSWORD,
        dsn=dsn,
    )


def _get_oracledb_connection() -> oracledb.Connection:
    """Create a connection to the database using the oracledb library."""
    dsn = f'{ATOLL_HOST}:{ATOLL_PORT}/{SERVICE_NAME}'

    return oracledb.connect(
        user=ATOLL_LOGIN,
        password=ATOLL_PASSWORD,
        dsn=dsn,
    )


class DbConnection(AbstractContextManager):
    """Context manager for handling database connections."""

    def __init__(self, db_type: str):
        """Initialize the DbConnection instance with the specified database type."""
        self.db_type = db_type
        self.connection = None

    def __enter__(self) -> Connection:
        """Open a database connection based on the specified db_type."""
        connectors = {
            'cx_oracle': _get_cx_oracle_connection,
            'oracledb': _get_oracledb_connection,
        }

        connection_func = connectors.get(self.db_type)
        if connection_func is None:
            raise ValueError(f'Wrong DB type: {self.db_type}')

        self.connection = connection_func()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection when exiting the context."""
        if self.connection is not None:
            self.connection.close()


def select(
    connection: Connection,
    sql_select: str,
    sql_params: Optional[Union[list, tuple, dict]] = None,
    row_factory: Any = None,
    batch_size: int = 10000,
) -> List[Any]:
    """Execute a SELECT SQL query and returns the result as a list of row factory."""
    with connection.cursor() as cursor:
        cursor.execute(sql_select, sql_params)
        if row_factory is not None:
            cursor.rowfactory = row_factory

        rows = []
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            rows.extend(batch)

    return rows
