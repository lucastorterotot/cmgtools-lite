import unittest
from efficiency import efficiency

class TestEfficiency(unittest.TestCase): 
    
    def test_1(self):
        self.assertEqual(efficiency('190503%HiggsSUSYGG1400%tt_mssm_signals_CMS_scale_j_RelativeSample_13TeV_up'),
                         0.)
        self.assertAlmostEqual(efficiency('190503%DYJetsToLL_M50%tt_DY_CMS_scale_j_RelativeBal_13TeV_up'),
                               0.106383)
        self.assertEqual(efficiency('190503%WWToLNuQQ%tt_generic_bg_Btagging_up'),
                         0.)

if __name__ == '__main__':
    unittest.main()
