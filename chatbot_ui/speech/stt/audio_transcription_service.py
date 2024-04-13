import speech_recognition as sr

def convert_audio_to_text(local_input_file_path: str) -> str:
    #Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(local_input_file_path) as audio_file:
        audio_data = recognizer.record(audio_file)
    try:
        # Perform speech recognition on the audio file
        text = recognizer.recognize_google(audio_data)
        return text

    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)
    