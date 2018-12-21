import unittest
import random

from scally.notes import *
from scally import notes
from scally import scales

class TestPack(unittest.TestCase):
    def setUp(self):
        pass

    def enum_choice(self, e):
        return random.choice(list(e))

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
        self.assertEqual(sc1.build(C4), sc2.build(C4))
        self.assertNotEqual(sc1.build(C5), sc2.build(C4))
        
    def test_scales(self):
        print("---test scales ---")
        maj0 = scales.scale([0, 2, 2, 1, 2, 2, 2, 1])
        maj1 = scales.scale([2, 2, 1, 2, 2, 2])
        maj2 = scales.scale("2-2-1-2-2-2")
        maj3 = scales.from_semitones([2, 4, 5, 7, 9, 11])
        maj4 = scales.from_semitones("2-4-5-7-9-11")
        maj5 = scales.from_binary("101011010101")
        maj6 = scales.from_binary([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
        maj7 = scales.from_degrees("1-2-3-4-5-6-7")
        maj8 = scales.from_degrees(["1","2","3", "4", "5", "6", "7"])
        print(maj0)
        print(maj1)
        print(maj2)
        print(maj3)
        print(maj4)
        print(maj5)
        print(maj6)
        print(maj7)

        self.assertScales(scales.scale("2-2-1-2-2-2-1"), scales.scale("2-2-1-2-2-2"))
        self.assertScales(scales.scale("0-2-2-1-2-2-2-1"), scales.scale("0-2-2-1-2-2-2"))
        self.assertScales(maj0, maj1)
        self.assertScales(maj1, maj2)
        self.assertScales(maj3, maj4)

        self.assertScales(maj4, maj1)
        self.assertScales(maj1, maj5)
        self.assertScales(maj5, maj6)
        self.assertScales(maj7, maj8)
        self.assertScales(maj1, maj8)
                    

if __name__ == "__main__":
    unittest.main()