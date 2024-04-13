import io
import requests
from gtts import gTTS
from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from speech.audio_service import handle_file_from_user
from pydantic import BaseModel
from rasa_service import rasa_response
import audioread
from io import BytesIO
from fastapi.responses import StreamingResponse
import speech_recognition as sr
import subprocess

import sys
print(sys.executable)

app = FastAPI()

# Initialize templates for rendering HTML
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_audio_format(file_content):
    # Check the format of the audio file
    with audioread.audio_open(file_content) as f:
        format_name = f.format_name.lower()
    return format_name


class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    # Load and render the HTML content from the index.html file
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chatbot_response")
async def chatbot_response(message: Message):
    message = message.message
    output_message = await rasa_response(message)
    print("output_message >>", output_message["message"])
    return output_message["message"]

# @app.post("/audio_message")
# async def handle_receive_audio_data(audio_file:UploadFile):
#     file_data = await audio_file.read()
#     generated_ai_audio_file_path = await handle_file_from_user(file=file_data)
#     return FileResponse(generated_ai_audio_file_path, media_type="audio/wav", filename="ai_output")

@app.post("/audio_message")
async def handle_audio_message():

    bot_message = ""
    message=""


    # Initialize recognizer
    r = sr.Recognizer()

    try:
        # Process audio
        with sr.Microphone() as source:
            print("Speak Anything:")
            audio = r.listen(source, timeout=5)  # Adjust timeout as needed

        # Convert audio to text
        message = r.recognize_google(audio)
        print("You said : {}".format(message))

        # Send the text message to Rasa
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})

        # Convert Rasa response to speech
        print("Bot says, ", end="")
        for i in response.json():
            bot_message = i.get('text', '')
            print(f"{bot_message}")

        if bot_message:
            # Create audio file from bot message
            tts = gTTS(text=bot_message)
            audio_bytes_io = io.BytesIO()
            tts.write_to_fp(audio_bytes_io)
            audio_bytes_io.seek(0)

            # Save audio file to a directory
            audio_path = "audio_files/response.mp3"
            with open(audio_path, "wb") as f:
                f.write(audio_bytes_io.read())

            # Play the audio file

            return FileResponse(audio_path, media_type="audio/mp3")

    except sr.WaitTimeoutError:
        return {"message": "No speech detected. Please try again."}

    except sr.UnknownValueError:
        return {"message": "Sorry, could not recognize your voice."}

    except sr.RequestError as e:
        return {"message": f"Could not request results from Google Speech Recognition service: {e}"}