
import scally.notes as notes
# from scally.notes import (C, Cs, D, Ds, E, F, G, Gs, A, As, B)
__all__ = []

for pc in notes.PITCH_CLASSES:
    name = str(pc)
    globals()[name] = pc
    __all__.append(name)


for name in notes._NOTES_BY_NAME:
    n = notes._NOTES_BY_NAME[name]
    globals()[name] = n
    __all__.append(name)

