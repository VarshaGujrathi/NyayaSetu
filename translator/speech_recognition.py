from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import librosa


class SpeechRecognizer:
    """Speech-to-Text using Whisper"""
    
    def __init__(self):
        """Initialize Whisper model"""
        print("\n🎤 Loading Speech Recognition Model...")
        print("   Using: Whisper (OpenAI)")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-base")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
        self.model.to(self.device)
        
        print("   ✅ Speech Recognition Ready!\n")
    
    def transcribe_from_file(self, audio_file, language_code):
        """
        Transcribe audio file
        
        Args:
            audio_file: Path to audio file
            language_code: Language code (flores format)
        
        Returns:
            Transcribed text
        """
        # Map flores codes to whisper language codes
        lang_map = {
            'eng_Latn': 'english',
            'hin_Deva': 'hindi',
            'guj_Gujr': 'gujarati',
            'mar_Deva': 'marathi'
        }
        
        # Load audio
        audio_array, _ = librosa.load(audio_file, sr=16000)
        
        # Process audio
        inputs = self.processor(
            audio_array,
            sampling_rate=16000,
            return_tensors="pt"
        )
        inputs = inputs.input_features.to(self.device)
        
        # Generate transcription
        with torch.no_grad():
            predicted_ids = self.model.generate(
                inputs,
                language=lang_map.get(language_code, 'english')
            )
        
        # Decode
        transcription = self.processor.batch_decode(
            predicted_ids,
            skip_special_tokens=True
        )[0]
        
        return transcription
        