enms = {
    'ENM_2': 'ENM_SERVER_2',
    'ENM_4': 'ENM_SERVER_4',
}


def get_enm_server(enm: str) -> str:
    """Get enm server's environment variable value."""
    enm_server = enms.get(enm)

    if enm_server is None:
        valid_options = ', '.join(enms.keys())
        raise ValueError(
            f'No configuration found for ENM identifier: {enm}. Valid options are: {valid_options}',
        )

    return enm_server
