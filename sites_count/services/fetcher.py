from datetime import date
from typing import Dict, Type

from django.db.models import Model, QuerySet  # type: ignore

from sites_count.models import (
    SitesByOperator,
    SitesByOperatorAndRegion,
    SitesByRegion,
    SitesByVendor,
)


def _aggregate_site_counts(site_counts: QuerySet, entity_field: str) -> Dict[str, Dict[str, int]]:
    counts: Dict[str, Dict[str, int]] = {}
    totals = {}

    for row in site_counts:
        entity_name = getattr(row, entity_field).name
        technology = row.technology.name
        if entity_name not in counts:
            counts[entity_name] = {}
        counts[entity_name][technology] = row.site_count

        if technology not in totals:
            totals[technology] = 0
        totals[technology] += row.site_count

    if counts:
        counts['Total'] = totals

    return counts


def _get_site_counts(group_by: str, requested_date: date) -> Dict[str, Dict[str, int]]:
    models: Dict[str, Type[Model]] = {
        'operator': SitesByOperator,
        'vendor': SitesByVendor,
        'region': SitesByRegion,
    }

    model = models[group_by]
    site_counts = model.objects.filter(created_at=requested_date)

    return _aggregate_site_counts(site_counts, group_by)


def _get_site_counts_operator_region(
    requested_date: date,
    operator: str,
) -> Dict[str, Dict[str, int]]:
    site_counts = SitesByOperatorAndRegion.objects.filter(
        created_at=requested_date,
        operator__name=operator,
    )
    return _aggregate_site_counts(site_counts, 'region')


def fetch_site_counts(group_by: str, requested_date: date) -> Dict[str, Dict[str, int]]:
    """Return site data for a given date."""
    if group_by in {'operator', 'vendor', 'region'}:
        return _get_site_counts(group_by, requested_date)
    return _get_site_counts_operator_region(requested_date, group_by)
