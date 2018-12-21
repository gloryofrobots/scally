from scally import notes


class Scale:

    def __init__(self, intervals):
        super().__init__()
        self.intervals = intervals

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

CHROMATIC = scale("1-1-1-1-1-1-1-1-1-1-1").build(notes.C4)

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

DEGREE = {
    "1": 0, "#1": 1,
    "b2": 1, "2": 2, "#2": 3,
    "b3": 3,  "3": 4, "#3":5,
    "b4": 4, "4": 5, "#4": 6,
    "b5": 6, "5": 7, "#5": 8,
    "b6": 8, "6": 9, "#6": 10,
    "b7": 10, "7": 11
}


def from_degrees(degrees):
    if isinstance(degrees, str):
        degrees = [val.strip() for val in degrees.split("-")]

    intervals = []
    for d in degrees:
        if d not in DEGREE:
            raise ValueError("Invalid scale degree. accepted values 1, b1, #1")
        interval = DEGREE[d]
        intervals.append(interval)
    return from_semitones(intervals)
