import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

# 현재 스크립트의 디렉토리 경로
script_dir = os.path.dirname(os.path.abspath(__file__))

# 비디오 파일 정렬 및 경로 설정
video_files = sorted([
    os.path.join(script_dir, f)
    for f in os.listdir(script_dir)
    if f.endswith('.mp4') and '_part' in f
])

# 비디오 클립 객체 리스트 생성
clips = [VideoFileClip(f) for f in video_files]

# 비디오 클립 병합
final_clip = concatenate_videoclips(clips, method="compose")

# 병합된 비디오 저장
output_path = os.path.join(script_dir, "merged.mp4")
final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# 리소스 정리
for clip in clips:
    clip.close()
