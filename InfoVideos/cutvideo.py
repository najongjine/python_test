"""
pip install moviepy==1.0.3
"""

import os
from moviepy.video.io.VideoFileClip import VideoFileClip


def split_video_by_size(input_file, target_size_mb=4):
    # 비디오 클립 로드
    clip = VideoFileClip(input_file)
    total_duration = clip.duration  # 전체 길이 (초)
    total_size = os.path.getsize(input_file)  # 전체 파일 크기 (바이트)
    total_size_mb = total_size / (1024 * 1024)  # 전체 파일 크기 (MB)

    # 분할할 조각 수 계산
    num_parts = int(total_size_mb // target_size_mb) + 1
    part_duration = total_duration / num_parts  # 각 조각의 길이 (초)

    base_name, ext = os.path.splitext(input_file)

    for i in range(num_parts):
        start_time = i * part_duration
        end_time = min((i + 1) * part_duration, total_duration)
        subclip = clip.subclip(start_time, end_time)
        output_filename = f"{base_name}_part{i + 1}{ext}"
        subclip.write_videofile(output_filename, codec="libx264", audio_codec="aac")

    clip.close()

script_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_dir, '피그마로 웹사이트 10초 안에 베껴오기 [MAdq_B4_4_w].mp4')
# 사용 예시
split_video_by_size(video_path, target_size_mb=4)
