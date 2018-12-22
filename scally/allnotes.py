__all__ = []

import scally.notes as notes

for name in notes._NOTES_BY_NAME:
    n = notes._NOTES_BY_NAME[name]
    globals()[name] = n
    __all__.append(name)

