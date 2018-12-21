from scally import notes

DEGREE = {
    "1": 0, "#1": 1,
    "b2": 1, "2": 2, "#2": 3,
    "b3": 3,  "3": 4, "#3": 5,
    "b4": 4, "4": 5, "#4": 6,
    "b5": 6, "5": 7, "#5": 8,
    "b6": 8, "6": 9, "#6": 10,
    "b7": 10, "7": 11
}

SEMITONES_TO_DEGREE = {

}

CHROMATIC = [notes.C4, notes.Cs4, notes.D4, notes.Ds4,
             notes.E4, notes.F4, notes.Fs4, notes.G4,
             notes.Gs4, notes.A4, notes.As4, notes.B4]



class Scale:

    def __init__(self, intervals):
        super().__init__()
        self.intervals = intervals
        self.c4 = self.build(notes.C4)
        
        self.binary = self._build_binary()
        self.semitones = self._build_semitones()
        self.degrees = self._build_degrees()

    def _build_degrees(self):

        pass

    def _build_semitones(self):
        val = 0
        semis = []
        for i in self.intervals:
            val += i
            semis.append(val)
        return semis

    def _build_binary(self):
        binary = []
        for n in CHROMATIC:
            if n in self.c4:
                binary.append(1)
            else:
                binary.append(0)

        return binary

    def to_semitone_string(self):
        return "-".join(map(str, self.semitones))

    def to_binary_string(self):
        return "".join(map(str, self.binary))

    def build(self, tonic, octaves=1, pop_last_note=True):
        result = []
        current = tonic
        for i in range(octaves):
            for interval in self.intervals:
                # distance = i * notes.OCTAVE_SEMITONES + interval
                note = current + interval
                result.append(note)
                current = note
        if pop_last_note:
            result.pop()
        return result

    def __str__(self):
        return "<scale %s>" % "-".join(map(str, self.intervals))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Scale):
            return False

        return self.intervals == other.intervals


class ScaleBuildError(RuntimeError):
    pass


def parse_int_list(semitones):
    return [int(val.strip()) for val in semitones.split("-")]


def scale(intervals):
    if isinstance(intervals, str):
        intervals = parse_int_list(intervals)
    intervals = intervals[:]
    s = sum(intervals)
    last = notes.OCTAVE_SEMITONES - s
    if last != 0:
        intervals.append(last)
    if intervals[0] != 0:
        intervals.insert(0, 0)

    if sum(intervals) > notes.OCTAVE_SEMITONES:
        raise ScaleBuildError(
            "Sum of scale intervals exceeds %d semitones. " +
            "Transition to octave tonic will be inserted automatically"
            % notes.OCTAVE_SEMITONES
        )
    return Scale(intervals)

def from_semitones(semitones):
    if isinstance(semitones, str):
        semitones = parse_int_list(semitones)
    # assure octave interval
    if semitones[len(semitones) - 1] != 12:
        semitones = semitones + [12]

    if len(set(semitones)) != len(semitones):
        raise ScaleBuildError("Duplicate scale semitones")

    prev = semitones[0]
    intervals = [prev]

    for s in semitones[1:]:
        interval = s - prev
        intervals.append(interval)
        prev = s

    return scale(intervals)


def parse_binary_list(binary):
    return list(map(int, list(iter(binary))))



def from_binary(binary):
    intervals = []
    if isinstance(binary, str):
        binary = parse_binary_list(binary)

    if len(binary) != 12:
        raise ScaleBuildError("Binary list must consists of 12 zeros or ones")

    if binary[0] != 1:
        raise ScaleBuildError("Expected 1 in the leftmost position")

    if len(set(binary)) != 2:
        raise ScaleBuildError("Invalid input. only ones and zeros are allowed")

    intervals = []
    prev = CHROMATIC[0]
    for i, ch in enumerate(binary):
        if ch == 1:
            note = CHROMATIC[i]
            interval = note - prev
            intervals.append(interval)
            prev = note

    return scale(intervals)

def from_degrees(degrees):
    if isinstance(degrees, str):
        degrees = [val.strip() for val in degrees.split("-")]

    intervals = []
    for d in degrees:
        if d not in DEGREE:
            raise ValueError("Invalid scale degree. accepted values x-bx-#x")
        interval = DEGREE[d]
        intervals.append(interval)
    return from_semitones(intervals)
