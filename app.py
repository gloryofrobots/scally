
from scally.allnotes import *
from scally import notes
from scally import scales
from scally import frets
from scally import library

def main():
    lib = library.load()
    maj = lib.find_scale("maj")
    print(maj)

if __name__ == "__main__":
    main()