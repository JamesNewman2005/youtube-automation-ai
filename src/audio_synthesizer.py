import edge_tts
import os

class AudioSynthesizer:
    def __init__(self) -> None:
        self.voice = "en-US-ChristopherNeural"

        os.makedirs('output/audio', exist_ok=True)

    async def convert_text_to_voice(self, script: str, output_filename: str) -> None:
        try:
            filename = output_filename.replace('.txt', '')
            if ' ' in filename:
                filename = filename.replace(' ', '_')
            elif '-' in filename:
                filename = filename.replace('-', '_')
            elif '/' in filename:
                filename = filename.replace('/', '_')
            
            audio_filename = f"{filename}.mp3"
            output_path = os.path.join('output/audio', audio_filename)
            
            communicate = edge_tts.Communicate(script, self.voice)
            await communicate.save(output_path)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error during audio synthesis: {e}")