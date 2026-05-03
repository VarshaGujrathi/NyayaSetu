# Configuration for ML modules
from django.conf import settings
import os

OUTPUT_FOLDER = os.path.join(settings.MEDIA_ROOT, "translations")
AUDIO_OUTPUT_FOLDER = os.path.join(settings.MEDIA_ROOT, "generated_audio")

# Language code mappings for different systems
LANGUAGE_CODE_MAPPINGS = {
    # Frontend format (used in UI) -> M2M100 format (for translation)
    "m2m100": {
        "en": "en",
        "hi": "hi",
        "mr": "mr",
        "gu": "gu",
        "bn": "bn",
        "ta": "ta",
        "te": "te",
        "kn": "kn",
        "pa": "pa",
        "ml": "ml"
    },
    # Frontend format -> gTTS format (same)
    "gtts": {
        "en": "en",
        "hi": "hi",
        "mr": "mr",
        "gu": "gu",
        "bn": "bn",
        "ta": "ta",
        "te": "te",
        "kn": "kn",
        "pa": "pa",
        "ml": "ml"
    },
    # Frontend format -> Whisper format
    "whisper": {
        "en": "english",
        "hi": "hindi",
        "mr": "marathi",
        "gu": "gujarati",
        "bn": "bengali",
        "ta": "tamil",
        "te": "telugu",
        "kn": "kannada",
        "pa": "punjabi",
        "ml": "malayalam"
    }
}
