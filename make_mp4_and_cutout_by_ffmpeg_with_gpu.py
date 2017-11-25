'''
Copy Right by likuku
kuku.li@fanc.co
last update on Nov25,2017
先决条件:
安装 ffmpeg-static for windows,给当前用户增加环境变量
安装 python3 for windows,默认安装 # .py 会与 python 解析器自动关联
'''

import sys
import os
import subprocess
import datetime
import time
import platform

str_os_type = platform.system()
if str_os_type == 'Windows':
    pass
    path_split_by = '\\'
    ffmpeg_name = 'ffmpeg.exe'
else:
    path_split_by = '/'
    ffmpeg_name = 'ffmpeg'

print('版本: v1.4.2 20171125')
print('请关闭系统里其他占用GPU的程序：3D游戏,3D渲染工具,AdobePR,AdobeMediaEncoder 等\n')
print('请输入素材文件路径 :' )
src_video_name_input=input().replace('"','').strip()
# 路径里包含空格，则拖拽文件时，windows 会自动给首尾加一对双引号，subprocess 不需要
src_video_name_input_list = src_video_name_input.rsplit(path_split_by,1)
src_video_file_name = src_video_name_input_list[1]
src_video_path = src_video_name_input_list[0]

print('\n反交错滤镜 -fv yadif=1，消除隔行扫描/如1080i素材画面的锯齿/百叶窗条纹')
print('是否开启反交错处理 1[是]? 0[否]? 直接回车则默认为 0[否]:')
src_codec_video_deinterlace_input=input()
if len(src_codec_video_deinterlace_input) == 0:
    pass
    src_codec_video_deinterlace_input = False
elif src_codec_video_deinterlace_input == '0':
    src_codec_video_deinterlace_input = False
elif src_codec_video_deinterlace_input == '1':
    src_codec_video_deinterlace_input = True
else:
    print ('Error: 再次运行后,重新输入正确的选项代号')
    time.sleep(2)
    exit()

_dict_codec_video={'0':['h264_nvenc','H.264 with Nvidia GPU [默认]'],
                   '1':['libx264','H.264 with CPU'],
                   '2':['hevc_nvenc','H.265 with Nvidia GPU'],
                   '3':['libx265','H.265 with CPU'],
                   '4':['h264_videotoolbox','H.265 with GPU on macOS'],
                   '5':['copy','Copy data from Source,the Fastest']}

print('视频编码器列表:')
for _i in _dict_codec_video.keys():
    print(' %s. %s: %s' % (_i,_dict_codec_video[_i][0],_dict_codec_video[_i][1]))
print('请输入视频编码器 序号(直接回车即选 0):')
_src_codec_video_input=input()

try:
    pass
    if len(_src_codec_video_input) == 0:
        pass
        str_codec_video = _dict_codec_video['0'][0]
    else:
        str_codec_video = _dict_codec_video[_src_codec_video_input][0]
except Exception as e:
        print ('Error: 再次运行后,重新输入正确的选项代号')
        time.sleep(2)
        exit()

if str_codec_video == 'copy':
    pass
    print('已选择纯剪切不编码的 copy 模式:')
else:
    print('请输入视频码率，数字即可，单位为 MBits/sec 默认 100MBits/sec :')
    _src_bitrate_input=input()
    if len(_src_bitrate_input) == 0:
        pass
        str_bitrate = '100M'
    else:
        str_bitrate = '%sM' % _src_bitrate_input

def get_str_cut_list_file_name_from_keyboard():
    pass
    print('''自动文件切片列表范例:
          00:00:00,00:07:07
          00:08:01,hh:mm:ss
          hh:mm:ss,hh:mm:ss
          每行定义一个切片，起止时刻以英文逗号分隔，.csv 扩展名
          也可用 Excel，Numbers，等表格软件制作，删除所有空白单元格后导出 .csv 文件
          ''')
    print('请输入切片列表文件路径(不明白这是什么，请直接回车忽略) :' )
    _src_cut_list_input=input().replace('"','').strip()
    if len(_src_cut_list_input) == 0:
        _src_cut_list_input = None
    return(_src_cut_list_input)

def get_str_start_timestamp_from_keyboard():
    pass
    print('请输入选择的视频片段开始时刻，时间戳格式 HH:mm:ss ,默认 00:00:00 :')
    _src_start_timestamp_input=input()
    if len(_src_start_timestamp_input) == 0:
        pass
        _src_start_timestamp_input = '00:00:00'
    return(_src_start_timestamp_input)

