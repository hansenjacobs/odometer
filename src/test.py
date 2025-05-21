from odometer import Dial, Odometer

dials = [
    Dial('section', [100, 101, 102]),
    Dial('row', ['A', 'B', 'C']),
    Dial('seat', [1, 2, 3])
]

odo = Odometer(dials)
print(odo.current_values)
odo.increment()
print(odo.current_values)
odo.increment()
print(odo.current_values)