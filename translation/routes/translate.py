from flask import Blueprint, request, render_template
import os

# import services
from services.audio_extractor import extract_audio
from services.speech_to_text import speech_to_text
from services.translator import translate_text
from services.text_to_speech import text_to_audio
from services.merger import merge_audio_video

translate_bp = Blueprint('translate', __name__)

# folders
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "output/final_videos"

# create folders safely
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@translate_bp.route('/translate', methods=['POST'])
def translate_video():
    try:
        # 1. Get file and language
        file = request.files['video']
        lang = request.form['language']

        # 2. Fix filename (remove spaces)
        filename = file.filename.replace(" ", "_")

        # 3. Save video
        video_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(video_path)

        # 4. Extract audio
        audio_path = extract_audio(video_path)

        # 5. Speech → Text
        text = speech_to_text(audio_path)

        # 6. Translate text
        translated_text = translate_text(text, lang)

        # 7. Text → Speech
        translated_audio = text_to_audio(translated_text)

        # 8. Merge audio + video
        output_filename = "final_" + filename
        output_video = os.path.join(OUTPUT_FOLDER, output_filename)
        merge_audio_video(video_path, translated_audio, output_video)

        # 9. Convert path for browser
        video_filename = os.path.basename(output_video)
        video_url = f"/output/{video_filename}"

        # 10. Show result page with video
        return render_template("result.html", video_path=video_url)

    except Exception as e:
        return f"Error: {str(e)}"
    