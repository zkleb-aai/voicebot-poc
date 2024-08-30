# import warnings
# from pydantic import ConfigDict

# warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
# ConfigDict(protected_namespaces=())

# from elevenlabs import VoiceSettings, play
# from elevenlabs.client import ElevenLabs
# import os

# client = ElevenLabs(
#     api_key=os.getenv("ELEVENLABS_API"),
# )

# def speak(msg):
#     audio = client.text_to_speech.convert(
#         voice_id="pMsXgVXv3BLzUgSXRplE",
#         optimize_streaming_latency=0,
#         output_format="mp3_22050_32",
#         text=msg,
#         voice_settings=VoiceSettings(
#             stability=0.1,
#             similarity_boost=0.3,
#             style=0.2,
#         ),
#     )
#     play(audio)

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
    # play(audio)
    # below for saving
    import random, string
    # Function to generate a random filename
    def generate_random_filename(length=5, extension=".mp3"):
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return random_string + extension

    # Ensure the 'audios' directory exists
    os.makedirs('audios', exist_ok=True)

    # Save the audio to the 'audios' directory
    # file_path = os.path.join('audios', generate_random_filename())
    # with open(file_path, 'wb') as f:
    #     for chunk in audio:
    #         f.write(chunk)

    # Play the audio
    play(audio)

    # print(f"Audio saved to {file_path}")