from scally import scales, notes

class Fret:
    def __init__(self, roots, length):
        super().__init__()
        self.length = length
        self.strings = []
        for root in roots:
            string = scales.chromatic.build_range(root, length)
            self.strings.append(string)