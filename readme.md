# VoiceBot

VoiceBot is an interactive voice-based assistant that uses speech recognition, natural language processing, and text-to-speech technologies to engage in conversation with users.

## Features

- Real-time speech-to-text transcription using AssemblyAI
- Natural language processing and conversation handling with Anthropic's Claude AI
- Text-to-speech output using ElevenLabs

## Prerequisites

- Python 3.10 or higher
- An AssemblyAI API key
- An Anthropic API key
- An ElevenLabs API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/voicebot.git
   cd voicebot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   ASSEMBLY_API=your_assemblyai_api_key
   ANTHROPIC_KEY=your_anthropic_api_key
   ELEVENLABS_API=your_elevenlabs_api_key
   ```

## Usage

Run the main script to start the VoiceBot:

```
python main.py
```

You can optionally set a custom system prompt for Claude:

```
python main.py --system-prompt "You are a helpful assistant specializing in technology."
```

## Important Note

**Please wear headphones when using VoiceBot!** 

The bot's responses are played out loud through your device's speakers. If you're not wearing headphones, your microphone may pick up these responses, potentially causing feedback loops or confusion in the conversation. Using headphones ensures a clear separation between your voice input and the bot's audio output.

## How It Works

1. **Speech Recognition**: The `main.py` script uses AssemblyAI to perform real-time speech-to-text transcription of your voice input.

2. **Conversation Handling**: The transcribed text is sent to Claude AI (via the `current_transcripts_printer.py` module) for processing and generating appropriate responses.

3. **Text-to-Speech**: Claude's text responses are converted to speech using ElevenLabs' text-to-speech API (in the `elevenlabs_tts.py` module) and played back to you.

## File Structure

- `main.py`: The main script that coordinates speech recognition and manages the conversation flow.
- `current_transcripts_printer.py`: Handles interaction with Claude AI and manages the conversation state.
- `elevenlabs_tts.py`: Converts text responses to speech using ElevenLabs.
- `helpers/`: Contains additional utility scripts and API wrappers.

## Customization

You can customize the bot's behavior by modifying the system prompt in `main.py`. This sets the context for Claude AI, determining how it should behave and respond.

## Troubleshooting

If you encounter any issues with Pydantic warnings, they can be suppressed by adding the following code at the beginning of the relevant scripts:

```python
import warnings
from pydantic import ConfigDict

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
ConfigDict(protected_namespaces=())
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.