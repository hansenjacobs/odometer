from typing import Dict, List


def next_combination(current_values: Dict[str, any], dials: Dict[str, List[any]]) -> Dict[str, any]:
    """
    Calculate the next combination of values for an odometer-like system.
    This function simulates the behavior of an odometer, where each "dial" can take on a set of prefedined values. It
    increments least significant dial and carries over to more siginifcant dials as needed. Optionally, it can also add
    skipped dials to the the result.
    Args:
        current_values (Dict[str, any]): A dictionary representing the current state of the odometer, where keys are
            dial names and values are the current values of those dials.
        dials (Dict[str, List[any]]): A dictionary defining the possible values for each dial, where keys are dial
            names and values are lists of possible values for those dials.
        add_skipped_dials (bool, optional): If True, any dials that are skipped (i.e., not present in current_values)
            will be added to the result with their least siginificant value. Defaults to False.
    Returns:
        Dict[str, any]: A dictionary representing the next combination of values for the odometer.
        If all combinations are exhausted, it returns None.
    Example:
        current_values = {'section': 100, 'row': 'B', 'seat': 3}
        dials = {
            'section': [100, 101, 102],
            'row': ['A', 'B', 'C'],
            'seat': [1, 2, 3]
        }
        next_combination(current_values, dials)
        # Return: {'section': 100, 'row': 'C', 'seat': 1}
    """
    new_values = current_values.copy()
    carry_increment = True

    for field in reversed(dials.keys()):
        if field not in new_values:
            continue

        if carry_increment:
            dial = dials[field]
            current_value = new_values[field]
            current_index = dial.index(current_value)
            if current_index + 1 < len(dial):
                new_values[field] = dial[current_index + 1]
                carry_increment = False
            else:
                new_values[field] = dial[0]
                carry_increment = True
        else:
            break

    # If carry_increment is still True, all combinations have been exhausted
    return None if carry_increment else new_values
