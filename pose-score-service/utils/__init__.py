from moviepy.editor import VideoFileClip
from config import videos_directory
import os

def convert_to_mp4(input_filename):
    input_video_path = os.path.join(videos_directory, input_filename)
    converted_video_output_path = os.path.join(videos_directory, input_filename + "_converted.mp4")
    clip = VideoFileClip(input_video_path)
    clip.write_videofile(converted_video_output_path, codec='libx264')
    return converted_video_output_path

def annotated_filename(filename):
    file_type = filename.split('.')[-1]
    filename_without_type = filename.rsplit('.', 1)[0]
    annotated_video_filename = filename_without_type + '_annotated.' + file_type
    return annotated_video_filename