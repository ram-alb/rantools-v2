import os

from ldap3 import ALL, SUBTREE, Connection, Server
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


def get_unit_ldap(email, password):
    """Get the user's unit from ldap."""
    base_dn = 'dc=kcell,dc=kz'
    attr_name = 'kcellUnitNewRus'
    search_filter = f'(mail={email})'

    server = Server(host=os.getenv('LDAP_URL'), get_info=ALL)

    conn = Connection(
        server,
        email,
        password=password,
        auto_bind=True,
    )

    conn.search(
        search_base=base_dn,
        search_filter=search_filter,
        search_scope=SUBTREE,
        attributes=[attr_name],
    )

    if conn.entries:
        entry = conn.entries[0]
        try:
            unit = entry.entry_attributes_as_dict.get(attr_name, [None])[0]
        except IndexError:
            unit = None

    conn.unbind()
    return unit
