import unittest
import tempfile 

from backends import GFAL, XRD

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


class TestXRD(unittest.TestCase): 
    
    def setUp(self): 
        self.path = '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304/0000'

    def test_rfile(self):
        xrd = XRD()
        local, path = xrd._file(self.path)
        self.assertEqual(local, False)
        self.assertEqual(
            path,
            '/dpm/in2p3.fr/home/cms/data'+self.path)
        local, path = xrd._file('test')
        self.assertEqual(local, True)
        self.assertEqual(path, 'test')

    def test_ls(self):
        xrd = XRD(False)
        self.assertEqual(
            xrd.ls('test'), 
            'ls test'
            )
        self.assertEqual(
            xrd.ls('/store/user/cbernet/heppyTrees'),
            'xrdfs lyogrid06.in2p3.fr ls  /dpm/in2p3.fr/home/cms/data/store/user/cbernet/heppyTrees'
            )

    def test_run(self):
        xrd = XRD(True)
        with tempfile.NamedTemporaryFile() as tfile:
            self.assertEqual(
                xrd.ls(tfile.name)[0],
                tfile.name
            )

    def test_ls_real(self):
        xrd = XRD(True)
        path = self.path
        result = xrd.ls(path)
        tgzs = [fname for fname in result if fname.endswith('.tgz')]
        self.assertEqual(len(tgzs),7)

    def test_cp(self): 
        '''COLIN: copy certainly does not work towards the SE!'''
        xrd = XRD(False)
        path = '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304/0000/heppyOutput_10.tgz'
        self.assertEqual(
            xrd.cp(path, '.'),
            'xrdcp root://lyogrid06.in2p3.fr//dpm/in2p3.fr/home/cms/data/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304/0000/heppyOutput_10.tgz .'
            )

    def test_lfn(self):
        xrd = XRD()
        self.assertEqual( xrd.lfn('/blah/store/foo'), '/store/foo' )
        self.assertEqual( xrd.lfn('/store/foo'), '/store/foo' )
        with self.assertRaises(ValueError):
            xrd.lfn('/tmp/foobar')

if __name__ == '__main__':
    unittest.main()
