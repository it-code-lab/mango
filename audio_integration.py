from gtts import gTTS

def generate_audio(text, language='en'):
    """Generate audio from text using Google Text-to-Speech."""
    tts = gTTS(text=text, lang=language)
    filename = "output_audio.mp3"
    tts.save(filename)
    return filename