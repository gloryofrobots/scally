from scally import scales, notes

class String:
    def __init__(self, notes):
        super().__init__()
        self.open_note = notes[0]
        self.notes = notes

    @property
    def fretted_notes(self):
        return self.notes[1:]

    def __getitem__(self, i):
        return self.notes[i]

    def __str__(self):
        return str(self.notes)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self.notes.__iter__()
    

class Fret:
    def __init__(self, length, roots):
        super().__init__()
        self.strings = []
        self.width = length + 1
        for root in roots:
            notes = scales.chromatic.forrange(root, self.width)
            self.strings.append(String(notes))
        self.height = len(self.strings)

    @property
    def count_bars(self):
        return self.width - 1

    def get_string(self, y):
        return self.strings[y]

    def get_note(self, x, y):
        return self.strings[y][x]


class Builder:
    def __init__(self):
        self.init()

    def init(self):
        self.line = None
        self.lines = []
        self.nl()

    def nl(self):
        self.line = []
        self.lines.append(self.line)

    def add(self, *args):
        for arg in args:
            self.line.append(str(arg))

    def _build_pad_line(self, prev, padding):
        data = "".join(prev)
        length = len(data)
        count = len(data) // len(padding)
        line = padding * count
        return line
        
    def insert_pad_line(self, index, padding):
        prev = self.lines[0]
        data = self._build_pad_line(prev, padding)
        line = [data]
        self.lines.insert(index, line)

    def append_pad_line(self, padding):
        prev = self.lines[len(self.lines) - 2]
        data = self._build_pad_line(prev, padding)
        self.add(data)
        self.nl()
        
    def build(self):
        return "\n".join(["".join(line) for line in self.lines])

class FretView:
    def __init__(self, fret):
        self.fret = fret
        self.filters = []
        self.enabled = None
        self.enabled = []
        for y,_ in enumerate(self.fret.strings):
            self.enabled.append([True] * self.fret.width)

    def reset_filters(self):
        if len(self.filters) == 0:
            for y in range(self.fret.height):
                for x in range(self.fret.width):
                    self.enabled[y][x] = True
        else:
            for y in range(self.fret.height):
                for x in range(self.fret.width):
                    n = self.fret.get_note(x, y)
                    val = False
                    for f in self.filters:
                        if n in f:
                            val = True
                            break
                    self.enabled[y][x] = val

    def add_filter(self, f):
        if f not in self.filters:
            self.filters.append(f)

        self.reset_filters()

    def has_filter(self, f):
        return scale in self.scales

    def remove_filter(self, f):
        self.scales.remove(f)

    def strings_in_display_order(self):
        return list(reversed(self.fret.strings))

    def is_note_enabled(self, x, y):
        return self.enabled[y][x]

    def note_str(self, x, y):
        note = self.fret.get_note(x, y)
        if not self.is_note_enabled(x, y):
            return "   "
        if note.has_bemole():
            return str(note)
        else:
            return str(note) + " "
            
    def _build_string(self, b, y):
        b.add(":: ", self.note_str(0, y), " :: ")

        last = self.fret.width - 1
        for x in range(1, self.fret.width):
            note_str = self.note_str(x, y)
            if x < last:
                padding = " | "
            else:
                padding = " ::"
                
            b.add(note_str, padding)

    def _build_numeration(self, b):
        b.add("   ", " 0 ", "    ")
        for i in range(1, self.fret.width):
            s = str(i)
            if len(s) == 1:
                s = " %s " % s
            elif len(s) == 2:
                s = " %s" % s
                
            b.add(s, "   ")
        b.nl()

    def to_ascii(self):
        b = Builder()
        strings = self.strings_in_display_order()
            
        # b.nl()
        self._build_numeration(b)
        last = self.fret.height - 1
        for y in range(self.fret.height - 1, -1, -1):
            self._build_string(b, y)
            b.nl()
            if y == 0:
                b.append_pad_line("=")
            else:
                b.append_pad_line("-")
                
        b.insert_pad_line(1, "=")
        # b.nl()

        self._build_numeration(b)
        return b.build()

def fret(length, roots):
    if length < 0:
        raise ValueError("Negative fret length")
    if len(roots) == 0:
        raise ValueError("Empty fret")
    if isinstance(roots[0], str):
        roots = [notes.note(r) for r in roots]
    return Fret(length, roots)