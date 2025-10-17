from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route('/voice', methods=['POST'])
def voice():
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/handle-input', method='POST')
    gather.say('Hello, how can I help you today? Please speak your request.')
    resp.append(gather)
    return str(resp)

@app.route('/handle-input', methods=['POST'])
def handle_input():
    resp = VoiceResponse()
    transcript = request.values.get('SpeechResult', 'No speech detected')
    resp.say(f'You said: {transcript}. Processing your request.')
    return str(resp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)