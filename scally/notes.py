import math

#############################################################
# CLASSES
#############################################################


def assure_int(func):
    def wrapper(self, *args):
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError("int expected")
        return func(self, *args)
    return wrapper


def assure_note(func):
    def wrapper(self, arg):
        if not isinstance(arg, Note):
            raise TypeError("note expected got %s" % str(type(arg)))
        return func(self, arg)
    return wrapper


def assure_pc(func):
    def wrapper(self, arg):
        if not isinstance(arg, PitchClass):
            raise TypeError("base note expected got %s" % str(type(arg)))
        return func(self, arg)
    return wrapper


class PitchClass:

    def __init__(self, names, value):
        super().__init__()
        if isinstance(names, str):
            names = (names, None, None)
        elif len(names) != 2:
            raise ValueError("Wrong pc names")
        else:
            # normal name same as sharp name
            names = (None, names[0], names[1])
        self.names = names
        self.value = value

    def __hash__(self):
        return self.value

    def has_bemole(self):
        return self.names[BEMOLE] is not None

    def has_sharp(self):
        return self.names[SHARP] is not None

    def get_name(self, notation):
        return self.names[notation]

    def has_note(self, note):
        return note.pc == self

    def foroctave(self, octave):
        return note_by_pc(self, octave)

    @property
    def name(self):
        return self.get_name(NATURAL)

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
        new_pc = self.value + num
        new_pc = new_pc % 12
        return get_pc(new_pc)

    def __sub__(self, num):
        if isinstance(num, int):
            new_pc = self.value - num
            new_pc = new_pc % 12
            return get_pc(new_pc)
        elif isinstance(num, PitchClass):
            new_pc = self.value - num.value
            return new_pc
        else:
            raise TypeError("PitchClass or int expected")


    def __rsub__(self, num):
        raise ValueError("Invalid operation use PitchClass as left operand of a __sub__")

    def __eq__(self, other):
        if not isinstance(other, PitchClass):
            return False

        # print("__EQ__", self, other, self.value, other.value)
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    @assure_pc
    def __lt__(self, other):
        return self.value < other.value

    @assure_pc
    def __le__(self, other):
        return self.value <= other.value

    @assure_pc
    def __gt__(self, other):
        return self.value > other.value

    @assure_pc
    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        if self.has_sharp():
            return self.get_name(SHARP)
        return self.get_name(NATURAL)

    def __repr__(self):
        return str(self)


class Note:

    def __init__(self, pc, octave, notation):
        super().__init__()
        self._pc = pc
        self._octave = octave
        self._notation = notation
        self._semitones_from_C0 = OCTAVE_SEMITONES * self.octave + self.value

    def kindof(self, pc):
        return self.pc == pc

    @property
    def pc(self):
        return self._pc

    @property
    def value(self):
        return self._pc.value

    @property
    def name(self):
        return self._pc.get_name(self.notation)

    @property
    def octave(self):
        return self._octave

    @property
    def notation(self):
        return self._notation

    @property
    def semitones_from_C0(self):
        return self._semitones_from_C0

    def has_bemole(self):
        return self.pc.has_bemole()

    def to_bemole(self):
        name = self.pc.bemole_name
        return note(name, self.octave)

    def to_sharp(self):
        name = self.pc.sharp_name
        return note(name, self.octave)

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False

        return self.octave == other.octave and self.pc == other.pc

    def __ne__(self, other):
        return not self.__eq__(other)

    @assure_note
    def __lt__(self, other):
        return self.octave <= other.octave and self.pc < other.pc

    @assure_note
    def __le__(self, other):
        return self.octave <= other.octave and self.pc <= other.pc

    @assure_note
    def __gt__(self, other):
        return self.octave >= other.octave and self.pc > other.pc

    @assure_note
    def __ge__(self, other):
        return self.octave >= other.octave and self.pc >= other.pc

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
            raise TypeError("int or note expected")

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


#############################################################
# GLOBAL STATE AND CONSTANTS
#############################################################


NATURAL = 0
SHARP = 1
BEMOLE = 2

# normal name same as sharp name for altered degrees
NOTATIONS = [NATURAL, SHARP, BEMOLE]

# Making notes
C = PitchClass("C", 0)
Cs = PitchClass(("Cs", "Db"), 1)
D = PitchClass("D", 2)
Ds = PitchClass(("Ds", "Eb"), 3)
E = PitchClass("E", 4)
F = PitchClass("F", 5)
Fs = PitchClass(("Fs", "Gb"), 6)
G = PitchClass("G", 7)
Gs = PitchClass(("Gs", "Ab"), 8)
A = PitchClass("A", 9)
As = PitchClass(("As", "Bb"), 10)
B = PitchClass("B", 11)


PITCH_CLASSES = [C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B]
# PITCH_CLASS_NAMES = [pc.name for pc in PITCH_CLASSES]

_PITCH_CLASSES_MAPPING = {}
for note in PITCH_CLASSES:
    for name in note.names:
        _PITCH_CLASSES_MAPPING[name] = note

# semitones in OCTAVE
OCTAVE_SEMITONES = 12

# ten octaves from c0 to c9
OCTAVE_COUNT = 10

# dictionary with all notes
# sharps and bemoles represented as different notes with same pitch class
_NOTES_BY_NAME = {}

# list of all unique notes (bemoles are ommitted)
_NOTES = []


def _create_notes():
    def _register_note(pc, octave_number, notation, is_main_note):
        n = Note(pc, octave_number, notation)
        _NOTES_BY_NAME[str(n)] = n
        if is_main_note:
            _NOTES[octave_number].append(n)

    for octave_number in range(OCTAVE_COUNT):
        _NOTES.append([])
        for pc in PITCH_CLASSES:
            if pc.has_bemole():
                _register_note(pc, octave_number, SHARP, True)
                _register_note(pc, octave_number, BEMOLE, False)
            else:
                _register_note(pc, octave_number, NATURAL, True)
_create_notes()

#############################################################
# API
#############################################################


def semitones_to_tones(n):
    return n / 2.0


def tones_to_semitones(n):
    return n * 2.0


def get_pc_by_name(name):
    return _PITCH_CLASSES_MAPPING[name]


def octave_to_semitones(octave):
    return OCTAVE_SEMITONES * octave

# getters / kindof constructors


def note(name, octave=None):
    if octave is not None:
        base = get_pc_by_name(name)
        return note_by_pc(base, octave)
    else:
        return _NOTES_BY_NAME[name]


def note_by_pc(pc, octave):
    return _NOTES[octave][pc.value]


def note_by_semitones(semitones):
    octave = math.floor(semitones / OCTAVE_SEMITONES)
    octave_semis = octave_to_semitones(octave)
    value = semitones - octave_semis
    pc = PITCH_CLASSES[value]
    return note_by_pc(pc, octave)


def notes_from_octave(n):
    if n >= OCTAVE_COUNT or n < 0:
        raise ValueError("Wrong octave")
    return list(iter(_NOTES[n]))

def has_pc(name):
    for pc in pcs:
        if pc.has_name(name):
            return True
    return False

def get_pc(number):
    number = number % len(PITCH_CLASSES)
    return PITCH_CLASSES[number]