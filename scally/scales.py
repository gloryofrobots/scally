from scally import notes


class Scale:
    def __init__(self, intervals):
        super().__init__()
        self.intervals = intervals

    def build(self, tonic, octaves=1, pop_last_note=True):
        result = [tonic]
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

    def __eq__(self, other):
        if not isinstance(other, Scale):
            return False

        return self.intervals == other.intervals


def scale(intervals):
    return Scale(intervals)

class ScaleBuildError(RuntimeError):
    pass

def from_semitones(semitones):
    # assure octave interval
    if semitones[len(semitones) - 1] != 12:
        semitones = semitones[:]
        semitones.append(12)

    if len(set(semitones)) != len(semitones):
        raise ScaleBuildError("duplicate scale semitones")
        

    prev = semitones[0]
    intervals = [prev]

    for s in semitones[1:]:
        interval = s - prev
        intervals.append(interval)
        prev = s

    return scale(intervals)

def from_binary_list(lst):
    intervals = 0


# 