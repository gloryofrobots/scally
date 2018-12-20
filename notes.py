import math


class _Note:

    def __init__(self, octave, noteid, bemole=False):
        super().__init__()
        self._nid = noteid
        self._octave = octave
        self._bemole = bemole

    @property
    def nid(self):
        return self._nid

    @property
    def octave(self):
        return self._octave

    @property
    def bemole(self):
        return self._bemole

    @property
    def semitones_from_C0(self):
        return OCTAVE * self.octave + self.nid

    def bemole_sharp(self):
        return note_by_name(notename(self, not self.bemole))

    def to_bemole(self):
        return note_by_name(notename(self, True))

    def to_sharp(self):
        return note_by_name(notename(self, False))

    @property
    def semitones(self):
        return self.nid

    def __eq__(self, other):
        if not isinstance(other, _Note):
            return False

        return self.nid == other.nid and self.octave == other.octave

    def __str__(self):
        return notename(self, bemole=self.bemole)

    def __repr__(self):
        return self.__str__()

    def __add__(self, interval):
        if not isinstance(interval, int):
            raise ValueError("int expected")
        noteid = self.nid + interval
        if noteid < OCTAVE:
            return note(self.octave, self.noteid)
        else:
            octave, noteid = _move_octave(self.octave, noteid)
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

CID = 0
CsID = min2(CID)
DbID = CsID
DID = maj2(CID)
DsID = min3(CID)
EbID = DsID
EID = maj3(CID)
FID = perf4(CID)
FsID = dim5(CID)
GbID = FsID
GID = perf5(CID)
GsID = min6(CID)
AbID = GsID
AID = maj6(CID)
AsID = min7(CID)
BbID = AsID
BID = maj7(CID)
_BEMOLES = [DbID, EbID, GbID, AbID, BbID]


# semitones in OCTAVE
OCTAVE = 12

OCTAVE_COUNT = 10

_NAMES = {}

_NAMES[CID] = "C"
_NAMES[CsID] = ("Cs", "Db")
_NAMES[DID] = "D"
_NAMES[DsID] = ("Ds", "Eb")
_NAMES[EID] = "E"
_NAMES[FID] = "F"
_NAMES[FsID] = ("Fs", "Gb")
_NAMES[GID] = "G"
_NAMES[GsID] = ("Gs", "Ab")
_NAMES[AID] = "A"
_NAMES[AsID] = ("As", "Bb")
_NAMES[BID] = "B"

_CHARS = {}

for k, v in _NAMES.items():
    if isinstance(v, tuple):
        _CHARS[v[0]] = k
        _CHARS[v[1]] = k
    else:
        _CHARS[v] = k


def notename(n, bemole=False):
    def getname():
        name = _NAMES[n.nid]
        if not isinstance(name, tuple):
            return name
        else:
            if bemole:
                return name[1]
            return name[0]
    name = getname()
    return "%s%d" % (name, n.octave)


def octave_to_semitones(octave):
    return (OCTAVE * octave)


def _move_octave(octave, interval):
    semis = octave_to_semitones(octave) + interval
    new_octave = math.floor(semis / OCTAVE)
    octave_semis = octave_to_semitones(new_octave)
    nid = semis - octave_semis
    return (new_octave, nid)

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
        for interval in range(0, OCTAVE, 1):
            # sharp notename
            n = _Note(octave_number, interval)
            # print(i, o, n)
            _NOTES[octave_number].append(n)
            _register_note(n)

            # bemole notename
            if interval in _BEMOLES:
                nb = _Note(octave_number, interval, True)
                _register_note(nb)
_create_notes()

# print(globals())

# getters / or kindof constructors


def note_by_name(name):
    return _NOTES_BY_NAME[name]


def note(octave, semitones):
    return _NOTES[octave][semitones]


def note_by_semitones(semitones):
    octave, nid = _move_octave(0, semitones)
    return note(octave, nid)


for o in _NOTES:
    print(o)


if __name__ == "__main__":
    n = note(CID, 3)
    print(n)
    n2 = n + 10
    print(n2)
    n3 = n + 13
    print(n3)
    n4 = n + OCTAVE * 10
    print(n4)
