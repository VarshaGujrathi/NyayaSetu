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
        self._translator = None
        self._stt = None
        self._tts = None

    @property
    def translator(self):
        if self._translator is None:
            self._translator = FixedTranslator()
        return self._translator

    @property
    def stt(self):
        if self._stt is None:
            self._stt = SpeechToText()
        return self._stt

    @property
    def tts(self):
        if self._tts is None:
            self._tts = TextToSpeech()
        return self._tts
    
    
def get_engine():
    return MLEngine.get_instance()