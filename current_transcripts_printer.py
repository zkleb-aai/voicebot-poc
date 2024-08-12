# current_transcripts_printer.py

import time
from threading import Event, Lock
from helpers.anthropic_helpers.messages import Messages
from helpers.anthropic_helpers.claude_chat import chat_with_claude
from helpers.elevenlabs_tts import speak
import json

class TranscriptPrinter:
    def __init__(self, transcript_array, stop_event: Event, system_prompt):
        self.transcript_array = transcript_array
        self.stop_event = stop_event
        self.last_message_timestamp = 0
        self.last_tts = 0
        self.processing_lock = Lock()
        self.messages = Messages()
        self.system_prompt = system_prompt

    def run(self):
        if not self.processing_lock.acquire(blocking=False):
            # If we can't acquire the lock, it means a message is still being processed
            return

        try:
            if self.transcript_array:
                # print(f"Current transcripts: {self.transcript_array}")
                if self.last_message_timestamp > self.last_tts:
                    new_message = " ".join(self.transcript_array)
                    self.transcript_array.clear()
                    new_response = self.claude_message(new_message)
                    print("Bot: " + new_response.text + "\n")
                    speak(new_response.text)
                    self.last_tts = time.time()
        finally:
            self.processing_lock.release()

    def claude_message(self, new_message):
        self.messages.add_message('user', new_message)
        resp = chat_with_claude(self.messages.get_messages(), self.system_prompt)
        self.messages.add_message(resp.role, resp.content)
        return resp.content[0]

    def get_messages_json(self):
        return self.messages.get_messages()