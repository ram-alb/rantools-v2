import os

from ldap3 import Connection, Server
from ldap3.core.exceptions import LDAPBindError


def is_ldap_bind(email, password):
    """Authenticate a user against an LDAP server."""
    server = Server(os.getenv('LDAP_URL'))
    conn = Connection(
        server,
        email,
        password=password,
    )
    try:
        is_bind = conn.bind()
    except LDAPBindError:
        is_bind = False
    return is_bind
