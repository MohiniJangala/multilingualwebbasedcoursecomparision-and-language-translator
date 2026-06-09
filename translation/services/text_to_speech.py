from gtts import gTTS

def text_to_audio(text):
    output_audio = "static/uploads/translated_audio.mp3"
    tts = gTTS(text=text)
    tts.save(output_audio)
    return output_audio
