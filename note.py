import math

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

def tones(n):
    return n / 2.0

def semitones(n):
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

OCTAVE = 12

__NAMES__ = {}

__NAMES__[C] = "C"
__NAMES__[Cs] = ("C#", "Db")
__NAMES__[D] = "D"
__NAMES__[Ds] = ("D#", "Eb")
__NAMES__[E] = "E"
__NAMES__[F] = "F"
__NAMES__[Fs] = ("F#", "Gb")
__NAMES__[G] = "G"
__NAMES__[Gs] = ("G#", "Ab")
__NAMES__[A] = "A"
__NAMES__[As] = ("A#", "Bb")
__NAMES__[B] = "B"

def notename(n, bemole=False):
    name = __NAMES__[n.nid]
    if not isinstance(name, tuple):
        return name
    else:
        if bemole:
            return name[1]
        return name[0]

def move_octave(octave, interval):
    semis = (OCTAVE * octave) + interval
    new_octave = math.floor(semis/OCTAVE)
    octave_semis = OCTAVE * new_octave
    nid = semis - octave_semis
    return (new_octave, nid)



class Note:
    def __init__(self, noteid, octave):
        super().__init__()
        self.nid = noteid
        self.octave = octave
    

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False

        return self.nid == other.nid
    
    def to_str(self, bemole=False):
        return "%s%d" % (notename(self, bemole), self.octave)
        
    def fullsemitones(self):
        return OCTAVE * self.octave + self.nid

    def __str__(self):
        return self.to_str()

    def __add__(self, interval):
        if not isinstance(interval , int):
            raise ValueError("int expected")
        noteid = self.nid + interval
        if noteid < OCTAVE:
            return Note(noteid, self.octave)
        else:
            octave, noteid = move_octave(self.octave, noteid)
            return Note(noteid, octave)


if __name__ == "__main__":
    n = Note(C, 3)
    print(n)
    n2 = n + 10
    print(n2)
    n3 = n + 13
    print(n3)
    n4 = n + OCTAVE * 10
    print(n4)
        
        
            