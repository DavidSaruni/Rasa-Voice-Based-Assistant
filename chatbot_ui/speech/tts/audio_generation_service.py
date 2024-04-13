import pyttsx3
from utils.file_utils import create_unique_tmp_file


def convert_text_to_audio(text_content: str, file_suffix: str):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set properties (optional)
    engine.setProperty("rate", 150)  # Speed percent (can go over 100)
    engine.setProperty("volume", 0.9)  # Volume 0-1

    # Queue up the text to be spoken
    #engine.say(text_content)

    # Generate audio from text
    output_audio_local_path = create_unique_tmp_file(file_suffix=file_suffix)
    engine.save_to_file(text_content, output_audio_local_path)
    
    # Process the queued text and generate the audio
    engine.runAndWait()
    return output_audio_local_path