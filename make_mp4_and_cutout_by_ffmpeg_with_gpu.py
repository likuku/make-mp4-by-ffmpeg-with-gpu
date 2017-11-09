'''
Copy Right by likuku
kuku.li@fanc.co
last update on Nov9,2017
先决条件:
安装 ffmpeg-static for windows,给当前用户增加环境变量
安装 python3 for windows,默认安装 # .py 会与 python 解析器自动关联
'''

import sys
import os
import subprocess
import datetime
import time

print('版本: v1.1 20171103')
print('请关闭系统里其他占用GPU的程序：3D游戏,3D渲染工具,AdobePR,AdobeMediaEncoder 等\n')
print('请输入素材文件路径 :' )
_src_video_name_input=input().replace('"','')
# 路径里包含空格，则拖拽文件时，windows 会自动给首尾加一对双引号，subprocess 不需要
_src_video_file_name = _src_video_name_input.rsplit('\\',1)[1]
_src_video_path = _src_video_name_input.rsplit('\\',1)[0]
_check_file_name = lambda _x : (_x.rsplit('.',1)[0].count('Capture') +
                                _x.rsplit('.',1)[1].count('mov')) == 2
_src_video_made_by_bmd = _check_file_name(_src_video_file_name)

print('\n反交错滤镜 -fv yadif=1，消除隔行扫描/如1080i素材画面的锯齿/百叶窗条纹')
print('是否开启反交错处理 1[是]? 0[否]? 直接回车则默认为 0[否]:')
_src_codec_video_deinterlace_input=input()
if len(_src_codec_video_deinterlace_input) == 0:
    pass
    _src_codec_video_deinterlace_input = False
elif _src_codec_video_deinterlace_input == '0':
    _src_codec_video_deinterlace_input = False
elif _src_codec_video_deinterlace_input == '1':
    _src_codec_video_deinterlace_input = True
else:
    print ('Error: 再次运行后,重新输入正确的选项代号')
    time.sleep(2)
    exit()

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

def make_cmd_array_for_bmd_recorder():
    pass
    _cmd_array = ['ffmpeg.exe','-ss','%s' % _src_start_timestamp_input,
        '-i','%s' % _src_video_name_input,
        '-c:v','%s' % _src_codec_video_input,
        '-map','0:1',
        '-ac','2',
        '-map','0:2',
        '-b:v','%s' % _bitrate,
        '-t','%s' % _duration,
        '-pix_fmt','yuv420p']
    return(_cmd_array)

def make_cmd_array_for_other():
    pass
    _cmd_array = ['ffmpeg.exe','-ss','%s' % _src_start_timestamp_input,
        '-i','%s' % _src_video_name_input,
        '-c:v','%s' % _src_codec_video_input,
        '-b:v','%s' % _bitrate,
        '-t','%s' % _duration,
        '-pix_fmt','yuv420p']
    return(_cmd_array)

print ('_src_codec_video_deinterlace_input:',_src_codec_video_deinterlace_input)

if _src_video_made_by_bmd:
    pass
    _cmd = make_cmd_array_for_bmd_recorder()
else:
    _cmd = make_cmd_array_for_other()
if _src_codec_video_deinterlace_input:
    pass
    _cmd = _cmd + ['-vf','yadif=1'] + ['%s.mp4' % _dst_video_file]
else:
    _cmd = _cmd + ['%s.mp4' % _dst_video_file]

print(_cmd)
subprocess.call(_cmd)
