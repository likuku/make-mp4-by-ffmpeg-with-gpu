'''
Copy Right by likuku
likuku.public@gmail.com
last update on Jan8,2018
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

dict_codec_video={'0':['h264_nvenc','H.264 with Nvidia GPU [默认]'],
                   '1':['libx264','H.264 with CPU'],
                   '2':['hevc_nvenc','H.265 with Nvidia GPU'],
                   '3':['libx265','H.265 with CPU'],
                   '4':['h264_videotoolbox','H.265 with GPU on macOS'],
                   '5':['copy','Copy data from Source,the Fastest']}

print('版本: v1.6.3 20171219')
print('请关闭系统里其他占用GPU的程序：3D游戏,3D渲染工具,AdobePR,AdobeMediaEncoder 等')
print('推荐使用 FFmpeg v3.3.x 版本，原因:')
print('FFmpeg v3.4 版本在 macOS 转码后打包文件时极机率会僵死无法完成','\n')

def get_str_raw_src_media_path_from_keyboard():
    pass
    _str_input_msg = '请输入素材文件路径 : '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)

def check_str_raw_src_media_path(_str_input):
    pass
    if len(_str_input) == 0:
        pass
        _bool_src_media_path = False
    else:
        _bool_src_media_path = os.access(_str_input.replace('"','').strip(),
                                         os.F_OK)
    return(_bool_src_media_path)

def rebuild_list_str_src_media_path(_str_input,_path_split_by):
    pass
    _str_src_input = _str_input.replace('"','').strip()
    # 路径里包含空格，则拖拽文件时，windows 会自动给首尾加一对双引号，subprocess 不需要
    _list_src_media_path_file = _str_src_input.rsplit(_path_split_by,1)
    return(_list_src_media_path_file)

def get_str_raw_deinterlace_from_keyboard():
    pass
    print('反交错滤镜 -fv yadif=1，消除隔行扫描/如1080i素材画面的锯齿/百叶窗条纹')
    _str_input_msg = ' 是否开启反交错处理 1[是]? 0[否]? 直接回车则默认为 0[否]: '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)

def rebuild_bool_deinterlace(_str_input):
    pass
    if len(_str_input) == 0 or _str_input == '0':
        pass
        _bool_deinterlace_input = False
    elif _str_input == '1':
        _bool_deinterlace_input = True
    else:
        print ('Error: 再次运行后,重新输入正确的选项代号')
        time.sleep(2)
        exit()
    return(_bool_deinterlace_input)

def show_dict_codec_video(_dict_input):
    pass
    print('视频编码器列表:')
    for _i in sorted(dict_codec_video.keys()):
        print(' %s. %s: %s' % (_i,dict_codec_video[_i][0],dict_codec_video[_i][1]))

def get_str_raw_codec_video_from_keyboard():
    pass
    _str_input_msg = ' 请输入视频编码器 序号(直接回车即选 [0]): '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)

def check_and_rebuild_str_codec_video(_str_input):
    pass
    try:
        pass
        if len(_str_input) == 0:
            pass
            _str_codec_video = dict_codec_video['0'][0]
        else:
            _str_codec_video = dict_codec_video[_str_input][0]
        return(_str_codec_video)
    except Exception as e:
            print ('Error: 再次运行后,重新输入正确的选项代号')
            time.sleep(2)
            exit()

def get_str_raw_bitrate_video_from_keyboard():
    pass
    _str_input_msg = ' 请输入视频码率，数字即可，单位为 MBits/sec 默认 80MBits/sec : '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)

def check_and_rebuild_str_bitrate_video(_str_input):
    pass
    if len(_str_input) == 0:
        pass
        _str_bitrate = '80M'
    else:
        _str_bitrate = '%sM' % _str_input
    return(_str_bitrate)

def get_str_cut_list_file_name_from_keyboard():
    pass
    print('''自动文件切片列表范例:
          00:00:00,00:07:07
          00:08:01,hh:mm:ss
          hh:mm:ss,hh:mm:ss
          每行定义一个切片，起止时刻以英文逗号分隔，.csv 扩展名
          也可用 Excel，Numbers，等表格软件制作，删除所有空白单元格后导出 .csv 文件
          ''')
    _str_input_msg = ' 请输入切片列表文件路径(不明白这是什么，请直接回车忽略) : '
    _str_input = str(input(_str_input_msg))
    _src_cut_list_input = _str_input.replace('"','').strip()
    if len(_src_cut_list_input) == 0:
        _src_cut_list_input = None
    return(_src_cut_list_input)

def get_bool_overwrite_output_from_keyboard():
    pass
    print('当输出文件已存在时，是否直接覆盖同名文件:')
    _str_input_msg = ' 1[是]? 0[否]? 直接回车则默认为 0[否]:'
    _str_input = str(input(_str_input_msg))
    _dict_bool_input = {'0':False,'1':True}
    try:
        pass
        if len(_str_input) == 0:
            pass
            _bool_deal = False
        else:
            _bool_deal = _dict_bool_input[_str_input]
        return(_bool_deal)
    except Exception as e:
            print ('Error: 再次运行后,重新输入正确的选项代号')
            time.sleep(2)
            exit()

def get_bool_make_2d_l_from_top_from_keyboard():
    pass
    print('是否从 上下(TB)3D 立体画面里抽取 上T(左眼) 并拉伸形成素材源尺寸单一2D画面:')
    _str_input_msg = ' 1[是]? 0[否]? 直接回车则默认为 0[否]:'
    _str_input = str(input(_str_input_msg))
    _dict_make2dl_from_top = {'0':False,'1':True}
    try:
        pass
        if len(_str_input) == 0:
            pass
            _bool_make_2d_l_from_top = False
        else:
            _bool_make_2d_l_from_top = _dict_make2dl_from_top[_str_input]
        return(_bool_make_2d_l_from_top)
    except Exception as e:
            print ('Error: 再次运行后,重新输入正确的选项代号')
            time.sleep(2)
            exit()

def get_str_bitrate_make_2d_l_from_top_from_keyboard():
    pass
    print('设定 3DTop2Left_2D 视频码率: ')
    _str_input_msg = ' 请输入视频码率，数字即可，单位为 MBits/sec 默认 40MBits/sec : '
    _src_bitrate_input = str(input(_str_input_msg))
    if len(_src_bitrate_input) == 0:
        pass
        _str_bitrate = '40M'
    else:
        _str_bitrate = '%sM' % _src_bitrate_input
    return(_str_bitrate)

def set_bitrate_for_3Dtop2Dleft_from_list_for_cmd_array(_list_cmd_array,
                                                        _str_bitrate):
    pass
    if _str_bitrate == None:
        pass
    else:
        for _index in list(range(len(_list_cmd_array))):
            if ('crop=iw:(ih/2):0:0,scale=iw:(ih*2)' in
                _list_cmd_array[_index]
                or 'yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)' in
                _list_cmd_array[_index]):
                pass
                _cmd_array = _list_cmd_array[_index]
                _list_cmd_array[_index][_cmd_array.index('-b:v')+1] = _str_bitrate
            else:
                pass
    return(_list_cmd_array)

def set_aspect_16x9_for_3Dtop2Dleft_from_list_for_cmd_array(_list_cmd_array):
    for _index in list(range(len(_list_cmd_array))):
        if ('crop=iw:(ih/2):0:0,scale=iw:(ih*2)' in
            _list_cmd_array[_index]
            or 'yadif=1,crop=iw:(ih/2):0:0,scale=iw:(ih*2)' in
            _list_cmd_array[_index]):
            pass
            _cmd_array = _list_cmd_array[_index]
            _list_cmd_array[_index].insert(_cmd_array.index('-vf'),'-aspect')
            _list_cmd_array[_index].insert(_cmd_array.index('-vf'),'16:9')
        else:
            pass
    return(_list_cmd_array)

def set_ar_44100hz_for_nocopy_from_list_for_cmd_array(_list_cmd_array):
    for _index in list(range(len(_list_cmd_array))):
        if ('-ac' in _list_cmd_array[_index]):
            _cmd_array = _list_cmd_array[_index]
            _list_cmd_array[_index].insert(_cmd_array.index('-ac'),'-ar')
            _list_cmd_array[_index].insert(_cmd_array.index('-ac'),'44100')
        else:
            pass
    return(_list_cmd_array)

def get_bool_double_action_for_3d_2d_from_keyboard():
    pass
    print('是否同时输出 上下(TB)3D 画面:')
    _str_input_msg = ' 1[是]? 0[否]? 直接回车则默认为 0[否]:'
    _str_input = str(input(_str_input_msg))
    _dict_map_bool = {'0':False,'1':True}
    try:
        pass
        if len(_str_input) == 0:
            pass
            _bool_double_action_3d2d = False
        else:
            _bool_double_action_3d2d = _dict_map_bool[_str_input]
        return(_bool_double_action_3d2d)
    except Exception as e:
            print ('Error: 再次运行后,重新输入正确的选项代号')
            time.sleep(2)
            exit()

def rebuild_str_timestamp_input(_str_input):
    pass
    _list_str_timestamp = list(map(lambda x:'%02d' % int(x),_str_input.split(':')))
    _str_input = ':'.join(_list_str_timestamp)
    return(_str_input)

def get_str_start_timestamp_from_keyboard():
    pass
    _str_input_msg = ' 请输入选择的视频片段开始时刻，时间戳格式 HH:mm:ss ,默认 00:00:00 : '
    _src_start_timestamp_input = str(input(_str_input_msg))
    if len(_src_start_timestamp_input) == 0:
        pass
        _src_start_timestamp_input = '00:00:00'
    else:
        pass
        _src_start_timestamp_input = rebuild_str_timestamp_input(_src_start_timestamp_input)
    return(_src_start_timestamp_input)

def get_str_end_timestamp_from_keyboard():
    pass
    _str_input_msg = ' 请输入选择的视频片段结束时刻，时间戳格式 HH:mm:ss ,默认 源视频结尾 : '
    _src_end_timestamp_input = str(input(_str_input_msg))
    if len(_src_end_timestamp_input) == 0:
        pass
        _src_end_timestamp_input = None
    else:
        pass
        _src_end_timestamp_input = rebuild_str_timestamp_input(_src_end_timestamp_input)
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

def make_str_dst_video_file(_start_timestamp,
                            _end_stimestamp,
                            _src_video_path,
                            _src_video_file_name):
    pass
    if _end_stimestamp == None:
        pass
        _dst_video_file_name = '%s_%s_to_end'% (_src_video_file_name,
            _start_timestamp.replace(':','_'))
    else:
        _dst_video_file_name = '%s_%s_to_%s'% (_src_video_file_name,
            _start_timestamp.replace(':','_'),
            _end_stimestamp.replace(':','_'))
    _dst_video_file = '%s%s%s' % (_src_video_path,
                                  path_split_by,
                                  _dst_video_file_name)
    return(_dst_video_file)

def make_array_vf(src_codec_video_deinterlace_input,
                str_make_2d_l_from_top,):
    pass
    _array = []
    if src_codec_video_deinterlace_input:
        pass
        _array.append('yadif=1')
    else:
        pass
    if str_make_2d_l_from_top:
        _array.append('crop=iw:(ih/2):0:0,scale=iw:(ih*2)')
    else:
        pass
    if len(_array) == 0:
        pass
        _array_vf = None
    elif len(_array) > 0:
        _array_vf = ['-vf','%s' % (','.join(_array))]
    else:
        pass
    return(_array_vf)

def make_cmd_array_for_copy(_start_timestamp,
                            _src_video_name_input,
                            _str_codec_video,
                            _duration):
    pass
    _cmd_array = ['%s' % ffmpeg_name,
        '-ss','%s' % _start_timestamp,
        '-i','%s' % _src_video_name_input,
        '-c','%s' % _str_codec_video,
        '-t','%s' % _duration]
    return(_cmd_array)

def make_cmd_array_for_other(_start_timestamp,
                             _src_video_name_input,
                             _str_codec_video,
                             _str_bitrate,
                             _duration):
    pass
    _cmd_array = ['%s' % ffmpeg_name,
        '-ss','%s' % _start_timestamp,
        '-i','%s' % _src_video_name_input,
        '-c:v','%s' % _str_codec_video,
        '-map','0:v',
        '-ac','2',
        '-map','0:a',
        '-b:v','%s' % _str_bitrate,
        '-t','%s' % _duration,
        '-pix_fmt','yuv420p']
    return(_cmd_array)

def make_list_for_cmd_array(_src_video_name_input,
                            _bool_video_deinterlace,
                            _str_codec_video,
                            _str_bitrate,
                            _start_timestamp,
                            _duration,
                            _dst_video_file,
                            _bool_make_2d_l_from_top,
                            _str_bitrate_3dt2dl,
                            _bool_double_action_3dt2dl,
                            _bool_overwrite_output):
    pass
    if _str_codec_video == 'copy':
        pass
        _cmd_array = make_cmd_array_for_copy(_start_timestamp,
                                    _src_video_name_input,
                                    _str_codec_video,
                                    _duration)
        if _bool_overwrite_output:
            pass
            _cmd_array = _cmd_array + ['-y']
        else:
            pass
        _cmd_array = _cmd_array + ['%s.%s' % (_dst_video_file,
                       (_src_video_name_input.rsplit('.',1)[1]))]
        _list_for_cmd_array = []
        _list_for_cmd_array.append(_cmd_array)
    else:
        _cmd_array = make_cmd_array_for_other(_start_timestamp,
                                              _src_video_name_input,
                                              _str_codec_video,
                                              _str_bitrate,
                                              _duration)
        if _bool_overwrite_output:
            pass
            _cmd_array = _cmd_array + ['-y']
        else:
            pass
        _array_vf = make_array_vf(_bool_video_deinterlace,
                              _bool_make_2d_l_from_top)
        if _bool_make_2d_l_from_top:
            pass
            if _bool_double_action_3dt2dl:
                pass
                _list_for_cmd_array = []
                if _bool_video_deinterlace:
                    pass
                    _list_for_cmd_array.append(_cmd_array + ['-vf','yadif=1','%s.mp4' % _dst_video_file])
                else:
                    _list_for_cmd_array.append(_cmd_array + ['%s.mp4' % _dst_video_file])
                _list_for_cmd_array.append(_cmd_array + _array_vf + ['%s_3DTop2Left_2D.mp4' % _dst_video_file])
            else:
                _list_for_cmd_array = []
                _list_for_cmd_array.append(_cmd_array + _array_vf + ['%s_3DTop2Left_2D.mp4' % _dst_video_file])
        elif _bool_video_deinterlace:
            pass
            _cmd_array = _cmd_array + _array_vf + ['%s.mp4' % _dst_video_file]
            _list_for_cmd_array = []
            _list_for_cmd_array.append(_cmd_array)
        else:
            _cmd_array = _cmd_array + ['%s.mp4' % _dst_video_file]
            _list_for_cmd_array = []
            _list_for_cmd_array.append(_cmd_array)
        _list_for_cmd_array = set_bitrate_for_3Dtop2Dleft_from_list_for_cmd_array(
            _list_for_cmd_array,_str_bitrate_3dt2dl)
        _list_for_cmd_array = set_aspect_16x9_for_3Dtop2Dleft_from_list_for_cmd_array(
            _list_for_cmd_array)
        _list_for_cmd_array = set_ar_44100hz_for_nocopy_from_list_for_cmd_array(
            _list_for_cmd_array)
    return(_list_for_cmd_array)

def main(_dev_mode):
    pass
    _tmp_src_media_path = get_str_raw_src_media_path_from_keyboard()
    if check_str_raw_src_media_path(_tmp_src_media_path):
        pass
        _tmp_src_media_path_list = rebuild_list_str_src_media_path(_tmp_src_media_path,
                                                                   path_split_by)
        _src_video_file_name = _tmp_src_media_path_list[1]
        _src_video_path = _tmp_src_media_path_list[0]
        _src_video_name_input = '%s%s%s' % (_src_video_path,
                                           path_split_by,
                                           _src_video_file_name)
    else:
        print('素材文件无法访问，再次运行后,重新输入')
        time.sleep(2)
        exit()
    show_dict_codec_video(dict_codec_video)
    src_codec_video_input = get_str_raw_codec_video_from_keyboard()
    str_codec_video = check_and_rebuild_str_codec_video(src_codec_video_input)
    if str_codec_video == 'copy':
        pass
        str_bitrate = None
        bool_video_deinterlace = False
        print('已选择纯剪切不编码的 copy 模式:')
    else:
        _tmp_deinterlace = get_str_raw_deinterlace_from_keyboard()
        bool_video_deinterlace = rebuild_bool_deinterlace(_tmp_deinterlace)
        _src_bitrate_input = get_str_raw_bitrate_video_from_keyboard()
        str_bitrate = check_and_rebuild_str_bitrate_video(_src_bitrate_input)
    str_cut_list_file_name = get_str_cut_list_file_name_from_keyboard()
    if str_cut_list_file_name == None:
        pass
        _bool_overwrite_output = False
        str_start_timestamp = get_str_start_timestamp_from_keyboard()
        str_end_stimestamp = get_str_end_timestamp_from_keyboard()
        str_duration = make_str_duration(str_start_timestamp,
                                         str_end_stimestamp)
        str_dst_video_file = make_str_dst_video_file(str_start_timestamp,
                                                     str_end_stimestamp,
                                                     _src_video_path,
                                                     _src_video_file_name)
        if str_codec_video != 'copy':
            _bool_3dt2dl = get_bool_make_2d_l_from_top_from_keyboard()
            if _bool_3dt2dl:
                pass
                _str_bitrate_3dt2dl = get_str_bitrate_make_2d_l_from_top_from_keyboard()
                _bool_double_3dt2dl = get_bool_double_action_for_3d_2d_from_keyboard()
            else:
                pass
                _str_bitrate_3dt2dl,_bool_double_3dt2dl = None,False
        else:
            pass
            _bool_3dt2dl,_bool_double_3dt2dl = False,False
            _str_bitrate_3dt2dl = None
        _list_for_cmd_array = make_list_for_cmd_array(_src_video_name_input,
                                                      bool_video_deinterlace,
                                                      str_codec_video,
                                                      str_bitrate,
                                                      str_start_timestamp,
                                                      str_duration,
                                                      str_dst_video_file,
                                                      _bool_3dt2dl,
                                                      _str_bitrate_3dt2dl,
                                                      _bool_double_3dt2dl,
                                                      _bool_overwrite_output)
        for _cmd_array in _list_for_cmd_array:
            if _dev_mode is True:
                print(_cmd_array)
                continue
            else:
                print(_cmd_array)
                subprocess.call(_cmd_array)
        pass
    else:
        pass
        _bool_overwrite_output = get_bool_overwrite_output_from_keyboard()
        if str_codec_video != 'copy':
            _bool_3dt2dl = get_bool_make_2d_l_from_top_from_keyboard()
            if _bool_3dt2dl:
                pass
                _str_bitrate_3dt2dl = get_str_bitrate_make_2d_l_from_top_from_keyboard()
                _bool_double_3dt2dl = get_bool_double_action_for_3d_2d_from_keyboard()
            else:
                pass
                _str_bitrate_3dt2dl,_bool_double_3dt2dl = None,False
        else:
            pass
            _bool_3dt2dl,_bool_double_3dt2dl = False,False
            _str_bitrate_3dt2dl = None
        with open(str_cut_list_file_name, 'r') as _raw_cut_list_file:
            for _line in _raw_cut_list_file.readlines():
                _list_line = _line.strip().split(',')
                str_start_timestamp = _list_line[0]
                str_end_stimestamp = _list_line[1]
                str_duration = make_str_duration(str_start_timestamp,
                                                 str_end_stimestamp)
                str_dst_video_file = make_str_dst_video_file(str_start_timestamp,
                                                             str_end_stimestamp,
                                                             _src_video_path,
                                                             _src_video_file_name)
                _list_for_cmd_array = make_list_for_cmd_array(_src_video_name_input,
                                                              bool_video_deinterlace,
                                                              str_codec_video,
                                                              str_bitrate,
                                                              str_start_timestamp,
                                                              str_duration,
                                                              str_dst_video_file,
                                                              _bool_3dt2dl,
                                                              _str_bitrate_3dt2dl,
                                                              _bool_double_3dt2dl,
                                                              _bool_overwrite_output)
                for _cmd_array in _list_for_cmd_array:
                    if _dev_mode is True:
                        print(_cmd_array)
                        continue
                    else:
                        print(_cmd_array)
                        subprocess.call(_cmd_array)
                pass


if __name__ == '__main__':
    _dev_mode = True
    main(_dev_mode)
