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
    def test_rebuild_list_str_src_media_path(self):
        pass
        self.assertEqual(['/path/subPath','file.ext'],
             rebuild_list_str_src_media_path('/path/subPath/file.ext',path_split_by))
        self.assertEqual(['/path/subPath','file.ext'],
             rebuild_list_str_src_media_path('"/path/subPath/file.ext"',path_split_by))
        self.assertEqual(['/path/subPath','file.ext'],
             rebuild_list_str_src_media_path('/path/subPath/file.ext ',path_split_by))
        self.assertEqual(['/path/sub\ Path','file.ext'],
             rebuild_list_str_src_media_path('/path/sub\ Path/file.ext ',path_split_by))
    def test_rebuild_bool_deinterlace(self):
        pass
        self.assertTrue(rebuild_bool_deinterlace('1'))
        self.assertFalse(rebuild_bool_deinterlace('0'))
        self.assertFalse(rebuild_bool_deinterlace(''))
        #with self.assertRaises(TypeError):
        #    value = rebuild_bool_deinterlace('balbala')
        #self.assertEqual(False,rebuild_bool_deinterlace('balabla'))
    def test_check_and_rebuild_str_codec_video(self):
        pass
        self.assertEqual('h264_nvenc',
                         check_and_rebuild_str_codec_video('0'))
        self.assertEqual('libx264',
                         check_and_rebuild_str_codec_video('1'))
        self.assertEqual('hevc_nvenc',
                         check_and_rebuild_str_codec_video('2'))
        self.assertEqual('libx265',
                         check_and_rebuild_str_codec_video('3'))
        self.assertEqual('h264_videotoolbox',
                         check_and_rebuild_str_codec_video('4'))
        self.assertEqual('copy',
                         check_and_rebuild_str_codec_video('5'))
    def test_check_and_rebuild_str_bitrate_video(self):
        pass
        self.assertEqual('100M',
                         check_and_rebuild_str_bitrate_video(''))
        self.assertEqual('10M',
                         check_and_rebuild_str_bitrate_video('10'))
    def test_set_bitrate_for_3Dtop2Dleft_from_list_for_cmd_array(self):
        pass
        self.assertEqual([['crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '-b:v','40M']],
             set_bitrate_for_3Dtop2Dleft_from_list_for_cmd_array(
                 [['crop=iw:(ih/2):0:0,scale=iw:(ih*2)','-b:v','100M']],'40M'))
        self.assertEqual([['yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                          '-b:v','40M']],
             set_bitrate_for_3Dtop2Dleft_from_list_for_cmd_array(
                 [['yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)','-b:v','100M']],
                 '40M'))
    def test_rebuild_str_timestamp_input(self):
        self.assertEqual('01:01:01',
                         rebuild_str_timestamp_input('01:01:01'))
        self.assertEqual('01:01:01',
                         rebuild_str_timestamp_input('1:1:1'))
        self.assertEqual('100:01:01',
                         rebuild_str_timestamp_input('100:1:1'))
        self.assertEqual('01:01:00',
                         rebuild_str_timestamp_input('01:01:0'))
    def test_make_str_duration(self):
        self.assertEqual('999999999',make_str_duration('00:00:00',None))
        self.assertEqual('60',make_str_duration('00:00:00','00:01:00'))
        self.assertEqual('60',make_str_duration('01:01:53','01:02:53'))
    def test_make_str_dst_video_file(self):
        pass
        self.assertEqual('/path%sfile.ext_00_00_00_to_00_00_60' % path_split_by,
                         make_str_dst_video_file('00:00:00',
                                                 '00:00:60',
                                                 '/path',
                                                 'file.ext'))
    def test_make_array_vf(self):
        self.assertEqual(['-vf', 'yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)'],
                         make_array_vf(True,True))
        self.assertEqual(None,
                         make_array_vf(False,False))
        self.assertEqual(['-vf', 'yadif=1'],
                         make_array_vf(True,False))
        self.assertEqual(['-vf', 'crop=iw:(ih/2):0:0,scale=iw:(ih*2)'],
                         make_array_vf(False,True))
    def make_cmd_array_for_copy(self):
        pass
        #self.assertEqual(None,make_cmd_array_for_copy('00:00:00','00:01:00'))
    def make_cmd_array_for_other(self):
        pass
    def make_list_for_cmd_array(self):
        pass


if __name__ == '__main__':
    unittest.main()
