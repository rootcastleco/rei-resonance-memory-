import math
import unittest
from model import Beam, Memory, channel, simulate, G

class TestBeam(unittest.TestCase):
    def setUp(self):
        self.b=Beam()

    def test_tuning(self):
        for f in (20,25,40,50):
            self.assertAlmostEqual(self.b.natural_frequency(self.b.tune(f)),f,places=9)

    def test_lengths(self):
        for f,L in ((20,77.75),(25,67.11),(40,49.18),(50,42.43)):
            self.assertAlmostEqual(self.b.tune(f)*1000,L,delta=0.03)

    def test_resonance(self):
        f=25
        L=self.b.tune(f)
        self.assertAlmostEqual(self.b.amplitude(L,f,.3,unit_participation=True),6*.3*G/(2*math.pi*f)**2,places=12)

    def test_zero(self):
        self.assertEqual(self.b.amplitude(self.b.tune(25),25,0),0)

    def test_frequency_selectivity(self):
        L=self.b.tune(25)
        self.assertGreater(self.b.amplitude(L,25,.3),self.b.amplitude(L,50,.3))

    def test_participation(self):
        self.assertGreater(self.b.participation(self.b.tune(25)),1)

    def test_negative_parameters(self):
        with self.assertRaises(ValueError):
            Beam(tip_mass=-1)

    def test_invalid_frequency(self):
        for f in (0,float("nan"),float("inf"),100000):
            with self.assertRaises(ValueError):
                self.b.tune(f)

    def test_invalid_acceleration(self):
        with self.assertRaises(ValueError):
            self.b.amplitude(self.b.tune(25),25,-1)

    def test_stress(self):
        self.assertEqual(self.b.stress(self.b.tune(25),0),0)

    def test_memory_leak(self):
        m=Memory(1,10)
        m.advance(0,True)
        m.advance(1)
        self.assertAlmostEqual(m.value,math.exp(-1))

    def test_memory_latch_reset(self):
        m=Memory(1,2)
        m.advance(0,True)
        self.assertTrue(m.advance(0,True))
        self.assertTrue(m.advance(100))
        m.reset()
        self.assertFalse(m.latched)
        self.assertEqual(m.value,0)

    def test_transient_sustained(self):
        r=simulate(self.b,25,25,.40,3)
        self.assertTrue(r["latched"])
        self.assertIsNotNone(r["trip_s"])

    def test_transient_short(self):
        r=simulate(self.b,25,25,.40,3,on_time=.1)
        self.assertFalse(r["latched"])

    def test_crossing_burst_rejected(self):
        r=simulate(self.b,25,25,.40,3,on_time=.4)
        self.assertGreater(r["events"],0)
        self.assertFalse(r["latched"])

    def test_invalid_memory_step(self):
        with self.assertRaises(ValueError):
            Memory(1,2).advance(-1)

    def test_transient_zero(self):
        self.assertEqual(simulate(self.b,25,25,0,1)["peak_mm"],0)

    def test_transient_convergence(self):
        a=simulate(self.b,25,25,.40,3,steps_per_cycle=120)
        b=simulate(self.b,25,25,.40,3,steps_per_cycle=240)
        self.assertAlmostEqual(a["peak_mm"],b["peak_mm"],delta=.002)
        self.assertAlmostEqual(a["trip_s"],b["trip_s"],delta=.005)

if __name__=="__main__":
    unittest.main()
