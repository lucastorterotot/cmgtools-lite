from backends import GFAL

@unittest.skip("GFAL does not work at the moment... if not needed remove unittest")
class TestGFAL(unittest.TestCase):
    
    def test_rfile(self):
        gfal = GFAL()
        self.assertEqual(gfal._file('/store'),
                         'srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data/store')
        self.assertEqual(gfal._file('test'),
                         'file:test')

    def test_ls(self):
        gfal = GFAL(False)
        self.assertEqual(gfal.ls('test'), 
                         'gfal-ls file:test')
        self.assertEqual(gfal.ls('/store/user/cbernet/heppyTrees'),
                         'gfal-ls srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data/store/user/cbernet/heppyTrees')

    def test_run(self):
        gfal = GFAL(True)
        with tempfile.NamedTemporaryFile() as tfile:
            self.assertEqual(gfal.ls(tfile.name),
                             [''.join(['file:',tfile.name])])

    def test_ls_real(self):
        gfal = GFAL(True)
        path = '/store/user/cbernet/heppyTrees/CMSSW_8_0_28_patch1/tauMu_2017_cfg/HiggsSUSYBB1000/180625_123805/0000'
        result = gfal.ls(path)
        tgzs = [fname for fname in result if fname.endswith('.tgz')]
        self.assertEqual(len(tgzs),9)