def get_str_end_timestamp_from_keyboard():
    pass
    print('请输入选择的视频片段结束时刻，时间戳格式 HH:mm:ss ,默认 源视频结尾 :')
    _src_end_timestamp_input=input()
    if len(_src_end_timestamp_input) == 0:
        pass
        _src_end_timestamp_input = None
    return(_src_end_timestamp_input)

def make_str_duration(_start_timestamp,_end_stimestamp):
    pass
    if _end_stimestamp == None:
        pass
        _duration = '999999999'
    else:
        _ss_list = _start_timestamp.split(':')
        _to_list = _end_stimestamp.split(':')
        _time_ss = datetime.timedelta(hours=int(_ss_list[0]),
                                      minutes=int(_ss_list[1]),
                                      seconds=int(_ss_list[2]))
        _time_to = datetime.timedelta(hours=int(_to_list[0]),
                                      minutes=int(_to_list[1]),
                                      seconds=int(_to_list[2]))
        _duration = str(int((_time_to - _time_ss).total_seconds()))
    return(_duration)

def make_str_dst_video_file(_start_timestamp,_end_stimestamp):
    pass
    if _end_stimestamp == None:
        pass
        _dst_video_file_name = '%s_%s_to_end'% (src_video_file_name,
            _start_timestamp.replace(':','_'))
    else:
        _dst_video_file_name = '%s_%s_to_%s'% (src_video_file_name,
            _start_timestamp.replace(':','_'),
            _end_stimestamp.replace(':','_'))
    _dst_video_file = '%s%s%s' % (src_video_path,
                                  path_split_by,
                                  _dst_video_file_name)
    return(_dst_video_file)

def make_cmd_array_for_copy(_start_timestamp,_duration):
    pass
    _cmd_array = ['%s' % ffmpeg_name,
        '-ss','%s' % _start_timestamp,
        '-i','%s' % src_video_name_input,
        '-c','%s' % str_codec_video,
        '-t','%s' % _duration]
    return(_cmd_array)

def make_cmd_array_for_other(_start_timestamp,_duration):
    pass
    _cmd_array = ['%s' % ffmpeg_name,
        '-ss','%s' % _start_timestamp,
        '-i','%s' % src_video_name_input,
        '-c:v','%s' % str_codec_video,
        '-map','0:v',
        '-ac','2',
        '-map','0:a',
        '-b:v','%s' % str_bitrate,
        '-t','%s' % _duration,
        '-pix_fmt','yuv420p']
    return(_cmd_array)

def make_str_cmd(_start_timestamp,_duration,_dst_video_file):
    pass
    if str_codec_video == 'copy':
        pass
        _cmd = make_cmd_array_for_copy(_start_timestamp,_duration)
        _cmd = _cmd + ['%s.%s' % (_dst_video_file,
                       (src_video_file_name.rsplit('.',1)[1]))]
    else:
        _cmd = make_cmd_array_for_other(_start_timestamp,_duration)
    if src_codec_video_deinterlace_input and (str_codec_video != 'copy'):
        pass
        _cmd = _cmd + ['-vf','yadif=1'] + ['%s.mp4' % _dst_video_file]
    elif str_codec_video != 'copy':
        _cmd = _cmd + ['%s.mp4' % _dst_video_file]
    return(_cmd)

def main():
    pass
    str_cut_list_file_name = get_str_cut_list_file_name_from_keyboard()
    if str_cut_list_file_name == None:
        pass
        str_start_timestamp = get_str_start_timestamp_from_keyboard()
        str_end_stimestamp = get_str_end_timestamp_from_keyboard()
        str_duration = make_str_duration(str_start_timestamp,
                                         str_end_stimestamp)
        str_dst_video_file = make_str_dst_video_file(str_start_timestamp,
                                                     str_end_stimestamp)
        _cmd = make_str_cmd(str_start_timestamp,str_duration,str_dst_video_file)
        print(_cmd)
        #exit()
        subprocess.call(_cmd)
    else:
        pass
        with open(str_cut_list_file_name, 'r') as _raw_cut_list_file:
            for _line in _raw_cut_list_file.readlines():
                _list_line = _line.strip().split(',')
                str_start_timestamp = _list_line[0]
                str_end_stimestamp = _list_line[1]
                str_duration = make_str_duration(str_start_timestamp,
                                                 str_end_stimestamp)
                str_dst_video_file = make_str_dst_video_file(str_start_timestamp,
                                                             str_end_stimestamp)
                _cmd = make_str_cmd(str_start_timestamp,str_duration,
                                    str_dst_video_file)
                print(_cmd)
                #continue
                subprocess.call(_cmd)


if __name__ == '__main__':
    main()
