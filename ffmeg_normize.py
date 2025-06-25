#pip install ffmpeg-python

import ffmpeg

input_path = "E:/python_test/Nothings Gonna Change My Love For You.mp4"         # 원본 영상
output_path = "normalized.mp4"    # 결과 파일 (이름은 원하는 대로)


ffmpeg.input(input_path).output(
    output_path,
    af='loudnorm=I=-14:TP=-1.5:LRA=11',
    **{'c:v': 'copy'}  # 영상은 다시 인코딩하지 않음
).run()
