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

# 示例：获取视频的总时长
video_path = "G:\\13_Video\\神断狄仁杰[2010][44集].1080P\\神断狄仁杰.第04集.1080P.mp4"
duration_seconds = get_video_duration(video_path)
print(f"Video duration: {duration_seconds} seconds")