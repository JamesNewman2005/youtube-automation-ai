import edge_tts
import os

class AudioSynthesizer:
    def __init__(self) -> None:
        self.voice = "en-US-ChristopherNeural"

    async def convert_text_to_voice(self, script: str, output_filename: str) -> None:
        try:
            communicate = edge_tts.Communicate(script, self.voice)
            
            audio_filename = output_filename.replace('.txt', '.mp3')
            output_path = os.path.join('output/audio', audio_filename)
            
            await communicate.save(output_path)
            
        except Exception as e:
            print(f"Error during audio synthesis: {e}")
            return None