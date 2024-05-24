import os


def get_enm_server(enm_pointer: str) -> str:
    """Get ENM server link."""
    enms = {
        'ENM_2': 'ENM_SERVER_2',
        'ENM_4': 'ENM_SERVER_4',
    }
    enm_var = enms[enm_pointer]
    enm_server = os.getenv(enm_var)
    if enm_server is None:
        raise ValueError(f'No {enm_var} environment variable')
    return enm_server
