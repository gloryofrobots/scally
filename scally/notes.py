import math


def assure_int(func):
    def wrapper(self, *args):
        for arg in args:
            if not isinstance(arg, int):
                raise ValueError("int expected")
        return func(self, *args)
    return wrapper


def assure_note(func):
    def wrapper(self, arg):
        if not isinstance(arg, Note):
            raise ValueError("note expected got %s" % str(type(arg)))
        return func(self, arg)
    return wrapper

def assure_base(func):
    def wrapper(self, arg):
        if not isinstance(arg, Base):
            raise ValueError("base note expected got %s" % str(type(arg)))
        return func(self, arg)
    return wrapper

NORMAL = 0
SHARP = 1
BEMOLE = 2

# normal name same as sharp name for altered degrees 
NOTATIONS = [NORMAL, SHARP, BEMOLE]

class Base:
    def __init__(self, names, value):
        super().__init__()
        if isinstance(names, str):
            names = (names, names, names)
        elif len(names) != 2:
            raise ValueError("Wrong basenote names")
        else:
            # normal name same as sharp name
            names = (names[0], names[0], names[1]) 
        assert(len(names) < 3, "Wrong basenote names")
        self.names = names
        self.value = value

    def has_bemole(self):
        return self.names[BEMOLE] != None

    def has_sharp(self):
        return self.names[SHARP] != None

    def get_name(self, notation):
        return self.names[notation]
        
    @property
    def name(self):
        return self.get_name(NORMAL)

    @property
    def sharp_name(self):
        return self.get_name(SHARP)

    @property
    def bemole_name(self):
        return self.get_name(BEMOLE)
            
    @assure_int
    def __radd__(self, interval):
        return self.__add__(interval)

    @assure_int
    def __add__(self, num):
        return self.value + num

    @assure_int
    def __sub__(self, num):
        return self.value - num

    @assure_int
    def __rsub__(self, num):
        return num - self.value

    def __eq__(self, other):
        if not isinstance(other, Base):
            return False

        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    @assure_base
    def __lt__(self, other):
        return self.value < other.value

    @assure_base
    def __le__(self, other):
        return self.value <= other.value

    @assure_base
    def __gt__(self, other):
        return self.value > other.value

    @assure_base
    def __ge__(self, other):
        return self.value >= other.value


class Note:

    def __init__(self, base, octave, notation):
        super().__init__()
        self._base = base
        self._octave = octave
        self._notation = notation
        self._semitones_from_C0 = OCTAVE_SEMITONES * self.octave + self.value

    @property
    def basenote(self):
        return self._base

    @property
    def value(self):
        return self._base.value

    @property
    def name(self):
        return self._base.get_name(self.notation)

    @property
    def octave(self):
        return self._octave

    @property
    def notation(self):
        return self._notation

    @property
    def semitones_from_C0(self):
        return self._semitones_from_C0

    def to_bemole(self):
        name = self.basenote.bemole_name
        return note(name, self.octave)

    def to_sharp(self):
        name = self.basenote.sharp_name
        return note(name, self.octave)

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False

        return self.octave == other.octave and self.basenote == other.basenote

    def __ne__(self, other):
        return not self.__eq__(other)

    @assure_note
    def __lt__(self, other):
        return self.octave <= other.octave and self.basenote < other.basenote

    @assure_note
    def __le__(self, other):
        return self.octave <= other.octave and self.basenote <= other.basenote

    @assure_note
    def __gt__(self, other):
        return self.octave >= other.octave and self.basenote > other.basenote

    @assure_note
    def __ge__(self, other):
        return self.octave >= other.octave and self.basenote >= other.basenote

    def __str__(self):
        return "%s%d" % (self.name, self.octave)

    def __repr__(self):
        return self.__str__()

    def __radd__(self, interval):
        return self.__add__(interval)

    def __add__(self, interval):
        return self.transpose(interval)

    def difference(self, note):
        semis0 = self.semitones_from_C0
        semis1 = note.semitones_from_C0
        return semis0 - semis1

    def __sub__(self, interval):
        if isinstance(interval, Note):
            return self.difference(interval)
        elif not isinstance(interval, int):
            raise ValueError("int or note expected")

        return self.transpose(-1 * interval)

    @assure_int
    def transpose(self, interval, octave=0):
        semis = self.semitones_from_C0
        semis += interval + (OCTAVE_SEMITONES * octave)
        return note_by_semitones(semis)

    def unison(self):
        return self

    def min2(self):
        return self + 1

    def maj2(self):
        return self + 2

    def min3(self):
        return self + 3

    def maj3(self):
        return self + 4

    def perf4(self):
        return self + 5

    def dim5(self):
        return self + 6

    def perf5(self):
        return self + 7

    def min6(self):
        return self + 8

    def maj6(self):
        return self + 9

    def min7(self):
        return self + 10

    def maj7(self):
        return self + 11

    def oct(self):
        return self + 12


def semitones_to_tones(n):
    return n / 2.0


def tones_to_semitones(n):
    return n * 2.0

C = Base("C", 0)
Cs = Base(("Cs", "Db"), 1)
D = Base("D", 2)
Ds = Base(("Ds", "Eb"), 3)
E = Base("E", 4)
F = Base("F", 5)
Fs = Base(("Fs", "Gb"), 6)
G = Base("G", 7)
Gs = Base(("Gs", "Ab"), 8)
A = Base("A", 9)
As = Base(("As", "Bb" ), 10)
B = Base("B", 11)


SCALE = [C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B]

_SCALE_MAPPING = {}
for note in SCALE:
    for name in note.names:
        _SCALE_MAPPING[name] = note

# semitones in OCTAVE
OCTAVE_SEMITONES = 12

OCTAVE_COUNT = 10


def get_base_by_name(name):
    return _SCALE_MAPPING[name]


def octave_to_semitones(octave):
    return OCTAVE_SEMITONES * octave


# Making notes

_NOTES_BY_NAME = {}
_NOTES = []

def _register_note(n):
    name = str(n)
    print(name)
    _NOTES_BY_NAME[name] = n
    globals()[name] = n
    __all__.append(name)


def _create_notes():
    for octave_number in range(OCTAVE_COUNT):
        _NOTES.append([])
        for basenote in SCALE:
            if basenote.has_bemole():
                ns = Note(basenote, octave_number, SHARP)
                _register_note(ns)
                nb = Note(basenote, octave_number, BEMOLE)
                _register_note(nb)
                _NOTES[octave_number].append(ns)
            else:
                n = Note(basenote, octave_number, NORMAL)
                _register_note(n)
                _NOTES[octave_number].append(n)
_create_notes()

# print(globals())

# getters / or kindof constructors


def note(name, octave=None):
    if octave is not None:
        base = get_base_by_name(name)
        return note_by_base(base, octave)
    else:
        return _NOTES_BY_NAME[name]


def note_by_base(base, octave):
    return _NOTES[octave][base.value]


def note_by_semitones(semitones):
    octave = math.floor(semitones / OCTAVE_SEMITONES)
    octave_semis = octave_to_semitones(octave)
    value = semitones - octave_semis
    base = SCALE[value]
    return note_by_base(base, octave)


def notes_from_octave(n):
    if n >= OCTAVE_COUNT or n < 0:
        raise ValueError("Wrong octave")
    return list(iter(_NOTES[n]))

