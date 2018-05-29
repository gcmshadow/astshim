from __future__ import absolute_import, division, print_function
import math
import unittest

from numpy.testing import assert_allclose

import astshim as ast
from astshim.test import MappingTestCase


class TestSkyFrame(MappingTestCase):

    def test_FrameBasics(self):
        frame = ast.SkyFrame()
        self.assertEqual(frame.className, "SkyFrame")
        self.assertEqual(frame.nIn, 2)
        self.assertEqual(frame.nAxes, 2)
        self.assertEqual(frame.maxAxes, 2)
        self.assertEqual(frame.minAxes, 2)

        # default values for Frame properties (methods below test
        # setters and getters of SkyFrame properties)
        self.assertEqual(frame.alignSystem, "ICRS")
        self.assertEqual(frame.dut1, 0.0)
        self.assertEqual(frame.epoch, 2000.0)
        self.assertEqual(frame.obsAlt, 0.0)
        self.assertEqual(frame.obsLat, "N0:00:00.00")
        self.assertEqual(frame.obsLon, "E0:00:00.00")
        self.assertTrue(frame.permute)
        self.assertFalse(frame.preserveAxes)
        self.assertEqual(frame.system, "ICRS")
        self.assertEqual(frame.title, "ICRS coordinates")

        self.assertGreater(abs(frame.getBottom(1)), 1e99)
        self.assertGreater(abs(frame.getTop(1)), 1e99)
        self.assertGreater(frame.getTop(1), frame.getBottom(1))
        self.assertFalse(frame.getDirection(1))
        self.assertEqual(frame.getInternalUnit(1), "rad")
        self.assertEqual(frame.getNormUnit(1), "rad")
        self.assertEqual(frame.getSymbol(1), "RA")
        self.assertEqual(frame.getUnit(1), "hh:mm:ss.s")

        self.assertAlmostEqual(frame.getBottom(2), -math.pi / 2)
        self.assertAlmostEqual(frame.getTop(2), math.pi / 2)
        self.assertTrue(frame.getDirection(2))
        self.assertEqual(frame.getInternalUnit(2), "rad")
        self.assertEqual(frame.getNormUnit(2), "rad")
        self.assertEqual(frame.getSymbol(2), "Dec")
        self.assertEqual(frame.getUnit(2), "ddd:mm:ss")

        self.checkCopy(frame)
        self.checkPersistence(frame)

    def test_SkyFrameLonLat(self):

        frame = ast.SkyFrame()

        self.assertEqual(frame.lonAxis, 1)
        self.assertEqual(frame.latAxis, 2)
        self.assertTrue(frame.getIsLonAxis(1))
        self.assertTrue(frame.getIsLatAxis(2))
        self.assertFalse(frame.getIsLonAxis(2))
        self.assertFalse(frame.getIsLatAxis(1))

        # permute axes
        frame.permAxes([2, 1])
        self.assertEqual(frame.lonAxis, 2)
        self.assertEqual(frame.latAxis, 1)
        self.assertTrue(frame.getIsLonAxis(2))
        self.assertTrue(frame.getIsLatAxis(1))
        self.assertFalse(frame.getIsLonAxis(1))
        self.assertFalse(frame.getIsLatAxis(2))

        # permute again to restore original state
        frame.permAxes([2, 1])
        self.assertEqual(frame.lonAxis, 1)
        self.assertEqual(frame.latAxis, 2)
        self.assertTrue(frame.getIsLonAxis(1))
        self.assertTrue(frame.getIsLatAxis(2))
        self.assertFalse(frame.getIsLonAxis(2))
        self.assertFalse(frame.getIsLatAxis(1))

    def test_SkyFrameAlignOffset(self):
        frame = ast.SkyFrame()

        self.assertFalse(frame.alignOffset)
        frame.alignOffset = True
        self.assertTrue(frame.alignOffset)

    def test_SkyFrameAsTime(self):
        frame = ast.SkyFrame()

        for axis, defAsTime in ((1, True), (2, False)):
            self.assertEqual(frame.getAsTime(axis), defAsTime)
            frame.setAsTime(axis, not defAsTime)
            self.assertEqual(frame.getAsTime(axis), not defAsTime)

    def test_SkyFrameEquinox(self):
        frame = ast.SkyFrame()

        self.assertAlmostEqual(frame.equinox, 2000)
        newEquinox = 2345.6
        frame.equinox = newEquinox
        self.assertAlmostEqual(frame.equinox, newEquinox)

    def test_SkyFrameNegLon(self):
        frame = ast.SkyFrame()

        self.assertFalse(frame.negLon)
        frame.negLon = True
        self.assertTrue(frame.negLon)

    def test_SkyFrameProjection(self):
        frame = ast.SkyFrame()

        self.assertEqual(frame.projection, "")
        newProjection = "Arbitrary description"
        frame.projection = newProjection
        self.assertEqual(frame.projection, newProjection)

    def test_SkyFrameSkyRef(self):
        frame = ast.SkyFrame()

        assert_allclose(frame.getSkyRef(), [0, 0], atol=1e-12)
        newSkyRef = [-4.5, 1.23]
        frame.setSkyRef(newSkyRef)
        assert_allclose(frame.getSkyRef(), newSkyRef, atol=1e-12)

    def test_SkyFrameSkyRefIs(self):
        frame = ast.SkyFrame()

        self.assertEqual(frame.skyRefIs, "Ignored")
        for newSkyRefIs in ("Origin", "Pole", "Ignored"):
            frame.skyRefIs = newSkyRefIs
            self.assertEqual(frame.skyRefIs, newSkyRefIs)

    def test_SkyFrameSkyRefP(self):
        frame = ast.SkyFrame()

        defSkyRefP = [0.0, math.pi/2]
        assert_allclose(frame.getSkyRefP(), defSkyRefP, atol=1e-12)
        newSkyRefP = [0.1234, 0.5643]
        frame.setSkyRefP(newSkyRefP)
        assert_allclose(frame.getSkyRefP(), newSkyRefP, atol=1e-12)

    def test_SkyFrameSkyTol(self):
        frame = ast.SkyFrame()

        # the default is arbitrary so do not to assume a specific value
        defSkyTol = frame.skyTol
        newSkyTol = defSkyTol*1.2345
        frame.skyTol = newSkyTol
        self.assertAlmostEqual(frame.skyTol, newSkyTol)

    def test_SkyFrameSkyOffsetMap(self):
        frame = ast.SkyFrame()

        mapping = frame.skyOffsetMap()
        self.assertEqual(mapping.className, "UnitMap")


if __name__ == "__main__":
    unittest.main()
