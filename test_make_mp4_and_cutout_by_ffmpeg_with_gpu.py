import unittest
from make_mp4_and_cutout_by_ffmpeg_with_gpu import *

class Test_make_mp4_and_cutout_by_ffmpeg_with_gpu(unittest.TestCase):
    def test_check_str_raw_src_media_path(self):
        self.assertEqual(False,
                         check_str_raw_src_media_path(''))
        self.assertEqual(False,
                         check_str_raw_src_media_path('.13123241'))
        self.assertEqual(True,
                         check_str_raw_src_media_path('.'))

    def test_rebuild_list_str_src_media_path(self):
        self.assertEqual(['/path/subPath','file.ext'],
             rebuild_list_str_src_media_path('/path/subPath/file.ext',path_split_by))
        self.assertEqual(['/path/subPath','file.ext'],
             rebuild_list_str_src_media_path('"/path/subPath/file.ext"',path_split_by))
        self.assertEqual(['/path/subPath','file.ext'],
             rebuild_list_str_src_media_path('/path/subPath/file.ext ',path_split_by))
        self.assertEqual(['/path/sub\ Path','file.ext'],
             rebuild_list_str_src_media_path('/path/sub\ Path/file.ext ',path_split_by))

    def test_rebuild_bool_deinterlace(self):
        self.assertTrue(rebuild_bool_deinterlace('1'))
        self.assertFalse(rebuild_bool_deinterlace('0'))
        self.assertFalse(rebuild_bool_deinterlace(''))
        #with self.assertRaises(TypeError):
        #    value = rebuild_bool_deinterlace('balbala')
        #self.assertEqual(False,rebuild_bool_deinterlace('balabla'))

    def test_check_and_rebuild_str_codec_video(self):
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
        self.assertEqual('80M',
                         check_and_rebuild_str_bitrate_video(''))
        self.assertEqual('10M',
                         check_and_rebuild_str_bitrate_video('10'))

    def test_set_bitrate_for_3Dtop2Dleft_from_list_for_cmd_array(self):
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
        self.assertEqual('/path%sfile.ext_00_00_00_to_00_00_60' % path_split_by,
                         make_str_dst_video_file('00:00:00',
                                                 '00:00:60',
                                                 '/path',
                                                 'file.ext'))

    def test_make_array_vf(self):
        #make_array_vf(src_codec_video_deinterlace_input,str_make_2d_l_from_top,)
        self.assertEqual(['-vf', 'yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)'],
                         make_array_vf(True,True))
        self.assertEqual(None,
                         make_array_vf(False,False))
        self.assertEqual(['-vf', 'yadif=1'],
                         make_array_vf(True,False))
        self.assertEqual(['-vf', 'crop=iw:(ih/2):0:0,scale=iw:(ih*2)'],
                         make_array_vf(False,True))

    def test_make_cmd_array_for_copy(self):
        self.assertEqual(['%s' % ffmpeg_name,
                          '-ss','00:00:00',
                          '-i','/path/file.ext',
                          '-c','copy',
                          '-t','60'],
                         make_cmd_array_for_copy('00:00:00',
                                                 '/path/file.ext',
                                                 'copy',
                                                 '60'))

    def test_make_cmd_array_for_other(self):
        self.assertEqual(['%s' % ffmpeg_name,
                          '-ss','00:00:00',
                          '-i','/path/file.ext',
                          '-c:v','libx264',
                          '-map','0:v',
                          '-ac','2',
                          '-map','0:a',
                          '-b:v','100M',
                          '-t','60',
                          '-pix_fmt','yuv420p'],
                         make_cmd_array_for_other('00:00:00',
                                                 '/path/file.ext',
                                                 'libx264',
                                                 '100M',
                                                 '60'))

    def test_make_list_for_cmd_array(self):
        _dict_input = {'_src_video_name_input':'/path/file.ext',
                       '_bool_video_deinterlace':False,
                       '_str_codec_video':'copy',
                       '_str_bitrate':'100M',
                       '_start_timestamp':'00:00:00',
                       '_duration':'60',
                       '_dst_video_file':'/path/file.ext_00_00_00_to_00_01_00',
                       '_bool_make_2d_l_from_top':False,
                       '_str_bitrate_3dt2dl':None,
                       '_bool_double_action_3dt2dl':False,
                       '_bool_rewrite_output':False}
        pass
        # copy,60sec
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c','copy',
                           '-t','60',
                           '/path/file.ext_00_00_00_to_00_01_00.ext']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,deinterlace,100M,60sec,no2d,solo,noOverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = True
        _dict_input['_bool_rewrite_output'] = False
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-vf','yadif=1',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,deinterlace,100M,60sec,no2d,solo,OverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = True
        _dict_input['_bool_rewrite_output'] = True
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '-vf','yadif=1',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,nodeinterlace,100M,60sec,no2d,solo,noOverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = False
        _dict_input['_bool_rewrite_output'] = False
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,nodeinterlace,100M,60sec,no2d,solo,OverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = False
        _dict_input['_bool_rewrite_output'] = True
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,nodeinterlace,100M,60sec,3tb2d,40M,solo,noOverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = False
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = False
        _dict_input['_bool_rewrite_output'] = False
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-aspect','16:9',
                           '-vf','crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,nodeinterlace,100M,60sec,3tb2d,40M,solo,OverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = False
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = False
        _dict_input['_bool_rewrite_output'] = True
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '-aspect','16:9',
                           '-vf','crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,deinterlace,100M,60sec,3tb2d,40M,solo,noOverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = True
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = False
        _dict_input['_bool_rewrite_output'] = False
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-aspect','16:9',
                           '-vf','yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,deinterlace,100M,60sec,3tb2d,40M,solo,OverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = True
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = False
        _dict_input['_bool_rewrite_output'] = True
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '-aspect','16:9',
                           '-vf','yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,nodeinterlace,100M,60sec,3tb2d,40M,DoubleAction,noOverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = False
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = True
        _dict_input['_bool_rewrite_output'] = False
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-aspect','16:9',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4'],
                          ['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-aspect','16:9',
                           '-vf','crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,nodeinterlace,100M,60sec,3tb2d,40M,DoubleAction,OverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = False
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = True
        _dict_input['_bool_rewrite_output'] = True
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '-aspect','16:9',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4'],
                          ['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '-aspect','16:9',
                           '-vf','crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,deinterlace,100M,60sec,3tb2d,40M,DoubleAction,noOverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = True
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = True
        _dict_input['_bool_rewrite_output'] = False
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-aspect','16:9',
                           '-vf','yadif=1',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4'],
                          ['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-aspect','16:9',
                           '-vf','yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass
        # h264_nvenc,deinterlace,100M,60sec,3tb2d,40M,DoubleAction,OverWriter
        _dict_input['_str_codec_video'] = 'h264_nvenc'
        _dict_input['_str_bitrate'] = '100M'
        _dict_input['_bool_video_deinterlace'] = True
        _dict_input['_bool_make_2d_l_from_top'] = True
        _dict_input['_str_bitrate_3dt2dl'] = '40M'
        _dict_input['_bool_double_action_3dt2dl'] = True
        _dict_input['_bool_rewrite_output'] = True
        self.assertEqual([['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','100M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '-aspect','16:9',
                           '-vf','yadif=1',
                           '/path/file.ext_00_00_00_to_00_01_00.mp4'],
                          ['ffmpeg',
                           '-ss','00:00:00',
                           '-i','/path/file.ext',
                           '-c:v','h264_nvenc',
                           '-map','0:v',
                           '-ac','2',
                           '-map','0:a',
                           '-b:v','40M',
                           '-t','60',
                           '-pix_fmt','yuv420p',
                           '-y',
                           '-aspect','16:9',
                           '-vf','yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
                           '/path/file.ext_00_00_00_to_00_01_00_3DTop2Left_2D.mp4']],
             make_list_for_cmd_array(_dict_input['_src_video_name_input'],
                 _dict_input['_bool_video_deinterlace'],
                 _dict_input['_str_codec_video'],
                 _dict_input['_str_bitrate'],
                 _dict_input['_start_timestamp'],
                 _dict_input['_duration'],
                 _dict_input['_dst_video_file'],
                 _dict_input['_bool_make_2d_l_from_top'],
                 _dict_input['_str_bitrate_3dt2dl'],
                 _dict_input['_bool_double_action_3dt2dl'],
                 _dict_input['_bool_rewrite_output']))
        pass


if __name__ == '__main__':
    unittest.main()
