from datetime import date
from typing import Dict, Type

from django.db import transaction  # type: ignore
from django.db.models import Model  # type: ignore

from sites_count.models import (
    Operator,
    Region,
    SitesByOperator,
    SitesByOperatorAndRegion,
    SitesByRegion,
    SitesByVendor,
    Technology,
    Vendor,
)


def _update_site_counts(
    tech: str,
    site_counts: Dict[str, int],
    related_model: Type[Model],
    site_model: Type[Model],
    related_field: str,
) -> None:
    """Update site counts in the database."""
    technology = Technology.objects.get(name=tech)
    for entity_name, site_count in site_counts.items():
        related_instance = related_model.objects.get(name=entity_name)
        site_model.objects.update_or_create(
            created_at=date.today(),
            **{related_field: related_instance},
            technology=technology,
            defaults={'site_count': site_count},
        )


def add_site_counts(
    count_data: Dict[str, Dict[str, int]],
    total_data: Dict[str, int],
    model_type: str,
) -> None:
    """Add the number of sites by operators, vendors, or regions."""
    model_mapping = {
        'operator': (SitesByOperator, Operator, 'operator'),
        'vendor': (SitesByVendor, Vendor, 'vendor'),
        'region': (SitesByRegion, Region, 'region'),
    }

    site_model, related_model, related_field = model_mapping[model_type]

    with transaction.atomic():
        for tech_name, site_counts in count_data.items():
            _update_site_counts(
                tech_name,
                site_counts,
                related_model,
                site_model,
                related_field,
            )
        _update_site_counts('Total', total_data, related_model, site_model, related_field)


def _update_operator_region_counts(
    tech: str,
    site_counts: Dict[str, int],
) -> None:
    technology = Technology.objects.get(name=tech)
    for entity_key, site_count in site_counts.items():
        operator_name, region_name = entity_key.split(':')
        operator = Operator.objects.get(name=operator_name)
        region = Region.objects.get(name=region_name)
        SitesByOperatorAndRegion.objects.update_or_create(
            created_at=date.today(),
            operator=operator,
            region=region,
            technology=technology,
            defaults={'site_count': site_count},
        )


def add_region_operator_counts(
    count_data: Dict[str, Dict[str, int]],
    total_data: Dict[str, int],
) -> None:
    """Add the number of sites by the 'operator-region' combination."""
    with transaction.atomic():
        for tech_name, site_counts in count_data.items():
            _update_operator_region_counts(tech_name, site_counts)

        _update_operator_region_counts('Total', total_data)
