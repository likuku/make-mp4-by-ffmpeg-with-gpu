'''
Copy Right by likuku
kuku.li@fanc.co
last update on Oct30,2017
先决条件:
安装 ffmpeg-static for windows,给当前用户增加环境变量
安装 python3 for windows,默认安装 # .py 会与 python 解析器自动关联
'''

import sys
import os
import subprocess
import datetime

print('请输入录像文件路径 :' )
_src_video_name_input=input()
_src_video_file_name = _src_video_name_input.rsplit('\\',1)[1]
_src_video_path = _src_video_name_input.rsplit('\\',1)[0]

print('请输入视频编码器 H264:h264_nvenc,libx264 H265/HEVC:hevc_nvenc,libx265 默认 h264_nvenc:')
_src_codec_video_input=input()
if len(_src_codec_video_input) == 0:
    pass
    _src_codec_video_input = 'h264_nvenc'

print('请输入视频码率，数字即可，单位为 MBits/sec 默认 100MBits/sec :')
_src_bitrate_input=input()
if len(_src_bitrate_input) == 0:
    pass
    _bitrate = '100M'
else:
    _bitrate = '%sM' % _src_bitrate_input

print('请输入选择的视频片段开始时刻，时间戳格式 HH:mm:ss ,默认 00:00:00 :')
_src_start_timestamp_input=input()
if len(_src_start_timestamp_input) == 0:
    pass
    _src_start_timestamp_input = '00:00:00'

print('请输入选择的视频片段结束时刻，时间戳格式 HH:mm:ss ,默认 源视频结尾 :')
_src_end_timestamp_input=input()
if len(_src_end_timestamp_input) == 0:
    pass
    _src_end_timestamp_input = None
    _duration = '999999999'
    _dst_video_file_name = '%s_%s_to_end'% (_src_video_file_name,
        _src_start_timestamp_input.replace(':','_'))
    _dst_video_file = '%s\\%s' % (_src_video_path,_dst_video_file_name)
else:
    _ss_list = _src_start_timestamp_input.split(':')
    _to_list = _src_end_timestamp_input.split(':')
    _time_ss = datetime.timedelta(hours=int(_ss_list[0]),
                                  minutes=int(_ss_list[1]),
                                  seconds=int(_ss_list[2]))
    _time_to = datetime.timedelta(hours=int(_to_list[0]),
                                  minutes=int(_to_list[1]),
                                  seconds=int(_to_list[2]))
    _duration = str(int((_time_to - _time_ss).total_seconds()))
    _dst_video_file_name = '%s_%s_to_%s'% (_src_video_file_name,
        _src_start_timestamp_input.replace(':','_'),
        _src_end_timestamp_input.replace(':','_'))
    _dst_video_file = '%s\\%s' % (_src_video_path,_dst_video_file_name)

print(['ffmpeg.exe','-ss','%s' % _src_start_timestamp_input,
    '-i','%s' % _src_video_name_input,
    '-c:v','%s' % _src_codec_video_input,
    '-b:v','%s' % _bitrate,
    '-t','%s' % _duration,
    '-pix_fmt','yuv420p',
    '%s.mp4' % _dst_video_file])

print()

subprocess.call(['ffmpeg.exe','-ss','%s' % _src_start_timestamp_input,
    '-i','%s' % _src_video_name_input,
    '-c:v','%s' % _src_codec_video_input,
    '-b:v','%s' % _bitrate,
    '-t','%s' % _duration,
    '-pix_fmt','yuv420p',
    '%s.mp4' % _dst_video_file])
