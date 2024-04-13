from utils.text_utils import dictionary_value_to_string
from utils.file_utils import create_unique_tmp_file, persist_binary_file_locally
from speech.transcoder.transcoder_service import convert_file_to_readable_mp3
from speech.stt.audio_transcription_service import convert_audio_to_text
from speech.tts.audio_generation_service import convert_text_to_audio
from rasa_service import rasa_response


def __get_transcoded_audio_file_path(audio: bytes) -> str:
    local_audio_file_path = persist_binary_file_locally(
        data=audio, file_suffix="user_audio.wav")
    local_output_file_path = create_unique_tmp_file(file_suffix="transcoded_user_audio.wav")
    convert_file_to_readable_mp3(
        local_input_file_path=local_audio_file_path,
        local_output_file_path=local_output_file_path)
    return local_output_file_path

async def handle_file_from_user(file: bytes) -> str:
    transcoded_user_audio_file_path = __get_transcoded_audio_file_path(audio=file)
    text_content = convert_audio_to_text(transcoded_user_audio_file_path)
    ai_text_reply = await rasa_response(text_content)
    ai_text_reply = dictionary_value_to_string(ai_text_reply["message"])
    generated_audio_ai_local_path = convert_text_to_audio(ai_text_reply, file_suffix="ai_audio_reply.wav")
    print("output_audio_local_path >>", generated_audio_ai_local_path)
    return generated_audio_ai_local_path
