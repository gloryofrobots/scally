from scally import scales, notes

class String:
    def __init__(self, notes):
        super().__init__()
        self.open_note = notes[0]
        self.notes = notes

    @property
    def fretted_notes(self):
        return self.notes[1:]

    def __str__(self):
        return str(self.notes)

    def __repr__(self):
        return self.__str__()
    

class Fret:
    def __init__(self, roots, length):
        super().__init__()
        self.strings = []
        for root in roots:
            notes = scales.chromatic.build_range(root, length+1)
            self.strings.append(String(notes))
        self.width = length
        self.height = len(self.strings)

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
        
    def prepend_pad_line(self, padding):
        prev = self.lines[0]
        data = self._build_pad_line(prev, padding)
        line = [data]
        self.lines.insert(0, line)

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
        self.scales = []

    def add(self, scale):
        if scale in self.scales:
            return False
        self.scales.append(scale)
        return True

    def has(self, scale):
        return scale in self.scales

    def remove(self, scale):
        self.scales.remove(scale)

    def strings_in_display_order(self):
        return list(reversed(self.fret.strings))

    def is_note_enabled(self, note):
        return note.has_bemole()
        return True

    def note_str(self, note):
        if not self.is_note_enabled(note):
            return "   "
        if note.has_bemole():
            return str(note)
        else:
            return str(note) + " "
            
    def _build_string(self, b, string):
        b.add(":: ", self.note_str(string.open_note), " :: ")
        notes = string.fretted_notes

        last = self.fret.width - 1
        for i in range(self.fret.width):
            note = notes[i]
            note_str = self.note_str(note)
            if i < last:
                padding = " | "
            else:
                padding = " ::"
                
            b.add(note_str, padding)

    def _build_numeration(self, b):
        b.add("   ", "   ", "    ")
        last = self.fret.width - 1
        for i in range(self.fret.width):
            s = str(i)
            if len(s) == 1:
                s = " %s " + s
            elif len(s) == 2:
                s = " %s" + s
                
            b.add(s, padding)
        b.nl()

    def to_ascii(self):
        b = Builder()
        strings = self.strings_in_display_order()
            
        last = self.fret.height - 1
        for i in range(self.fret.height):
            string = strings[i]
            self._build_string(b, string)
            b.nl()
            if i < last:
                b.append_pad_line("-")
            else:
                b.append_pad_line("=")
                
        b.prepend_pad_line("=")
        b.nl()

        self._build_numeration(b)
        return b.build()