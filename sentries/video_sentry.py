from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import ffmpeg
import os


def print_video_info(path):
    """
    Выводит информацию о файле
    """
    video_file = VideoFileClip(path)

    print(f"""
    file: {video_file.filename}
    fps: {video_file.fps}
    duration: {video_file.duration}
    size: {video_file.size}
    """)


def get_audio(path):
    """
    Вырезает аудио из файла
    """
    video_file = VideoFileClip(path)

    return video_file.audio


def split_on_frames(file_path):
    """
    Разбивает видео на кадры
    """
    directory = os.path.dirname(file_path)

    if os.path.exists(file_path):

        os.mkdir(f'{directory}\\frames') if not os.path.exists(f'{directory}\\frames') else None

        ffmpeg.input(file_path).output(f'{directory}\\frames\\img%03d.png').run()


def frames_to_video(images_dir, name='test.mp4', framerate=24):
    """
    Собирает кадры в видео

    :param images_dir директория с кадрами.
    :param name название итогового файла (default test.mp4).
    :param framerate xастота кадров (default 24).
    """
    command = (
        f"ffmpeg -y -framerate {framerate} -i {images_dir}\\img%03d.png -c:v libx264 -pix_fmt yuv420p {name}"
    )

    os.system(command)

