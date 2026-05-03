import os
import uuid
from django.conf import settings
from main.ml_engine import get_engine

def translate_text_pipeline(text, target_lang):
    engine = get_engine()

    # source_lang = "en"  # assume English input (safe for your use case)

    source_lang = "en"  # keep
    target_lang = target_lang  # keep

    try:
        if source_lang != target_lang:
            return engine.translator.translate(
                text,
                source_lang,   # keep simple
                target_lang    # keep simple
            )
        print("DEBUG LANG:", source_lang, target_lang)    
        return text

    except Exception as e:
        print("DEBUG LANG:", source_lang, target_lang)
        print("Translation Error:", e)
        return text  # fallback instead of crash


def text_to_speech_pipeline(text, lang_code):
    engine = get_engine()

    filename = f"audio_{uuid.uuid4()}.mp3"
    output_path = os.path.join(settings.MEDIA_ROOT, "generated_audio", filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    engine.tts.synthesize(text, lang_code, output_path)

    return f"/media/generated_audio/{filename}"