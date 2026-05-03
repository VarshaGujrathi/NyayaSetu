from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import os
from .config import LANGUAGE_CODE_MAPPINGS


class SpeechToText:
    """Speech recognition using OpenAI Whisper"""
    
    def __init__(self):
        """Initialize Whisper model"""
        print("\n" + "=" * 70)
        print("🎤 Loading Speech-to-Text Model (Whisper)")
        print("=" * 70)
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Device: {self.device}")
        print("   Loading...")
        
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
        self.model.to(self.device)
        
        print("   ✅ Speech-to-Text model loaded!\n")
    
    def _convert_language_code(self, lang_code):
        """
        Convert from frontend language code to Whisper format
        E.g., 'hi' -> 'hindi', 'en' -> 'english'
        """
        whisper_map = LANGUAGE_CODE_MAPPINGS.get("whisper", {})
        return whisper_map.get(lang_code, lang_code)
    
    def transcribe(self, audio_file, language_code):
        """
        Transcribe audio file to text
        
        Args:
            audio_file: Path to audio file (.wav, .mp3, .m4a)
            language_code: Language code (en, hi, gu, mr, etc.)
        
        Returns:
            Transcribed text
        """
        import librosa
        
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Load audio
        print(f"   Loading audio file...")
        audio_array, sample_rate = librosa.load(audio_file, sr=16000)
        
        # Process audio
        print(f"   Transcribing {language_code} speech...")
        inputs = self.processor(
            audio_array,
            sampling_rate=16000,
            return_tensors="pt"
        )
        inputs = inputs.input_features.to(self.device)
        
        # Convert language code to Whisper format
        whisper_lang = self._convert_language_code(language_code)
        
        # Generate transcription
        with torch.no_grad():
            predicted_ids = self.model.generate(
                inputs,
                language=whisper_lang,
                task="transcribe"
            )
        
        # Decode
        transcription = self.processor.batch_decode(
            predicted_ids,
            skip_special_tokens=True
        )[0]
        
        return transcription.strip()