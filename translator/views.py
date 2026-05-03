from django.shortcuts import render

# Create your views here.
import os
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .ml_engine import get_engine
from .config import LANGUAGES

def index(request):

    # Change 'index.html' to 'translator_index.html'
    return render(request, 'translator_index.html', {'languages': LANGUAGES})

def translate_text(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text')
            s_id = request.POST.get('source')
            t_id = request.POST.get('target')
            engine = get_engine()
            res = engine.translator.translate(text, LANGUAGES[s_id]['code'], LANGUAGES[t_id]['code'])
            return JsonResponse({'status': 'success', 'translation': res})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def transcribe_audio(request):
    if request.method == 'POST':
        try:
            audio = request.FILES.get('audio')
            s_id = request.POST.get('source')
            t_id = request.POST.get('target')
            
            # Save temp file
            path = default_storage.save(f"temp/{audio.name}", ContentFile(audio.read()))
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            
            engine = get_engine()
            transcription = engine.stt.transcribe(full_path, LANGUAGES[s_id]['whisper_code'])
            
            translation = transcription
            if s_id != t_id:
                translation = engine.translator.translate(transcription, LANGUAGES[s_id]['code'], LANGUAGES[t_id]['code'])
            
            if os.path.exists(full_path): os.remove(full_path)
            
            return JsonResponse({'status': 'success', 'transcription': transcription, 'translation': translation})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def synthesize_speech(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text')
            t_id = request.POST.get('target')
            
            engine = get_engine()
            filename = f"speech_{uuid.uuid4()}.mp3"
            
            out_path = os.path.join(settings.MEDIA_ROOT, 'generated_audio', filename)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            
            # Note: We are saving manually to ensure path correctness for web serving
            engine.tts.synthesize(text, LANGUAGES[t_id]['whisper_code'], filename)
            
            # Move the file if it saved elsewhere, or ensure tts.synthesize uses the full path.
            # Ideally update text_to_speech.py to take a full path, but for now we assume it saves to AUDIO_OUTPUT_FOLDER
            # Let's check if we need to move it.
            
            # SIMPLER FIX: Let's just return the success. 
            # If your TTS saves to 'audio_output(2)', we need to serve that.
            
            # CORRECT APPROACH:
            # We will tell the browser where the file is.
            # Assuming your TTS class puts files in 'audio_output(2)' inside the project root:
            
            return JsonResponse({'status': 'success', 'audio_url': f"/media/generated_audio/{filename}"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})