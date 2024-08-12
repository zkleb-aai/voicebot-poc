import warnings
from pydantic import ConfigDict

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
ConfigDict(protected_namespaces=())

from elevenlabs import VoiceSettings, play
from elevenlabs.client import ElevenLabs
import os

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API"),
)

def speak(msg):
    audio = client.text_to_speech.convert(
        voice_id="pMsXgVXv3BLzUgSXRplE",
        optimize_streaming_latency=0,
        output_format="mp3_22050_32",
        text=msg,
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )
    play(audio)