import os

import cx_Oracle


class DBConnector:
    """A class providing connection to Atoll db."""

    @classmethod
    def get_connection(cls):
        """Get a connection to Atoll db."""
        dsn = cx_Oracle.makedsn(
            os.getenv('ATOLL_HOST'),
            os.getenv('ATOLL_PORT'),
            service_name=os.getenv('SERVICE_NAME'),
        )
        return cx_Oracle.connect(
            user=os.getenv('ATOLL_LOGIN'),
            password=os.getenv('ATOLL_PASSWORD'),
            dsn=dsn,
        )
