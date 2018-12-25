import yaml
import os.path
from scally import notes
from scally import frets
from scally import scales
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class ParseLibError(RuntimeError):
    pass

class Record:
    def __init__(self, keys, value):
        if isinstance(keys, str):
            self._names = [keys]
        else:
            self._names = keys

        self._value = value

    @property
    def names(self):
        return self._names

    @property
    def value(self):
        return self._value

    def similar(self, name):
        maxratio = -1
        for n in self._names:
            maxratio = max(similar(n, name), maxratio)
        return maxratio

    def similar_name(self, name):
        best_id, maxratio = -1,-1
        for i,n in enumerate(self._names):
            ratio = similar(n, name)
            if ratio > maxratio:
                best_id = i
                maxratio = ratio
        if best_id == -1:
            return None
        return self._names[best_id]
            
    def __iter__(self):
        return iter((self.names, self.value))


class Library:
    FILENAME = "default_lib.yml"
    # FILENAME = "libtest.yml"

    def __init__(self, default_filename=None):
        super().__init__()
        self.scales = []
        self.chords = []
        self.instruments = []
        if default_filename is None:
            self.default_filename = os.path.join(os.path.dirname(__file__), self.FILENAME)
        else:
            self.default_filename = default_filename

        self.load(self.default_filename)

    def load(self, filename):
        with open(filename) as f:
            txt = f.read()
        data = yaml.load(txt)
        if "instruments" in data:
            self.add_instruments(data["instruments"])
        if "scales" in data:
            self.add_scales(data["scales"])
        if "chords" in data:
            self.add_chords(data["chords"])

    def add_instruments(self, data):
        for obj in data:
            name = obj["name"]
            tune = obj["tune"]
            length = obj["length"]
            fret = frets.fret(length, tune)
            self.instruments.append(Record(name, fret))

    def normalize_seq(self, txt):
        if "-" in txt:
            return txt
        txt = "-".join([s.strip() for s in txt.split(" ")])
        return txt

    def parse_template(self, obj):
        if "intervals" in obj:
            tpl = scales.from_intervals(self.normalize_seq(obj["intervals"]))
        elif "binary" in obj:
            tpl = scales.from_binary(obj["binary"])
        elif "semitones" in obj:
            tpl = scales.from_semitones(self.normalize_seq(obj["semitones"]))
        elif "degrees" in obj:
            tpl = scales.from_degrees(self.normalize_seq(obj["degrees"]))
        else:
            raise ParseLibError("Expected to have some formula for %s" % str(obj))

        return tpl

    def add_chords(self, data):
        for obj in data:
            name = obj["name"]
            tpl = self.parse_template(obj)
            self.chords.append(Record(name, tpl))

    def add_scales(self, data):
        for obj in data:
            name = obj["name"]
            tpl = self.parse_template(obj)
            self.scales.append(Record(name, tpl))

    def _find(self, name, records):
        best_id, maxratio = -1,-1
        for i,record in enumerate(records):
            try:
                ratio = record.similar(name)
            except:
                print("Error", record.names)
                continue
            if ratio > maxratio:
                best_id = i
                maxratio = ratio
        if best_id == -1:
            return None
        return records[best_id]

    def find_chord(self, name):
        return self._find(name, self.chords)

    def find_scale(self, name):
        return self._find(name, self.scales)

    def find_instrument(self, name):
        return self._find(name, self.instruments)

    def find_chord_scales(self, chord):
        result = []
        for r in self.scales:
            name, tpl = r
            scale = tpl.forkey(chord.root)
            if chord.is_part_of(scale):
                result.append((name, scale))
        return result
        

def load():
    return Library()
