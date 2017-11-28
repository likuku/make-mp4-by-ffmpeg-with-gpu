import unittest
from make_mp4_and_cutout_by_ffmpeg_with_gpu import *

class Test_make_array_vf(unittest.TestCase):
    def test_make_array_vf(self):
        self.assertEqual(['-vf', 'yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)'],
                         make_array_vf(True,True))
        self.assertEqual(None,
                         make_array_vf(False,False))
        self.assertEqual(['-vf', 'yadif=1'],
                         make_array_vf(True,False))
        self.assertEqual(['-vf', 'crop=iw:(ih/2):0:0,scale=iw:(ih*2)'],
                         make_array_vf(False,True))
    def test_make_cmd_array_for_copy(self):
        self.assertEqual(None,make_cmd_array_for_copy('00:00:00','00:01:00'))

if __name__ == '__main__':
    unittest.main()
