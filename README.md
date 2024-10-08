# chatbot-openai
This repository contains a chatbot built using the OpenAI API, with integrated audio processing and speech recognition via the Google Cloud Speech API. It allows users to capture audio, transcribe it into text, and then generate automatic responses.

### Features:

#### Audio Capture:
Records audio from the microphone in real-time and saves it as a .wav file.
#### Speech Transcription: 
Uses Google Cloud Speech API to transcribe the recorded audio into text.
#### ChatGPT Interaction: 
Sends the transcription to OpenAI's GPT-3.5 model and returns a response based on the provided content.
#### * Flask Integration

#### Libraries:
openai
google-cloud-speech
pyaudio
Flask

#### Credentials:
OpenAI API Key
Google Cloud Speech credentials (JSON file)
