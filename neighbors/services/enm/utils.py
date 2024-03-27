import os


def get_enm_server(enm: str) -> str:
    """Get enm server's environment variable value."""
    if enm == 'ENM2':
        enm_server = os.getenv('ENM_SERVER_2')
    elif enm == 'ENM4':
        enm_server = os.getenv('ENM_SERVER_4')

    if enm_server is None:
        raise ValueError(f'No {enm_server} environment variable')

    return enm_server
