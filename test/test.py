import unittest
import random

from scally.allnotes import *
from scally import notes
from scally import scales
from scally import frets
from scally import library

class TestPack(unittest.TestCase):
    def setUp(self):
        pass

    def test_notes(self):
        self.assertFalse(Cs4 < C4)
        self.assertTrue(E5 > C4)

        self.assertTrue(C4 < B5)
        self.assertTrue(B5 > C4)
        self.assertFalse(B5 == C4)
        self.assertTrue(C5 == C5)

        self.assertFalse(C4 < C4)
        self.assertFalse(C4 > Cs4)
        self.assertTrue(C4 < Cs4)
        self.assertEqual(Cs4.to_bemole(), Db4)
        self.assertEqual(Db4.to_sharp(), Cs4)

        self.assertEqual(notes.notes_from_octave(1), [C1, Cs1, D1, Ds1, E1, F1, Fs1, G1, Gs1, A1, As1, B1])
        self.assertEqual(notes.notes_from_octave(9), [C9, Cs9, D9, Ds9, E9, F9, Fs9, G9, Gs9, A9, As9, B9])
        self.assertEqual(notes.note_by_semitones(11), B0)
        self.assertEqual(notes.note_by_semitones(22), As1)
        self.assertEqual(notes.note("C", 4), C4)
        self.assertEqual(notes.note("C4"), C4)

        self.assertEqual(C4.min2(), Cs4)
        self.assertEqual(C4.maj2(), D4)
        self.assertEqual(C4.min3(), Ds4)
        self.assertEqual(C4.maj3(), E4)
        self.assertEqual(C4.perf4(), F4)
        self.assertEqual(C4.dim5(), Fs4)
        self.assertEqual(C4.perf5(), G4)
        self.assertEqual(C4.min6(), Gs4)
        self.assertEqual(C4.maj6(), A4)
        self.assertEqual(C4.min7(), As4)
        self.assertEqual(C4.maj7(), B4)

        self.assertEqual(12 + C4, C5)
        self.assertEqual(C4 + 12, C5)
        self.assertEqual(C4 + 13, Cs5)
        self.assertEqual(C4 + 24, C6)
        self.assertEqual(C4 - 12, C3)
        self.assertEqual(C4 - 1, B3)
        self.assertEqual(C4 - 13, B2)
        self.assertEqual(C4 - D4, -2)
        self.assertEqual(D4 - C4, 2)
        self.assertEqual(D4 - C5, -10)
        self.assertEqual(C5 - C4, 12)
        self.assertEqual(C5 - D0, 58)
        self.assertEqual(A4.transpose(0, -1), A3)
        self.assertEqual(A4.transpose(1, 1), As5)

    def assertScales(self, sc1, sc2):
        self.assertEqual(sc1, sc2)
        self.assertEqual(sc1.build_octave(C4), sc2.build_octave(C4))
        self.assertNotEqual(sc1.build_octave(C5), sc2.build_octave(C4))
        
    def test_scales(self):
        print("---test scales ---")
        maj0 = scales.scale_intervals([0, 2, 2, 1, 2, 2, 2, 1])
        maj1 = scales.scale_intervals([2, 2, 1, 2, 2, 2])
        maj2 = scales.scale_intervals("2-2-1-2-2-2")
        maj3 = scales.scale_semitones([2, 4, 5, 7, 9, 11])
        maj4 = scales.scale_semitones("0-2-4-5-7-9-11-12")
        maj7 = scales.scale("1-2-3-4-5-6-7")
        maj8 = scales.scale(["1","2","3", "4", "5", "6", "7"])

        # maj9 = scales.scale("1-2-b3-4-5-b6-7")
        # min1 = scales.scale("1-b2-b3-b4-b5-b6-6")

        self.assertScales(scales.scale("1-2-b3-4-5-b6-7"), scales.scale("1-2-#2-4-5-b6-7"))

        self.assertEqual(maj0.to_semitone_string(), "0-2-4-5-7-9-11-12")
        self.assertEqual(maj0.to_degree_string(), "1-2-3-4-5-6-7")

        self.assertScales(scales.scale_intervals("2-2-1-2-2-2-1"), scales.scale_intervals("2-2-1-2-2-2"))
        self.assertScales(scales.scale_intervals("0-2-2-1-2-2-2-1"), scales.scale_intervals("0-2-2-1-2-2-2"))

        self.assertScales(maj0, maj1)
        self.assertScales(maj1, maj2)
        self.assertScales(maj3, maj4)

        self.assertScales(maj4, maj1)
        self.assertScales(maj7, maj8)
        self.assertScales(maj1, maj8)

    def test_lib(self):
        lib = library.load()
        scl = lib.find_scale("maj")
        ch = lib.find_chord('maj7')
        self.assertEqual(ch.build_octave(C4, 2), [C4, E4, G4, B4, C5, E5, G5, B5])
        self.assertEqual(scl.build_octave(C4, 2), [C4, D4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5, A5, B5])

        scl = lib.find_scale("bb7")
        self.assertEqual(
            scl.build_octave(C4, 3),
            [C4, Cs4, Ds4, E4, Fs4, Gs4, A4, C5, Cs5, Ds5, E5, Fs5, Gs5, A5, C6, Cs6, Ds6, E6, Fs6, Gs6, A6])

        ch = lib.find_chord('13sus4(b9)')
        self.assertEqual(
            ch.build_octave(C4, 5),
            [C4, F4, G4, As4, Cs5, A5, C5, F5, G5, As5, Cs6, A6, C6, F6,
             G6, As6, Cs7, A7, C7, F7, G7, As7, Cs8, A8, C8, F8, G8, As8, Cs9, A9])

        
        self._test_algos(lib)

    def _test_algos(self, lib):
        scl = lib.find_scale('lydian')
        ch = lib.build_chord(C, 'maj13#11')
        scales = lib.build_chord_root_scales(ch)
        self.assertScales(scl, scales[0].template)

        scl = lib.build_scale(A, "whole tone")
        chords = lib.build_scale_chords(scl)

        
        ch = lib.build_chord(C, 'dim7')
        scales = lib.build_chord_scales(ch)

        scl = lib.find_scale_intervals([2, 2, 1, 2, 2, 2])
        scl2 = lib.find_scale_degrees("1-2-3-4-5-6-7")
        self.assertScales(scl[0], scl2[0])

        # list(map(print, scales))

        # print(ch)
    # def test_pc(self):
    #     maj = scales.scale("2-2-1-2-2-2")
    #     print(maj.forkey(C).pcs)

    # def test_fret(self):
    #     fret = frets.fret(24, [E2, As2, D3, G3, B3, E4])
    #     view = frets.FretView(fret)
    #     maj = scales.scale_intervals("2-2-1-2-2-2")
    #     print(maj.forkey(C).pcs)
    #     # view.add_filter(maj.forkey(notes.C))
    #     print(view.to_ascii())
    #     # for string in fret.strings:
    #     #     print(string)

if __name__ == "__main__":
    unittest.main()