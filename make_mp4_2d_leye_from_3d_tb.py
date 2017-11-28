'''
Copy Right by likuku
kuku.li@fanc.co
last update on Nov28,2017
先决条件:
安装 ffmpeg-static for windows,给当前用户增加环境变量
安装 python3 for windows,默认安装 # .py 会与 python 解析器自动关联
'''

import sys
import os
import subprocess
import platform

str_os_type = platform.system()
if str_os_type == 'Windows':
    pass
    path_split_by = '\\'
    ffmpeg_name = 'ffmpeg.exe'
else:
    path_split_by = '/'
    ffmpeg_name = 'ffmpeg'

print('请关闭系统里其他占用GPU的程序：3D游戏,3D渲染工具,AdobePR,AdobeMediaEncoder 等')
print('推荐使用 FFmpeg v3.3.x 版本，原因:')
print('FFmpeg v3.4 版本在 macOS 转码后打包文件时极机率会僵死无法完成','\n')
_str_input_msg = '请拖拽素材文件所在目录到此 : '
_src_video_dir_input = str(input(_str_input_msg)).replace('"','').strip()
# 路径里包含空格，则拖拽文件时，windows 会自动给首尾加一对双引号，subprocess 不需要

def make_cmd_array(_src_video):
    pass
    _cmd_array = ['%s' % ffmpeg_name,
        '-i','%s' % _src_video,
        '-c:v','h264_nvenc',
        '-vf','crop=iw:(ih/2):0:0,scale=iw:(ih*2)',
        '-aspect','16:9',
        '-map','0:v',
        '-ac','2',
        '-map','0:a',
        '-b:v','80M',
        '-pix_fmt','yuv420p',
        '-y',
        '%s_3DTop2Left_2D.mp4' % _src_video]
    return(_cmd_array)

try:
    _list_src_video = os.listdir(_src_video_dir_input)
    for _video in _list_src_video:
        _cmd_array = make_cmd_array('%s%s%s' % (_src_video_dir_input,
                                                path_split_by,
                                                _video))
        print(_cmd_array)
        #continue
        subprocess.call(_cmd_array)
except Exception as e:
    raise
