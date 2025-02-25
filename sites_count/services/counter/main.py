from sites_count.services.counter.db_updater import add_region_operator_counts, add_site_counts
from sites_count.services.counter.site_counter import count_sites
from sites_count.services.counter.sql import select_from_network_live


def update_site_counts():
    """Update site counts."""
    selected_nl_data = select_from_network_live()
    site_counts = count_sites(selected_nl_data)

    add_site_counts(
        site_counts.operator.counts,
        site_counts.operator.total,
        'operator',
    )

    add_site_counts(
        site_counts.vendor.counts,
        site_counts.vendor.total,
        'vendor',
    )

    add_site_counts(
        site_counts.region.counts,
        site_counts.region.total,
        'region',
    )

    add_region_operator_counts(
        site_counts.operator_region.counts,
        site_counts.operator_region.total,
    )
