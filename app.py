import time

from flask import Flask, render_template, request, jsonify, url_for
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

# CREDENTIALS
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client_file = os.getenv('GOOGLE_CREDENTIALS_PATH')
credentials = service_account.Credentials.from_service_account_file(client_file)
speech_client = speech.SpeechClient(credentials=credentials)

AUDIO_DIR = 'static/audio/'
MAX_AUDIO_FILES = 3


def cleanup_audio_files():
    # Obtém todos os arquivos de áudio no diretório
    audio_files = glob.glob(os.path.join(AUDIO_DIR, '*.mp3'))  # Altere a extensão conforme necessário
    audio_files.sort(key=os.path.getmtime)  # Ordena os arquivos pela data de modificação

    # Se o número de arquivos de áudio exceder o máximo permitido
    if len(audio_files) > MAX_AUDIO_FILES:
        # Deleta os arquivos mais antigos
        for file in audio_files[:len(audio_files) - MAX_AUDIO_FILES]:
            os.remove(file)  # Remove o arquivo
            print(f"Arquivo deletado: {file}")


# Função para capturar áudio do microfone e salvar como .wav temporário
def record_audio(filename="input_audio.wav", record_seconds=4):
    chunk = 1024  # Tamanho do bloco
    sample_format = pyaudio.paInt16  # Formato do áudio
    channels = 1  # Canal mono
    fs = 16000  # Taxa de amostragem em Hertz (16kHz)
    p = pyaudio.PyAudio()  # Inicializa o PyAudio

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    for _ in range(0, int(fs / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Parar e fechar o stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Salvar o áudio capturado em um arquivo WAV
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


# Função para enviar o áudio para o Google Cloud Speech API e realizar a transcrição
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="pt-BR",
        )

        response = speech_client.recognize(config=config, audio=audio)

        # Juntando todas as transcrições (se houver mais de uma)
        transcription = ' '.join([result.alternatives[0].transcript for result in response.results])
        return transcription

    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")
        return None


def get_chatgpt_response(transcription):
    if not transcription:
        print("Transcrição inválida. Verifique o arquivo de áudio.")
        return None

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": transcription}
        ],
        max_tokens=50
    )
    # Extrai o conteúdo da resposta corretamente
    response_content = response.choices[0].message.content
    return response_content


def speak(text):
    filename = f'static/audio/response_{int(time.time())}.mp3'  # Gera um nome de arquivo único
    try:
        tts = gTTS(text=text, lang='pt-br')
        tts.save(filename)  # Gera e salva o áudio
        print(f"Áudio salvo em: {filename}")
    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
    return filename


@app.route('/')
def chat():
    return render_template('chat.html')


@app.route('/send', methods=['POST'])
def send():
    record_audio(record_seconds=4)
    transcription = transcribe_audio('input_audio.wav')

    if transcription:
        chatgpt_response = get_chatgpt_response(transcription)
        print("Resposta do ChatGPT:", chatgpt_response)

        # Gera o áudio a partir da resposta
        audio_file = speak(chatgpt_response)  # Recebe o novo nome do arquivo de áudio
        cleanup_audio_files()

        return jsonify({
            "transcription": transcription,
            "chatgpt_response": chatgpt_response,
            "audio_file": url_for('static', filename='audio/' + audio_file.split('/')[-1])
        })
