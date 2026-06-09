from moviepy.editor import VideoFileClip

def extract_audio(video_path):
    audio_path = "temp_audio.wav"
    
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()
    
    return audio_path

