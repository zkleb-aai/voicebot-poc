# main.py

import assemblyai as aai
import dotenv
import os
from threading import Thread, Event
import time
from current_transcripts_printer import TranscriptPrinter
import json

dotenv.load_dotenv()

aai.settings.api_key = os.environ.get('ASSEMBLY_API')

# CONFIG
global end_utterance_silence_threshold, system_prompt
end_utterance_silence_threshold = 700 # set custom end of utterance silence threshold. default is 700 ms
# set custom system prompt 
system_prompt = "You are a helpful customer service agent for a tech company who is brief in your responses.  You are working at a call center so please respond how you would on a phonecall."

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
        sample_rate=16_000,
        on_data=on_data,
        on_error=on_error,
        on_open=on_open,
        on_close=on_close,
        end_utterance_silence_threshold=end_utterance_silence_threshold
    )

    return transcriber

def main():
    transcript_array = []
    stop_event = Event()

    # Create the transcript printer with the system prompt
    printer = TranscriptPrinter(transcript_array, stop_event, system_prompt)

    # Start the transcription
    transcriber = start_transcription(transcript_array, stop_event, printer)

    # Run transcription in the main thread
    transcriber.connect()
    microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)

    try:
        transcriber.stream(microphone_stream)
    except KeyboardInterrupt:
        print("Stopping transcription...")
    finally:
        stop_event.set()
        transcriber.close()

    # Return messages as JSON string
    print("Messages Data:")
    print(printer.get_messages_json())

if __name__ == "__main__":
    main()