# Chatbot with OpenAI and Google Cloud Speech

This repository contains a chatbot built using the OpenAI API, with integrated audio processing and speech recognition
via the Google Cloud Speech API. It allows users to capture audio, transcribe it into text, and then generate automatic
responses.

## Demo

Watch the demonstration of the Chatbot here:

[![Watch the Demo](https://img.youtube.com/vi/q2_NwTfCx24/0.jpg)](https://www.youtube.com/watch?v=q2_NwTfCx24)

### Features:

#### Audio Capture:

- Records audio from the microphone in real-time and saves it as a .wav file.

#### Speech Transcription:

- Uses Google Cloud Speech API to transcribe the recorded audio into text.

#### ChatGPT Interaction:

- Sends the transcription to OpenAI's GPT-3.5 model and returns a response based on the provided content.

#### GPT Response to Audio

- Converts the GPT-generated responses into speech using Google Text-to-Speech (gTTS), allowing users to hear the
  chatbot’s reply.

####                                                              * Flask Integration

#### Libraries:

- **openai**
- **google-cloud-speech**

#### Credential Requirements:

- OpenAI API Key
- Google Cloud Speech credentials (JSON file)

### AJAX for Real-Time Chat

In this project, AJAX is used to create a seamless real-time chat experience. The chat is updated dynamically as
messages are exchanged between the user and the bot, without requiring the page to reload.

## TODO  as improvements:

### • DB Implementations

Consider adding a database to store user conversations for
tracking history, user progress, and analytics. Storing interactions could enable personalized responses and suggestions
based on previous chats.

### • Improving Performance with Celery (Optional)

To boost performance, especially when handling multiple requests, you can use **Celery** for background jobs.

- Handling API calls in the background to improve responsiveness
- Enhancing scalability
- Increasing **response speed**.
- Combined with AJAX, it offers a smoother user experience by providing real-time updates.

## Instalation

1. Clone this repository:

``` bash
git clone https://github.com/your-username/chatbot-openai.git
```

2. Install the dependencies:

```bash
pip
install - r
requirements.txt
```

3. Set up credentials:

- Add your OpenAI API Key in the .env file:

``` bash
OPENAI_API_KEY=your_openai_api_key
```

- Download the Google Cloud service account **JSON file** for Speech-to-Text API access, and
  export its path as an environment variable

```bash
GOOGLE_CREDENTIALS_PATH=path/to/your-google-credentials.json
```
