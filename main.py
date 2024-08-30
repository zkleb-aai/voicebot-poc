import base64
from flask import Flask, request, Response
from flask_sock import Sock
import ngrok
from twilio.rest import Client
import assemblyai as aai
import os
from threading import Thread, Event
import time
import json
from dotenv import load_dotenv
load_dotenv()

from current_transcripts_printer import TranscriptPrinter

aai.settings.api_key = os.environ.get('ASSEMBLY_API')

# CONFIG
global end_utterance_silence_threshold, system_prompt
end_utterance_silence_threshold = 1300
system_prompt = "You are a helpful customer service agent for a tech company who is brief in your responses. You are working at a call center so please respond how you would on a phonecall."

# Flask settings
PORT = 5002 # running on port 5002 by default
DEBUG = False
INCOMING_CALL_ROUTE = '/'
WEBSOCKET_ROUTE = '/realtime'

# Twilio authentication
account_sid = os.environ['TWILIO_ACCOUNT_SID']
api_key = os.environ['TWILIO_API_KEY_SID']
api_secret = os.environ['TWILIO_API_SECRET']
client = Client(api_key, api_secret, account_sid)

TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
TWILIO_SAMPLE_RATE = 8000 # Hz

ngrok.set_auth_token(os.getenv("NGROK_AUTHTOKEN"))
app = Flask(__name__)
sock = Sock(app)

@app.route(INCOMING_CALL_ROUTE, methods=['GET', 'POST'])
def receive_call():
    if request.method == 'POST':
        xml = f"""
<?xml version="1.0" encoding="UTF-8"?>
<Response>
   <Connect>
       <Stream url='wss://{request.host}{WEBSOCKET_ROUTE}' />
   </Connect>
   <Say>This TwiML instruction is unreachable unless the Stream is ended by your WebSocket server.</Say>
</Response>
""".strip()
        return Response(xml, mimetype='text/xml')
    else:
        return f"Real-time phone call transcription app"

def start_transcription(transcript_array, stop_event, printer):
    def on_open(session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)

    def on_data(transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print("User: "+ transcript.text +"\n")
            transcript_array.append(transcript.text)
            printer.last_message_timestamp = time.time()
            Thread(target=printer.run).start()
        else:
            print("Partial:", transcript.text, end="\r")

    def on_error(error: aai.RealtimeError):
        print("An error occurred:", error)

    def on_close():
        print("Closing Session")
        stop_event.set()

    transcriber = aai.RealtimeTranscriber(
        sample_rate=TWILIO_SAMPLE_RATE,
        on_data=on_data,
        on_error=on_error,
        on_open=on_open,
        on_close=on_close,
        encoding=aai.AudioEncoding.pcm_mulaw,
        end_utterance_silence_threshold=end_utterance_silence_threshold
    )

    return transcriber

@sock.route(WEBSOCKET_ROUTE)
def transcription_websocket(ws):
    transcript_array = []
    stop_event = Event()
    printer = TranscriptPrinter(transcript_array, stop_event, system_prompt, ws)
    transcriber = start_transcription(transcript_array, stop_event, printer)

    while True:
        data = json.loads(ws.receive())
        match data['event']:
            case "connected":
                transcriber.connect()
                print('transcriber connected')
            case "start":
                print('twilio started')
                printer.set_stream_sid(data['start']['streamSid'])  # Set the stream_sid here
            case "media":
                payload_b64 = data['media']['payload']
                payload_mulaw = base64.b64decode(payload_b64)
                transcriber.stream(payload_mulaw)
            case "stop":
                print('twilio stopped')
                transcriber.close()
                print('transcriber closed')
                break

def main():
    try:
        listener = ngrok.forward(f"http://localhost:{PORT}")
        print(f"Ngrok tunnel opened at {listener.url()} for port {PORT}")
        NGROK_URL = listener.url()

        twilio_numbers = client.incoming_phone_numbers.list()
        twilio_number_sid = [num.sid for num in twilio_numbers if num.phone_number == TWILIO_NUMBER][0]
        client.incoming_phone_numbers(twilio_number_sid).update(voice_url=f"{NGROK_URL}{INCOMING_CALL_ROUTE}")

        app.run(port=PORT, debug=DEBUG)

    finally:
        ngrok.disconnect()

if __name__ == "__main__":
    main()