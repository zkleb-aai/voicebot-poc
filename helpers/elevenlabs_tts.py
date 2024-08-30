import warnings
from pydantic import ConfigDict

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
ConfigDict(protected_namespaces=())

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import os
import io
from pydub import AudioSegment

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API"),
)


def speak(msg):
    audio = client.text_to_speech.convert(
        model_id="eleven_turbo_v2_5", # fastest model
        voice_id="pMsXgVXv3BLzUgSXRplE",
        optimize_streaming_latency=0,
        output_format="mp3_44100_128",  # We'll convert this to μ-law
        text=msg,
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )

    # Convert the audio to bytes
    audio_bytes = b''.join(audio)

    # Load the audio into pydub
    audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
    
    # Convert to 8000 Hz, mono, PCM mu-law
    audio_segment = audio_segment.set_frame_rate(8000).set_channels(1).set_sample_width(1)
    
    # Export the audio to mu-law format in memory
    buffer = io.BytesIO()
    audio_segment.export(buffer, format="wav", codec="pcm_mulaw")
    
    return buffer.getvalue()