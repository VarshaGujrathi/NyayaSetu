import os
from .config import AUDIO_OUTPUT_FOLDER, LANGUAGE_CODE_MAPPINGS

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
    
    def synthesize(self, text, language_code, output_path):
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert
            language_code: Language code (en, hi, gu, mr, etc.)
            output_path: Full output path (e.g., '/path/to/audio_abc123.mp3')
        
        Returns:
            Path to saved audio file
        """
        if self.gTTS is None:
            raise ImportError("gTTS is not installed. Install with: pip install gtts")
        
        # Create output folder if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Map language codes to gTTS format
        lang_map = LANGUAGE_CODE_MAPPINGS.get("gtts", {})
        lang = lang_map.get(language_code, 'en')
        
        print(f"   Generating {lang} speech...")
        
        # Generate speech
        tts = self.gTTS(text=text, lang=lang, slow=False)
        
        # Save audio file
        tts.save(output_path)
        
        print(f"   ✅ Audio saved: {output_path}")
        
        return output_path