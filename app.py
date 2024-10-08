from flask import Flask
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
from openai import OpenAI
import pyaudio
import wave
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Inicialize o cliente OpenAI e Flask
app = Flask(__name__)

# Carregue suas credenciais de serviço
client_file = os.getenv('GOOGLE_CREDENTIALS_PATH')
credentials = service_account.Credentials.from_service_account_file(client_file)
speech_client = speech.SpeechClient(credentials=credentials)

# Função para capturar áudio do microfone e salvar como .wav temporário
def record_audio(filename="input_audio.wav", record_seconds=5):
    chunk = 1024  # Tamanho do bloco
    sample_format = pyaudio.paInt16  # Formato do áudio
    channels = 1  # Canal mono
    fs = 16000  # Taxa de amostragem em Hertz (16kHz)
    p = pyaudio.PyAudio()  # Inicializa o PyAudio

    print("Gravando...")

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

    print("Gravação finalizada!")

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

    try:
        # Faz a chamada para obter a resposta
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": transcription}
            ],
            max_tokens=50  # Ajuste conforme necessário
        )
        # Extrai o conteúdo da resposta corretamente
        response_content = response.choices[0].message.content
        return response_content
    except Exception as e:
        print(f"Erro ao obter resposta do ChatGPT: {e}")
        return None



# Exemplo de uso
# Capturar áudio do microfone (aqui por 5 segundos)
record_audio(record_seconds=5)

# Transcrever o áudio gravado
transcription = transcribe_audio('input_audio.wav')
print(f"Transcrição obtida: {transcription}")

# Obter a resposta do ChatGPT com a transcrição
chatgpt_response = get_chatgpt_response(transcription)
print("Resposta do ChatGPT:", chatgpt_response)