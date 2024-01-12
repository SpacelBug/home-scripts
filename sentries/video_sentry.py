from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import ffmpeg
import os


def print_video_info(path):
    video_file = VideoFileClip(path)

    print(f"""
    file: {video_file.filename}
    fps: {video_file.fps}
    duration: {video_file.duration}
    size: {video_file.size}
    """)


def get_audio(path):
    video_file = VideoFileClip(path)

    return video_file.audio


def split_on_frames(path, name):

    os.chdir(path)

    if os.path.exists(name):

        os.mkdir('frames') if not os.path.exists(f"{path}\\frames") else None

        ffmpeg.input(name).output('frames/img%03d.png').run()


def frames_to_video(images_dir, name='test.mp4', fps=24):

    img = []

    for dir_path, dirs, files in os.walk(images_dir):
        for f in files:
            img.append(os.path.abspath(os.path.join(dir_path, f)))

    clips = [ImageClip(m).set_duration(2)
             for m in img]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(name, fps=fps)

