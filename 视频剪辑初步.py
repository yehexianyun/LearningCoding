import subprocess
import json

def get_video_duration(video_path):
    """
    使用ffprobe获取视频的总时长。

    参数:
    - video_path: 视频文件的路径。

    返回:
    - 视频的总时长，以秒为单位。
    """
    # 构建ffprobe命令，以获取视频信息的JSON格式
    command = [
        'ffprobe',
        '-v', 'error',  # 不显示错误信息
        '-show_entries', 'format=duration',  # 只获取时长
        '-of', 'default=noprint_wrappers=1:nokey=1',  # 输出格式
        '-of', 'json',  # 输出为JSON格式
        video_path
    ]

    # 执行命令并捕获输出
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 解析JSON输出
    duration = json.loads(result.stdout)

    return float(duration['format']['duration'])


import os
filepath = "G:\\等待清单\\神断狄仁杰\\"
filelist = os.listdir(filepath)
filelist.pop(0)
filelist = [filepath + x for x in filelist]

lengthlist = [get_video_duration(x) for x in filelist]


def trim_audio(input_file, output_file, start_time, end_time):
    """
    使用ffmpeg裁剪音频文件。

    参数:
    input_file (str): 输入音频文件的路径。
    output_file (str): 输出音频文件的路径。
    start_time (int): 裁剪开始的时间，单位为秒。
    end_time (int): 裁剪结束的时间，单位为秒。
    """
    command = [
        'ffmpeg',
        '-i', input_file,           # 输入文件
        '-ss', str(start_time),     # 裁剪开始时间
        '-to', str(end_time),       # 裁剪结束时间
        '-c', 'copy',               # 使用相同的编解码器复制音轨
        output_file                 # 输出文件
    ]
    subprocess.run(command, check=True)


endlist = [ x-148 for x in lengthlist]
for i in range(len(filelist)):
    trim_audio(filelist[i], f"{i}.mp3", 216, endlist[i])