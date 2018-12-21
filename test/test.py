import unittest
import random

from scally.notes import *
from scally import notes


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

        self.assertEqual(C4 + 12, C5)
        self.assertEqual(C4 + 13, Cs5)
        self.assertEqual(C4 + 24, C6)




if __name__ == "__main__":
    unittest.main()