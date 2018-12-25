from scally import notes
import scally.allnotes as ns


DEGREE = {
    "1": 0, "#1": 1,
    "b2": 1, "2": 2, "#2": 3,
    "b3": 3,  "3": 4, "#3": 5,
    "b4": 4, "4": 5, "#4": 6,
    "b5": 6, "5": 7, "#5": 8,
    "b6": 8, "6": 9, "#6": 10,
    "b7": 10, "7": 11,

    "8": 12, "#8": 13,
    "b9": 13, "9": 14, "#9": 15,
    "b10": 15,  "10": 16, "#10": 17,
    "b11": 16, "11": 17, "#11": 18,
    "b12": 18, "12": 19, "#12": 20,
    "b13": 20, "13": 21, "#13": 22,
    "b14": 22, "14": 23,
}


SEMITONES_TO_DEGREE = {
    0: "1", 1: "b2", 2: "2",
    3: "b3", 4: "3", 5: "4",
    6: "b5", 7: "5", 8: "b6",
    9: "6", 10: "b7", 11: "7",

    12: "8", 13: "b9", 14: "9",
    15: "b10", 16: "10", 17: "11",
    18: "b12", 19: "12", 20: "b13",
    21: "13", 22: "b14", 23: "14"
}


class Template:

    def __init__(self, intervals):
        super().__init__()
        self.intervals = intervals
        self.semitones = self._build_semitones()
        self.pcs = self._build_pitch_classes()
        self.degrees = self._build_degrees()

    def get_interval(self, step):
        step = step % len(self.intervals)
        return self.intervals[step]
        
    def _build_degrees(self):
        degree = []
        for s in self.semitones[0:len(self.semitones) - 1]:
            d = SEMITONES_TO_DEGREE[s]
            degree.append(d)

        return degree

    def _build_semitones(self):
        val = 0
        semis = [0]
        for i in self.intervals:
            val += i
            semis.append(val)
        return semis

    def _build_pitch_classes(self):
        return [notes.C] + [notes.get_pc(s) for s in self.semitones[0:len(self.semitones) - 1]]

    def to_degree_string(self):
        return "-".join(map(str, self.degrees))
    
    def to_semitone_string(self):
        return "-".join(map(str, self.semitones))

    def fornote(self, tonic, octaves=1):
        pc = tonic.pc
        octave = tonic.octave
        return self.forkey(pc).build_octave(octave, octaves)

    def forrange(self, tonic, steps):
        pc = tonic.pc
        octave = tonic.octave
        return self.forkey(pc).build_range(octave, steps)
        
    def forkey(self, pc):
        if not isinstance(pc, notes.PitchClass):
            raise TypeError("PitchClass expected")

        current = pc
        result = [current]
        for interval in self.intervals:
            # distance = i * notes.OCTAVE_SEMITONES + interval
            current = current + interval
            if current not in result:
                result.append(current)

        # result.pop()
        return self.build(result)

    def __str__(self):
        return "<scale %s>" % "-".join(map(str, self.degrees))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Template):
            return False

        return self.intervals == other.intervals

class ScaleTemplate(Template):
    def __init__(self, intervals):
        super().__init__(intervals)
        self.binary = self._build_binary()

    def _build_binary(self):
        binary = []
        for pc in notes.PITCH_CLASSES:
            if pc in self.pcs:
                binary.append(1)
            else:
                binary.append(0)

        return binary

    def build(self, notes):
        return Scale(self, notes)

    def to_binary_string(self):
        return "".join(map(str, self.binary))

    def __str__(self):
        return "<scale %s>" % "-".join(map(str, self.degrees))


class ChordTemplate(Template):
    def __init__(self, intervals):
        super().__init__(intervals)

    def __str__(self):
        return "<chord %s>" % "-".join(map(str, self.degrees))

    def build(self, pcs):
        return Chord(self, pcs)

class Scale:
    def __init__(self, template, pcs):
        super().__init__()
        self.template = template
        self.pcs = pcs
        self.root = self.pcs[0]

        
    def build_range(self, octave, steps):
        current = self.root.foroctave(octave)
        result = [current]
        i = 0
        for _ in range(steps):
            interval = self.template.get_interval(i)
            current = current + interval
            result.append(current)
            i += 1
            i = i % notes.OCTAVE_SEMITONES + 1

        return result

    def build_octave(self, octave, octaves=1):
        current = self.root.foroctave(octave)
        result = [current]
        for i in range(octaves):
            for interval in self.template.intervals:
                # distance = i * notes.OCTAVE_SEMITONES + interval
                note = current + interval
                result.append(note)
                current = note
        # last note will be start of new octave
        result.pop()
        return result

    def is_part_of(self, scale):
        for pc in self.pcs:
            if not scale.has_pc(pc):
                return False
        return True

    def has_note(self, note):
        for pc in self.pcs:
            if pc.has_note(note):
                return True
        return False
                
    def has_pc(self, _pc):
        for pc in self.pcs:
            if pc == _pc:
                return True
        return False

    def __contains__(self, note):
        if isinstance(note, notes.Note):
            return self.has_note(note)
        elif isinstance(note, notes.PitchClass):
            return self.has_pc(note)

    def __str__(self):
        return "<scale %s>" % "-".join(map(str, self.template.degrees))

    def __repr__(self):
        return str(self)

class Chord(Scale):
    pass

class ScaleBuildError(RuntimeError):
    pass


def parse_int_list(semitones):
    return [int(val.strip()) for val in semitones.split("-")]


def from_intervals(intervals):
    if isinstance(intervals, str):
        intervals = parse_int_list(intervals)
    intervals = intervals[:]
    s = sum(intervals)
    last = notes.OCTAVE_SEMITONES - s
    if last != 0:
        intervals.append(last)

    if intervals[0] == 0:
        intervals.pop(0)

    # if intervals[0] != 0:
    #     intervals.insert(0, 0)

    # if sum(intervals) > notes.OCTAVE_SEMITONES:
    #     raise ScaleBuildError(
    #         "Sum of scale intervals exceeds %d semitones. " +
    #         "Transition to octave tonic will be inserted automatically"
    #         % notes.OCTAVE_SEMITONES
    #     )
    return ScaleTemplate(intervals)


def from_semitones(semitones):
    if isinstance(semitones, str):
        semitones = parse_int_list(semitones)
    # assure octave interval
    if max(semitones) < 12:
    # if semitones[len(semitones) - 1] != 12:
        semitones = semitones + [12]


    if len(set(semitones)) != len(semitones):
        raise ScaleBuildError("Duplicate scale semitones")

    prev = semitones[0]
    intervals = [prev]

    for s in semitones[1:]:
        interval = s - prev
        intervals.append(interval)
        prev = s
    return from_intervals(intervals)


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

    if len(set(binary)) > 2:
        raise ScaleBuildError("Invalid input. only ones and zeros are allowed")

    intervals = []
    prev = notes.get_pc(0)
    for i, ch in enumerate(binary):
        if ch == 1:
            note = notes.get_pc(i)
            interval = note - prev
            intervals.append(interval)
            prev = note

    return from_intervals(intervals)


def from_degrees(degrees):
    # print("DE", degrees)
    if isinstance(degrees, str):
        degrees = [val.strip() for val in degrees.split("-")]

    intervals = []
    for d in degrees:
        if d not in DEGREE:
            raise ValueError(
                "Invalid scale degree %s. accepted values x-bx-#x" % d
            )

        interval = DEGREE[d]
        intervals.append(interval)
    return from_semitones(intervals)


chromatic = from_binary("1" * 12)
