import os
from typing import Union

import cx_Oracle  # type: ignore
import oracledb  # type: ignore

Connection = Union[cx_Oracle.Connection, oracledb.Connection]


class DBConnector:
    """A class to manage connections to databases."""

    atoll_host = os.getenv('ATOLL_HOST')
    atoll_port = os.getenv('ATOLL_PORT')
    service_name = os.getenv('SERVICE_NAME')
    atoll_login = os.getenv('ATOLL_LOGIN')
    atoll_password = os.getenv('ATOLL_PASSWORD')

    @classmethod
    def get_connection(cls, db_type: str) -> Connection:
        """Get a database connection based on the specified database type."""
        connectors = {
            'atoll_cx_oracle': cls._atoll_cx_oracle_connection,
            'atoll_oracledb': cls._atoll_oracledb_connection,
        }
        connection_func = connectors.get(db_type)
        if connection_func is None:
            raise ValueError(f'Wrong DB type: {db_type}')
        return connection_func()

    @classmethod
    def _atoll_cx_oracle_connection(cls) -> cx_Oracle.Connection:
        """Create a connection to the database using the cx_Oracle library."""
        dsn = cx_Oracle.makedsn(
            cls.atoll_host,
            cls.atoll_port,
            service_name=cls.service_name,
        )
        return cx_Oracle.connect(
            user=cls.atoll_login,
            password=cls.atoll_password,
            dsn=dsn,
        )

    @classmethod
    def _atoll_oracledb_connection(cls) -> oracledb.Connection:
        """Create a connection to the database using the oracledb library."""
        dsn = f'{cls.atoll_host}:{cls.atoll_port}/{cls.service_name}'

        return oracledb.connect(
            user=cls.atoll_login,
            password=cls.atoll_password,
            dsn=dsn,
        )
