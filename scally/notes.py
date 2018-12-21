import math

class Note:

    def __init__(self, name, interval, octave):
        super().__init__()
        self._name = name
        self._interval = interval
        self._octave = octave
        self._bemole = False
        if len(self.name) > 1:
            self._bemole = self._name[1] == "b"

    @property
    def interval(self):
        return self._interval

    @property
    def name(self):
        return self._name

    @property
    def octave(self):
        return self._octave

    @property
    def bemole(self):
        return self._bemole

    @property
    def semitones_from_C0(self):
        return OCTAVE_SEMITONES * self.octave + self.interval

    def to_bemole(self):
        return note(notename(self, True))

    def to_sharp(self):
        return note(notename(self, False))

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False

        return self.octave == other.octave and self.interval == other.interval

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, Note):
            raise ValueError("Illegal comparison with note")
        return self.octave <= other.octave and self.interval < other.interval

    def __le__(self, other):
        if not isinstance(other, Note):
            raise ValueError("Illegal comparison with note")
        return self.octave <= other.octave and self.interval <= other.interval

    def __gt__(self, other):
        if not isinstance(other, Note):
            raise ValueError("Illegal comparison with note")
        return self.octave >= other.octave and self.interval > other.interval

    def __ge__(self, other):
        if not isinstance(other, Note):
            raise ValueError("Illegal comparison with note")
        return self.octave >= other.octave and self.interval >= other.interval

    def __str__(self):
        return "%s%d" % (self.name, self.octave)

    def __repr__(self):
        return self.__str__()

    def __add__(self, interval):
        if not isinstance(interval, int):
            raise ValueError("int expected")
        new_interval = self.interval + interval
        if new_interval < OCTAVE_SEMITONES:
            return note_by_interval(new_interval, self.octave)
        else:
            octave, new_interval = _move_octave(self.octave, new_interval)
            return note_by_interval(new_interval, octave)


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

C = 0
Cs = 1
Db = 1
D = 2
Ds = 3
Eb = 3
E = 4
F = 5
Fs = 6
Gb = 6
G = 7
Gs = 8
Ab = 8
A = 9
As = 10
Bb = 10
B = 11

_BEMOLES = [Db, Eb, Gb, Ab, Bb]


# semitones in OCTAVE
OCTAVE_SEMITONES = 12

OCTAVE_COUNT = 10

_NAMES = {}

_NAMES[C] = "C"
_NAMES[Cs] = ("Cs", "Db")
_NAMES[D] = "D"
_NAMES[Ds] = ("Ds", "Eb")
_NAMES[E] = "E"
_NAMES[F] = "F"
_NAMES[Fs] = ("Fs", "Gb")
_NAMES[G] = "G"
_NAMES[Gs] = ("Gs", "Ab")
_NAMES[A] = "A"
_NAMES[As] = ("As", "Bb")
_NAMES[B] = "B"


_INTERVALS = {}
for k, v in _NAMES.items():
    if isinstance(v, tuple):
        _INTERVALS[v[0]] = k
        _INTERVALS[v[1]] = k
    else:
        _INTERVALS[v] = k


def get_name_interval(name):
    return _INTERVALS[name]


def get_interval_name(interval, bemole=False):
    name = _NAMES[interval]
    if not isinstance(name, tuple):
        return name
    else:
        if bemole:
            return name[1]
        return name[0]


def notename(n, bemole=False):
    name = get_interval_name(n.interval)
    return "%s%d" % (name, n.octave)


def octave_to_semitones(octave):
    return OCTAVE_SEMITONES * octave


def _move_octave(octave, interval):
    semis = octave_to_semitones(octave) + interval
    new_octave = math.floor(semis / OCTAVE_SEMITONES)
    # print("<<", new_octave, semis)
    octave_semis = octave_to_semitones(new_octave)
    new_interval = semis - octave_semis
    # print("<1",new_octave, new_interval, semis, octave_semis)
    return (new_octave, new_interval)

# Making notes

_NOTES_BY_NAME = {}
_NOTES = []

__all__ = []

def _register_note(n):
    name = str(n)
    _NOTES_BY_NAME[name] = n
    globals()[name] = n
    __all__.append(name)


def _create_notes():
    for octave_number in range(OCTAVE_COUNT):
        _NOTES.append([])
        for interval in range(0, OCTAVE_SEMITONES, 1):
            name = get_interval_name(interval)
            # sharp 
            n = Note(name, interval, octave_number)
            # print(i, o, n)
            _NOTES[octave_number].append(n)
            _register_note(n)

            # bemole 
            if interval in _BEMOLES:
                nameb = get_interval_name(interval, True)
                nb = Note(nameb, interval, octave_number)
                _register_note(nb)

_create_notes()

# print(globals())

# getters / or kindof constructors
def note(name, octave=None):
    if octave is not None:
        interval = get_name_interval(name)
        return note_by_interval(interval, octave)
    else:
        return _NOTES_BY_NAME[name]


def note_by_interval(interval, octave):
    if interval > OCTAVE_SEMITONES:
        raise ValueError("Wrong note interval")

    return _NOTES[octave][interval]


def note_by_semitones(semitones):
    octave, new_interval = _move_octave(0, semitones)
    return note_by_interval(new_interval, octave)


def notes_from_octave(n):
    if n >= OCTAVE_COUNT or n < 0:
        raise ValueError("Wrong octave")
    return list(iter(_NOTES[n]))

if __name__ == "__main__":
    n = note(CID, 3)
    print(n)
    n2 = n + 10
    print(n2)
    n3 = n + 13
    print(n3)
    n4 = n + OCTAVE_SEMITONES * 10
    print(n4)
