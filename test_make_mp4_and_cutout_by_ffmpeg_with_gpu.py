import unittest
from make_mp4_and_cutout_by_ffmpeg_with_gpu import *

class Test_make_mp4_and_cutout_by_ffmpeg_with_gpu(unittest.TestCase):
    def test_check_str_raw_src_media_path(self):
        pass
        self.assertEqual(False,
                         check_str_raw_src_media_path(''))
        self.assertEqual(False,
                         check_str_raw_src_media_path('.13123241'))
        self.assertEqual(True,
                         check_str_raw_src_media_path('.'))
    def test_rebuild_str_timestamp_input(self):
        self.assertEqual('01:01:01',
                         rebuild_str_timestamp_input('01:01:01'))
        self.assertEqual('01:01:01',
                         rebuild_str_timestamp_input('1:1:1'))
        self.assertEqual('100:01:01',
                         rebuild_str_timestamp_input('100:1:1'))
        self.assertEqual('01:01:00',
                         rebuild_str_timestamp_input('01:01:0'))
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
        pass
        #self.assertEqual(None,make_cmd_array_for_copy('00:00:00','00:01:00'))

if __name__ == '__main__':
    unittest.main()
