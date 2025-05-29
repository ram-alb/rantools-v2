tools = {
    'BTS Info': {'url': 'bts-info', 'icon': 'fas fa-broadcast-tower'},
    'Sites Count': {'url': 'sites_count', 'icon': 'fas fa-calculator'},
    'BTS Files': {'url': 'bts-files', 'icon': 'fas fa-file-export'},
    'KML Files': {'url': 'bts-files-kml', 'icon': 'fas fa-file-export'},
    'Network Live': {'url': 'nl-index', 'icon': 'fas fa-signal'},
    'Neighbors': {'url': 'nbr-index', 'icon': 'fas fa-link'},
    'TR Data': {'url': 'tr-data-index', 'icon': 'fas fa-network-wired'},
    'HW Info': {'url': 'hw-info-index', 'icon': 'fas fa-warehouse'},
    'DayX': {'url': 'dayX', 'icon': 'fa fa-user-secret'},
    'API Docs': {'url': 'api-docs', 'icon': 'fas fa-book'},
    'RetSubUnit': {'url': 'retsubunit_index', 'icon': 'fas fa-sort-amount-down'},
    'Network vs Atoll': {'url': 'network_vs_atoll', 'icon': 'fas fa-not-equal'},
    'Submit TOA': {'url': 'search_form', 'icon': 'fas fa-book'},
}

group_tools = {
    'Regular Users': ['BTS Info', 'Sites Count'],
    'RNPO Users': [
        'BTS Files',
        'Network Live',
        'Neighbors',
        'TR Data',
        'HW Info',
        'API Docs',
        'RetSubUnit',
        'Network vs Atoll',
    ],
    'Hardware': ['HW Info'],
    'BTS Files': ['BTS Files'],
    'DayX': ['DayX'],
    'Partial Access Users': ['KML Files'],
    'Trans Group': ['TR Data'],
    'Rollout': ['TR Data'],
    'Integration Team': ['Submit TOA'],
}


def user_tools(request):
    """Context processor that passes available tools to base.html."""
    if not request.user.is_authenticated:
        return {'tools': {}}

    user_groups = request.user.groups.values_list('name', flat=True)

    allowed_tools = set()
    for group in user_groups:
        allowed_tools.update(group_tools[group])

    return {
        'tools': {tool: tools[tool] for tool in sorted(allowed_tools)},
    }
