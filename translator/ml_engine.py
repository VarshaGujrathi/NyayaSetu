from .translator import FixedTranslator
from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech

class MLEngine:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print("⏳ Initializing ML Engine Singleton...")
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.translator = FixedTranslator()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        print("✅ ML Engine Ready")

def get_engine():
    return MLEngine.get_instance()