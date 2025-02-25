import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Dict, List, Set, Tuple


def _extract_site_id(sitename: str, operator: str) -> str:
    """Extract site id from sitename."""
    if operator != 'Kcell':
        return sitename

    site_id_obj = re.search(r'\d{5}', sitename)
    if site_id_obj:
        return site_id_obj.group()

    return sitename


def _nested_defaultdict() -> DefaultDict[str, DefaultDict[str, int]]:
    return defaultdict(lambda: defaultdict(int))


@dataclass
class CountData:
    """Dataclass for counting sites."""

    uniq_ids: defaultdict = field(default_factory=lambda: defaultdict(set))
    counts: defaultdict = field(default_factory=_nested_defaultdict)
    total: Dict[str, int] = field(default_factory=dict)


@dataclass
class SiteCounter:
    """Dataclass for counting sites."""

    operator: CountData = field(default_factory=CountData)
    vendor: CountData = field(default_factory=CountData)
    region: CountData = field(default_factory=CountData)
    operator_region: CountData = field(default_factory=CountData)


def _update_counts(
    tech_uniq_ids: Dict[str, Set[str]],
    tech: str,
    category: CountData,
    key: str,
    site_id: str,
) -> None:
    """Update counts for a given category."""
    if site_id not in tech_uniq_ids[key]:
        tech_uniq_ids[key].add(site_id)
        category.uniq_ids[key].add(site_id)
        category.counts[tech][key] += 1


def _process_site_entry(
    site_counts: SiteCounter,
    tech_uniq_ids: Dict[str, Set[str]],
    tech: str,
    row: Tuple[str, str, str, str],
) -> None:
    """Process a site entry."""
    operator, site, vendor, region = row
    site_id = _extract_site_id(site, operator)

    _update_counts(tech_uniq_ids, tech, site_counts.operator, operator, site_id)
    _update_counts(tech_uniq_ids, tech, site_counts.vendor, vendor, site_id)

    if region:
        _update_counts(tech_uniq_ids, tech, site_counts.region, region, site_id)
        key = f'{operator}:{region}'
        _update_counts(tech_uniq_ids, tech, site_counts.operator_region, key, site_id)


def _compute_totals(count_data: CountData) -> None:
    """Compute total counts."""
    count_data.total = {
        name: len(site_ids) for name, site_ids in count_data.uniq_ids.items()
    }


def count_sites(selected_nl_data: Dict[str, List[tuple]]) -> SiteCounter:
    """Count the number of sites by operators, vendors, and regions."""
    site_counts = SiteCounter()

    for tech, nl_data in selected_nl_data.items():
        tech_uniq_ids: DefaultDict[str, Set[str]] = defaultdict(set)
        for row in nl_data:
            _process_site_entry(site_counts, tech_uniq_ids, tech, row)

    _compute_totals(site_counts.operator)
    _compute_totals(site_counts.vendor)
    _compute_totals(site_counts.region)
    _compute_totals(site_counts.operator_region)

    return site_counts
