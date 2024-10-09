from flask import Flask, render_template, jsonify, url_for
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
from openai import OpenAI
from gtts import gTTS
import pyaudio
import wave
import os
import time
import glob

load_dotenv()
app = Flask(__name__)

# Credentials
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
credentials = service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_CREDENTIALS_PATH'))
speech_client = speech.SpeechClient(credentials=credentials)

AUDIO_DIR = 'static/audio/'
MAX_AUDIO_FILES = 3


# Clean old sound files
def cleanup_audio_files():
    audio_files = sorted(glob.glob(os.path.join(AUDIO_DIR, '*.mp3')), key=os.path.getmtime)

    if len(audio_files) > MAX_AUDIO_FILES:
        for file in audio_files[:len(audio_files) - MAX_AUDIO_FILES]:
            os.remove(file)
            print(f"Arquivo deletado: {file}")


# Record audio and save as a WAV file
def record_audio(filename="input_audio.wav", record_seconds=5):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, frames_per_buffer=1024, input=True)

    frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * record_seconds))]

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))


# Transcribe audio using Google Cloud Speech API
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = speech_client.recognize(config=config, audio=audio)
    transcription = ' '.join([result.alternatives[0].transcript for result in response.results])

    return transcription


# Get ChatGPT answer
def get_chatgpt_response(transcription):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": transcription}],
        max_tokens=100
    )
    return response.choices[0].message.content


# Generate audio with gTTS
def speak(text):
    filename = f'static/audio/response_{int(time.time())}.mp3'
    gTTS(text=text, lang='en').save(filename)
    print(f"Audio saved as: {filename}")
    return filename


# Root route
@app.route('/')
def chat():
    return render_template('chat.html')


# Process send audio and answers from GPT
@app.route('/send', methods=['POST'])
def send():
    record_audio(record_seconds=5)
    transcription = transcribe_audio('input_audio.wav')

    if transcription:
        chatgpt_response = get_chatgpt_response(transcription)
        print("ChatGPT answer:", chatgpt_response)

        audio_file = speak(chatgpt_response)
        cleanup_audio_files()

        return jsonify({
            "transcription": transcription,
            "chatgpt_response": chatgpt_response,
            "audio_file": url_for('static', filename='audio/' + os.path.basename(audio_file))
        })


if __name__ == '__main__':
    app.run(debug=True)
