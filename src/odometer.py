from typing import Any, Dict, Iterator, List, Union


def next_combination(current_values: Dict[str, Any], dials: Dict[str, List[Any]]) -> Dict[str, Any]:
    """
    Calculate the next combination of values for an odometer-like system.
    This function simulates the behavior of an odometer, where each "dial" can take on a set of prefedined values. It
    increments least significant dial and carries over to more siginifcant dials as needed. Optionally, it can also add
    skipped dials to the the result.
    Args:
        current_values (Dict[str, Any]): A dictionary representing the current state of the odometer, where keys are
            dial names and values are the current values of those dials.
        dials (Dict[str, List[Any]]): A dictionary defining the possible values for each dial, where keys are dial
            names and values are lists of possible values for those dials.
        add_skipped_dials (bool, optional): If True, any dials that are skipped (i.e., not present in current_values)
            will be added to the result with their least siginificant value. Defaults to False.
    Returns:
        Dict[str, Any]: A dictionary representing the next combination of values for the odometer.
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
            # If a dial is not in current_values, skip it
            continue

        if carry_increment:
            dial = dials[field]
            if len(dial) < 1:
                raise ValueError(f"Dial '{field}' has no values defined.")
            current_value = new_values[field]
            if current_value not in dial:
                raise ValueError(f"Invalid value for '{field}' dial: {current_value}")
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


class Dial:
    def __init__(self, name: str, values: List[Any]):
        if not name:
            raise ValueError('Dial name cannot be emtpy.')
        if not values:
            raise ValueError(f'Dial values for {name} dial cannot be empty.')
        if not isinstance(values, list):
            raise TypeError(f'Dial values for {name} dial must be a list.')
        
        self.name = name
        self.values = values
        self.current_index = 0

    def __len__(self):
        return len(self.values)

    @property
    def current_value(self):
        return self.values[self.current_index]
    
    def increment(self):
        carry = False       # Should the increment carry over to the next dial?
        if self.current_index + 1 < len(self.values):
            self.current_index += 1
        else:
            self.current_index = 0
            carry = True
        return carry


class Odometer:
    def __init__(self, dials: Union[Dict[str, List[Any]], List[Dial]]):
        self._exhausted = False
        self.dials = {}
        if isinstance(dials, dict):
            self._create_dials_from_dict(dials)
        elif isinstance(dials, list):
            self._create_dials_from_list(dials)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        return self
    
    def __next__(self) -> Dict[str, Any]:
        if self._exhausted:
            raise StopIteration
        result = self.current_values
        self._increment()
        return result
            
    def _create_dials_from_dict(self, dials: Dict[str, List[Any]]):
        for name, values in dials.items():
            self.dials[name] = Dial(name, values)

    def _create_dials_from_list(self, dials: List[Dial]):
        for index, dial in enumerate(dials):
            if not isinstance(dial, Dial):
                raise TypeError(f'Invalid dial type at index {index}. Expected Dial instance.')
        self.dials = {dial.name: dial for dial in dials}

    def _increment(self):
        if not self._exhausted:
            carry = True
            for dial_name in reversed(self.dials.keys()):
                if carry:
                    carry = self.dials[dial_name].increment()
                else:
                    break
            # If carry is still True, all combinations have been exhausted
            self._exhausted = carry

    @property
    def current_values(self):
        if self._exhausted:
            retval = None
        else:
            retval = {name: dial.current_value for name, dial in self.dials.items()}
        return retval

    def increment(self):
        self._increment()
        return self.current_values
    
    def reset(self):
        self._exhausted = False
        for dial in self.dials.values():
            dial.current_index = 0
        return self.current_values
