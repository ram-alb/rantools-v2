import os
import subprocess

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


def is_member_pou(email):
    """Authenticate a user against an LDAP server."""
    ldap_url = os.getenv('LDAP_URL')
    super_user = os.getenv('LDAP_USER')
    super_password = os.getenv('LDAP_PASSWORD')
    base_dn = 'DC=kcell,DC=kz'
    user = email.split('@')[0]
    group_name = 'NDS-RNPOU'

    ldapsearch_cmd = [
        'ldapsearch',
        '-v',
        '-x',
        '-D',
        super_user,
        '-w',
        super_password,
        '-b',
        base_dn,
        '-H',
        ldap_url,
        '-LLL',
        '-o',
        'ldif-wrap=no',
        f'sAMAccountName={user}',
        'memberOf',
    ]

    try:
        answer = subprocess.run(ldapsearch_cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        return False

    return group_name in answer.stdout
