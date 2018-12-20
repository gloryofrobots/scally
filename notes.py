import math


class _Note:

    def __init__(self, noteid, octave):
        super().__init__()
        self.nid = noteid
        self.octave = octave

    def to_semitones(self):
        return OCTAVE * self.octave + self.nid

    def __eq__(self, other):
        if not isinstance(other, _Note):
            return False

        return self.nid == other.nid

    def to_str(self, bemole=False):
        return "%s%d" % (notename(self, bemole), self.octave)

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.__str__()

    def __add__(self, interval):
        if not isinstance(interval, int):
            raise ValueError("int expected")
        noteid = self.nid + interval
        if noteid < OCTAVE:
            return note(noteid, self.octave)
        else:
            octave, noteid = move_octave(self.octave, noteid)
            return note(noteid, octave)


def unison(n):
    return n


def min2(n):
    return n + 1


def maj2(n):
    return n + 2


def min3(n):
    return n + 3


def maj3(n):
    return n + 4


def perf4(n):
    return n + 5


def dim5(n):
    return n + 6


def perf5(n):
    return n + 7


def min6(n):
    return n + 8


def maj6(n):
    return n + 9


def min7(n):
    return n + 10


def maj7(n):
    return n + 11


def oct(n):
    return n + 12


def semitones_to_tones(n):
    return n / 2.0


def tones_to_semitones(n):
    return n * 2.0

C = 0
Cs = min2(C)
Db = Cs
D = maj2(C)
Ds = min3(C)
Eb = Ds
E = maj3(C)
F = perf4(C)
Fs = dim5(C)
Gb = Fs
G = perf5(C)
Gs = min6(C)
Ab = Gs
A = maj6(C)
As = min7(C)
Bb = As
B = maj7(C)


# semitones in OCTAVE
OCTAVE = 12

MAX_OCTAVE = 10

_NAMES__ = {}

_NAMES[C] = "C"
_NAMES[Cs] = ("C#", "Db")
_NAMES[D] = "D"
_NAMES[Ds] = ("D#", "Eb")
_NAMES[E] = "E"
_NAMES[F] = "F"
_NAMES[Fs] = ("F#", "Gb")
_NAMES[G] = "G"
_NAMES[Gs] = ("G#", "Ab")
_NAMES[A] = "A"
_NAMES[As] = ("A#", "Bb")
_NAMES[B] = "B"


def notename(n, bemole=False):
    name = _NAMES[n.nid]
    if not isinstance(name, tuple):
        return name
    else:
        if bemole:
            return name[1]
        return name[0]


def octave_to_semitones(octave):
    return (OCTAVE * octave)


def move_octave(octave, interval):
    semis = octave_to_semitones(octave) + interval
    new_octave = math.floor(semis / OCTAVE)
    octave_semis = octave_to_semitones(new_octave)
    nid = semis - octave_semis
    return (new_octave, nid)

# Making notes

_NOTES_BY_NAME = {}
_NOTES = []

for o in range(MAX_OCTAVE):
    _NOTES.append([])
    for i in range(0, OCTAVE, 1):
        n = _Note(i, o)
        _NOTES[o].append(n)
        _NOTES_BY_NAME[notename(n, True)] = n
        _NOTES_BY_NAME[notename(n, False)] = n


# getters / or kindof constructors
def note_by_name(name):
    return _NOTES_BY_NAME[name]


def note(octave, nid):
    return _NOTES[octave][nid]


def note_from_semitones(semitones):
    octave, nid = move_octave(0, semitones)
    return note(octave, nid)

for o in _NOTES:
    print(o)


if __name__ == "__main__":
    n = note(C, 3)
    print(n)
    n2 = n + 10
    print(n2)
    n3 = n + 13
    print(n3)
    n4 = n + OCTAVE * 10
    print(n4)
