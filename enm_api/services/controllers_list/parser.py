from typing import Dict, List

from enmscripting import ElementGroup  # type: ignore


def _parse_element_group(element_group: ElementGroup) -> List[str]:
    """Parse the given ElementGroup object to extract NodeIds."""
    parsing_results = []
    table = element_group.groups()[0]
    for row in table:
        node_id = row.find_by_label('NodeId')[0].value()
        parsing_results.append(node_id)
    return sorted(parsing_results)


def parse_controllers(enm_data: Dict[str, ElementGroup]) -> Dict[str, List[str]]:
    """Parse the controllers from the given dictionary of ElementGroups."""
    return {
        controller_type: _parse_element_group(element_group)
        for controller_type, element_group in enm_data.items()
    }
