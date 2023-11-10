import json
import random
from typing import Dict, List, Optional


def partner_in_previous_assignments(name: str, partner: str, previous_assignments: Optional[List[Dict[str, str]]]):
    for previous_assignment in previous_assignments:
        if (name, partner) in previous_assignment.items():
            return True

    return False


def get_possible_partners(
    name: str,
    groups: List[List[str]],
    assignments: Dict[str, str],
    previous_assignments: Optional[List[Dict[str, str]]],
) -> List[str]:
    names = []
    for group in groups:
        if name in group:
            continue

        for partner in group:
            if partner not in assignments.values() and not partner_in_previous_assignments(
                name, partner, previous_assignments
            ):
                names.append(partner)

    random.shuffle(names)
    return names


def get_possible_names(groups: List[List[str]], assignments: Dict[str, str]) -> List[str]:
    names = []
    for group in groups:
        for name in group:
            if name not in assignments.keys():
                names.append(name)

    random.shuffle(names)
    return names


def secret_santa(
    groups: List[List[str]],
    assignments: Optional[Dict[str, str]] = None,
    previous_assignments: Optional[List[Dict[str, str]]] = None,
) -> Optional[Dict[str, str]]:
    if not assignments:
        assignments = {}
    if not previous_assignments:
        previous_assignments = []

    names = get_possible_names(groups, assignments)
    for name in names:
        possible_partners = get_possible_partners(name, groups, assignments, previous_assignments)
        if not possible_partners:
            return None

        for partner in possible_partners:
            assignments[name] = partner
            if not secret_santa(groups, assignments, previous_assignments):
                del assignments[name]
            else:
                return assignments

        if name not in assignments:
            return None

    assert assignments is not None
    assert_no_duplications(assignments)
    assert_all_assigned(groups, assignments)
    assert_not_in_same_group(groups, assignments)
    assert_partner_not_in_previous_assignment(assignments, previous_assignments)
    return assignments


def assert_no_duplications(assignments: Optional[Dict[str, str]]) -> None:
    assert len(assignments.keys()) == len(set(assignments.keys()))
    assert len(assignments.values()) == len(set(assignments.values()))


def assert_all_assigned(groups: List[List[str]], assignments: Optional[Dict[str, str]]) -> None:
    for group in groups:
        for name in group:
            assert name in assignments.keys() and name in assignments.values()


def assert_not_in_same_group(groups: List[List[str]], assignments: Optional[Dict[str, str]]) -> None:
    for name, partner in assignments.items():
        for group in groups:
            if name in group or partner in group:
                assert not (name in group and partner in group)


def assert_partner_not_in_previous_assignment(
    assignments: Optional[Dict[str, str]], previous_assignments: Optional[List[Dict[str, str]]]
) -> None:
    for name, partner in assignments.items():
        assert not partner_in_previous_assignments(name, partner, previous_assignments)


if __name__ == "__main__":
    groups = [
        ["PersonA", "PersonB"],
        ["PersonC", "PersonD"],
    ]
    previous_assignments = []
    res = set()
    for i in range(5000):
        assignments = secret_santa(groups, previous_assignments=previous_assignments)
        res.add(json.dumps(assignments, sort_keys=True))

    # print(json.loads(res[0]))
    print(res)
    print(f"# of possibilities: {len(set(res))}")
