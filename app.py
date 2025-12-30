from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "call_log.txt"

def log_call(transcript, intent):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] Transcript: {transcript} | Intent: {intent}\n")

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
    
    intent = 'agent'  # default
    
    if any(word in transcript for word in ['buy', 'purchase', 'order', 'shop', 'product']):
        intent = 'sales'
        resp.say('Routing to sales queue.')
    elif any(word in transcript for word in ['help', 'support', 'issue', 'problem', 'broken', 'not working']):
        intent = 'support'
        resp.say('Routing to support.')
    elif any(word in transcript for word in ['bill', 'invoice', 'payment', 'charge', 'billing']):
        intent = 'billing'
        resp.say('Routing to billing department.')
    elif any(word in transcript for word in ['track', 'tracking', 'delivery', 'ship', 'where is my order']):
        intent = 'tracking'
        resp.say('Routing to order tracking.')
    else:
        resp.say('Please hold for an agent.')
    
    resp.say("Thank you for calling. Have a great day!")
    
    # Log to console and file
    print(f"Transcript: {transcript}, Intent: {intent}")
    log_call(transcript.capitalize(), intent)
    
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)