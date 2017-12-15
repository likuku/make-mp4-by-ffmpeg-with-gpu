'''
Copy Right by likuku
kuku.li@fanc.co
last update on Jul7,2017
先决条件:
安装 ffmpeg-static for windows,给当前用户增加环境变量
安装 python3 for windows,默认安装 # .py 会与 python 解析器自动关联
make_mp4_from_images.py 与 序列帧目录 在同一个父目录下
'''

import sys
import os
import subprocess

print('请输入序列帧目录名:' )
_src_dir_name_input=input()
print('请输入帧率:')
_src_fps_input=input()

subprocess.call(['ffmpeg.exe','-r','%s' % _src_fps_input,
    '-f','image2',
    '-i','%s/img%%05d.jpg' % _src_dir_name_input,
    '-r','%s' % _src_fps_input,
    '-vcodec','h264','-pix_fmt','yuv420p','-y',
    '%s.mp4' % _src_dir_name_input])

# 测试:
#print(['ffmpeg.exe','-f','image2','-i','%s/img%%05d.jpg' % _src_dir_name_input,'-r','60',
#    '-vcodec','h264','-pix_fmt','yuv420p','-y','%s.mp4' % _src_dir_name_input])
