
from scally.allnotes import *
from scally import notes
from scally import scales
from scally import frets
from scally import library

def assure_view(func):
    def wrapper(self, *args):
        if self.view is None:
            self.msg("Please specify instrument")
            return
        return func(self, *args)
    return wrapper

class App:
    
    def __init__(self):
        super().__init__(self)
        self.view = None
        self.lib = library.load()

    @assure_view
    def show(self):
        if self.view is None:
            self.msg("Please specify instrument")
        else:
            self.msg(self.view.to_ascii())

    def load(self, fname):
        try:
            self.lib.load(fname)
        except e:
            self.msg("LOAD ERROR %s" % str(e))

    @assure_view
    def add_chord_filter(self, root, name):
        pc = notes.get_pc_by_name(root)
        ch = lib.build_chord(pc, name)
        self.view.add_filter(ch)

    @assure_view
    def remove_chord_filter(self, root, name):
        pc = notes.get_pc_by_name(root)
        ch = lib.build_chord(pc, name)
        self.view.remove_filter(ch)

    @assure_view
    def reset_filters(self):
        self.view.reset_filters()
    

def build_scale(lib, tonic, name):
    scl = lib.build_scale(tonic, name)
    print("________________________________________________")
    print(scl)
    chords = lib.build_scale_chords(scl)
    list(map(print, chords))
    

def main():
    lib = library.load()
    # FROZEN DESERT
    build_scale(lib, E, "bb7")
    build_scale(lib, A, "augmented")

if __name__ == "__main__":
    main()
