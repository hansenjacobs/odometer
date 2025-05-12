import pytest
from src.odometer import next_combination


@pytest.mark.parametrize(
    "current_values, dials, expected",
    [
        (
            {'section': 100, 'row': 'A', 'seat': 1},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            {'section': 100, 'row': 'A', 'seat': 2}
        ),
        (
            {'section': 100, 'row': 'A', 'seat': 3},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            {'section': 100, 'row': 'B', 'seat': 1}
        ),
        (
            {'section': 100, 'row': 'C', 'seat': 3},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            {'section': 101, 'row': 'A', 'seat': 1}
        ),
        (
            {'section': 101, 'row': 'A', 'seat': 1},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            {'section': 101, 'row': 'A', 'seat': 2}
        ),
        (
            {'section': 101, 'row': 'B', 'seat': 1},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            {'section': 101, 'row': 'B', 'seat': 2}
        ),
        (
            {'section': 102, 'row': 'C', 'seat': 3},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            None
         ),
        (
            {'section': 100, 'seat': 1},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            {'section': 100, 'seat': 2}
         ),
        (
            {'section': 102, 'seat': 1},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            {'section': 102, 'seat': 2}
         ),
        (
            {'section': 102, 'seat': 3},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C'], 'seat': [1, 2, 3]},
            None
         ),
        (
            {'section': 100, 'row': 'A'},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C']},
            {'section': 100, 'row': 'B'}
         ),
        (
            {'section': 100, 'row': 'C'},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C']},
            {'section': 101, 'row': 'A'}
         ),
        (
            {'section': 102, 'row': 'C'},
            {'section': [100, 101, 102], 'row': ['A', 'B', 'C']},
            None
         ),
    ]
)
def test_next_combination(current_values, dials, expected):
    assert next_combination(current_values, dials) == expected, \
        f"Failed for current_values={current_values}, dials={dials}, expe-cted={expected}"
