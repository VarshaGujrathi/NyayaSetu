import os
from .config import AUDIO_OUTPUT_FOLDER

class TextToSpeech:
    """Text-to-Speech using Google Text-to-Speech (gTTS)"""
    
    def __init__(self):
        """Initialize TTS"""
        print("\n" + "=" * 70)
        print("🔊 Loading Text-to-Speech System (gTTS)")
        print("=" * 70)
        
        try:
            from gtts import gTTS
            self.gTTS = gTTS
            print("   ✅ Text-to-Speech ready!\n")
        except ImportError:
            print("   ⚠️ gTTS not installed!")
            print("   Install with: pip install gtts")
            self.gTTS = None
    
    def synthesize(self, text, language_code, output_filename):
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert
            language_code: Language code (en, hi, gu, mr)
            output_filename: Output filename (e.g., 'output.mp3')
        
        Returns:
            Path to saved audio file
        """
        if self.gTTS is None:
            raise ImportError("gTTS is not installed. Install with: pip install gtts")
        
        # Create output folder
        if not os.path.exists(AUDIO_OUTPUT_FOLDER):
            os.makedirs(AUDIO_OUTPUT_FOLDER)
        
        # Map language codes
        lang_map = {
            'en': 'en',
            'hi': 'hi',
            'gu': 'gu',
            'mr': 'mr'
        }
        
        lang = lang_map.get(language_code, 'en')
        
        print(f"   Generating {lang} speech...")
        
        # Generate speech
        tts = self.gTTS(text=text, lang=lang, slow=False)
        
        # Save audio file
        output_path = os.path.join(AUDIO_OUTPUT_FOLDER, output_filename)
        tts.save(output_path)
        
        print(f"   ✅ Audio saved: {output_path}")
        
        return output_path