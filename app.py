from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from transformers import pipeline
from dotenv import load_dotenv
import os
import assemblyai as aai

app = Flask(__name__)
load_dotenv()
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

@app.route('/voice', methods=['POST'])
def voice():
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/handle-input', method='POST')
    gather.say('Hello, how can I help you today? Please speak your request.')
    resp.append(gather)
    return str(resp)

@app.route('/handle-input', methods=['POST'])
def handle_input():
    transcript = request.values.get('SpeechResult', 'No speech detected').lower()
    resp = VoiceResponse()
    intent = 'agent'
    if 'buy' in transcript or 'purchase' in transcript:
        intent = 'sales'
        resp.say('Routing to sales queue.')
    elif 'help' in transcript or 'support' in transcript or 'issue' in transcript:
        intent = 'support'
        resp.say('Routing to support.')
    else:
        resp.say('Please hold for an agent.')
    print(f"Transcript: {transcript}, Intent: {intent}")  # Log to console
    return str(resp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)