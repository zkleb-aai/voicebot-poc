# current_transcripts_printer.py

import time
from threading import Event, Lock
from helpers.anthropic_helpers.messages import Messages
from helpers.anthropic_helpers.claude_chat import chat_with_claude
from helpers.elevenlabs_tts import speak
import json
import base64

class TranscriptPrinter:
    def __init__(self, transcript_array, stop_event: Event, system_prompt, websocket):
        self.transcript_array = transcript_array
        self.stop_event = stop_event
        self.last_message_timestamp = 0
        self.last_tts = 0
        self.processing_lock = Lock()
        self.messages = Messages()
        self.system_prompt = system_prompt
        self.websocket = websocket
        self.stream_sid = None  # Initialize stream_sid as None

    def set_stream_sid(self, sid):
        self.stream_sid = sid

    def run(self):
        if not self.processing_lock.acquire(blocking=False):
            return

        try:
            if self.transcript_array:
                if self.last_message_timestamp > self.last_tts:
                    new_message = " ".join(self.transcript_array)
                    self.transcript_array.clear()
                    new_response = self.claude_message(new_message)
                    print("Bot: " + new_response.text + "\n")
                    audio_data = speak(new_response.text)
                    if self.stream_sid:  # Only send audio if we have a stream_sid
                        self.send_audio_over_websocket(audio_data)
                    else:
                        print("Warning: No stream_sid available. Audio not sent.")
                    self.last_tts = time.time()
        finally:
            self.processing_lock.release()

    def claude_message(self, new_message):
        self.messages.add_message('user', new_message)
        resp = chat_with_claude(self.messages.get_messages(), self.system_prompt)
        self.messages.add_message(resp.role, resp.content)
        return resp.content[0]

    def send_audio_over_websocket(self, audio_data):
        if not self.stream_sid:
            print("Error: No stream_sid available. Cannot send audio.")
            return

        encoded_audio = base64.b64encode(audio_data).decode('utf-8')

        # Prepare the media message
        media_message = {
            "event": "media",
            "streamSid": self.stream_sid,
            "media": {
                "payload": encoded_audio
            }
        }

        # Send the message over WebSocket
        self.websocket.send(json.dumps(media_message))