from translator import FixedTranslator
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from config import LANGUAGES
import os


def display_header():
    """Display header"""
    print("\n" + "=" * 70)
    print("🌍 COMPLETE TRANSLATION SYSTEM")
    print("   Text • Speech • Audio Translation")
    print("   Languages: English • Hindi • Gujarati • Marathi")
    print("=" * 70)


def display_languages():
    """Show languages"""
    print("\n🌐 Available Languages:")
    for key, lang in LANGUAGES.items():
        print(f"   {key}. {lang['name']} ({lang['display']})")


def text_to_text_mode(translator):
    """Text to Text translation"""
    print("\n" + "=" * 70)
    print("📝 MODE 1: DIRECT TEXT TRANSLATION")
    print("=" * 70)
    
    display_languages()
    
    source = input("\n📤 Select SOURCE language (1-4): ").strip()
    if source not in LANGUAGES:
        print("❌ Invalid choice!")
        return
    
    target = input("📥 Select TARGET language (1-4): ").strip()
    if target not in LANGUAGES or source == target:
        print("❌ Invalid choice or same language!")
        return
    
    source_lang = LANGUAGES[source]
    target_lang = LANGUAGES[target]
    
    print(f"\n✍️ Enter text in {source_lang['name']}:")
    text = input("> ")
    
    if not text.strip():
        print("❌ No text entered!")
        return
    
    print(f"\n⏳ Translating directly {source_lang['name']} -> {target_lang['name']}...")
    
    try:
        # Use simple codes: 'hi', 'mr', 'gu', 'en'
        translation = translator.translate(text, source_lang['code'], target_lang['code'])
        
        print("\n" + "=" * 70)
        print("✅ TRANSLATION RESULT")
        print("=" * 70)
        print(f"📤 Original ({source_lang['name']}): {text}")
        print(f"📥 Translated ({target_lang['name']}): {translation}")
        print("=" * 70)
        
        return translation
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def speech_to_text_mode(stt, translator):
    """
    Speech to Text with Translation capabilities
    Audio (Lang A) -> Text (Lang B)
    """
    print("\n" + "=" * 70)
    print("🎤 MODE 2: SPEECH TO TEXT & TRANSLATION")
    print("=" * 70)
    
    # 1. Get Audio File
    audio_file = input("\n📁 Enter audio file path (.wav, .mp3, .m4a): ").strip().strip('"\'')
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return
    
    display_languages()
    
    # 2. Select Source Language (What language is the audio in?)
    source = input("\n🗣️ Select AUDIO Source language (1-4): ").strip()
    if source not in LANGUAGES:
        print("❌ Invalid choice!")
        return
        
    # 3. Select Target Language (What language do you want the text in?)
    target = input("📝 Select TEXT Target language (1-4): ").strip()
    if target not in LANGUAGES:
        print("❌ Invalid choice!")
        return

    source_lang = LANGUAGES[source]
    target_lang = LANGUAGES[target]
    
    print(f"\n⏳ Transcribing {source_lang['name']} speech...")
    
    try:
        transcription = stt.transcribe(audio_file, source_lang['whisper_code'])
        
        final_text = transcription
        
        # Step B: Translate if languages are different
        if source != target:
            print(f"⏳ Translating to {target_lang['name']}...")
            
            # We use the standard 'code' ('hi', 'en', etc.) for the Translator
            translation = translator.translate(
                transcription, 
                source_lang['code'], 
                target_lang['code']
            )
            final_text = translation
        
        # 4. Display Result
        print("\n" + "=" * 70)
        print("✅ FINAL RESULT")
        print("=" * 70)
        print(f"🎤 Original Audio ({source_lang['name']}):")
        print(f"   {transcription}")
        print("-" * 70)
        print(f"📝 Final Text ({target_lang['name']}):")
        print(f"   {final_text}")
        print("=" * 70)
        
        return final_text
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
def text_to_speech_mode(tts, translator):
    """
    Text to Speech with Translation
    Text (Lang A) -> Text (Lang B) -> Audio (Lang B)
    """
    print("\n" + "=" * 70)
    print("🔊 MODE 3: TEXT TO SPEECH & TRANSLATION")
    print("=" * 70)
    
    display_languages()
    
    # 1. Select Source Language (What language are you writing in?)
    source = input("\n✍️ Select TEXT Source language (1-4): ").strip()
    if source not in LANGUAGES:
        print("❌ Invalid choice!")
        return

    # 2. Select Target Language (What language do you want to hear?)
    target = input("🗣️ Select AUDIO Target language (1-4): ").strip()
    if target not in LANGUAGES:
        print("❌ Invalid choice!")
        return
    
    source_lang = LANGUAGES[source]
    target_lang = LANGUAGES[target]
    
    # 3. Enter Text
    print(f"\n✍️ Enter text in {source_lang['name']}:")
    text = input("> ")
    
    if not text.strip():
        print("❌ No text entered!")
        return
    
    final_text = text
    
    try:
        # Step A: Translate (if languages are different)
        if source != target:
            print(f"\n⏳ Translating from {source_lang['name']} to {target_lang['name']}...")
            final_text = translator.translate(
                text, 
                source_lang['code'], 
                target_lang['code']
            )
            print(f"   ✅ Translated: {final_text}")
        
        # Step B: Generate Speech
        output_filename = f"output_{target_lang['name'].lower()}.mp3"
        print(f"\n⏳ Generating {target_lang['name']} speech...")
        
        # Note: We use the translated 'final_text' here
        output_path = tts.synthesize(final_text, target_lang['whisper_code'], output_filename)
        
        print("\n" + "=" * 70)
        print("✅ SPEECH GENERATED")
        print("=" * 70)
        print(f"📝 Original: {text}")
        print(f"📝 Translated: {final_text}")
        print(f"🔊 Audio File: {output_path}")
        print("=" * 70)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def speech_to_speech_mode(translator, stt, tts):
    """Complete Speech to Speech translation"""
    print("\n" + "=" * 70)
    print("🎙️ MODE 4: SPEECH TO SPEECH TRANSLATION")
    print("=" * 70)
    
    # Get audio file
    audio_file = input("\n📁 Enter audio file path: ").strip().strip('"\'')
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return
    
    display_languages()
    
    # Get source language
    source = input("\n📤 Select SOURCE language (audio language) (1-4): ").strip()
    if source not in LANGUAGES:
        print("❌ Invalid choice!")
        return
    
    # Get target language
    target = input("📥 Select TARGET language (output language) (1-4): ").strip()
    if target not in LANGUAGES:
        print("❌ Invalid choice!")
        return
    
    source_lang = LANGUAGES[source]
    target_lang = LANGUAGES[target]
    
    try:
        # Step 1: Speech to Text
        print(f"\n⏳ Step 1/3: Transcribing {source_lang['name']} speech...")
        transcription = stt.transcribe(audio_file, source_lang['whisper_code'])
        print(f"   ✅ Transcribed: {transcription}")
        
# Step 2: Translate (if different language)
        if source != target:
             print(f"\n⏳ Step 2/3: Translating to {target_lang['name']}...")
             translation = translator.translate(
                 transcription,
                 source_lang['code'],
                 target_lang['code']
             )
             print(f"   ✅ Translated: {translation}")
        else:
            translation = transcription
            print(f"\n⏳ Step 2/3: Same language, skipping translation...")
        
        # Step 3: Text to Speech
        print(f"\n⏳ Step 3/3: Generating {target_lang['name']} speech...")
        output_filename = f"translated_{target_lang['name'].lower()}.mp3"
        output_path = tts.synthesize(translation, target_lang['whisper_code'], output_filename)
        
        # Final result
        print("\n" + "=" * 70)
        print("✅ SPEECH-TO-SPEECH TRANSLATION COMPLETE")
        print("=" * 70)
        print(f"🎤 Original ({source_lang['name']}): {transcription}")
        print(f"📝 Translated ({target_lang['name']}): {translation}")
        print(f"🔊 Output Audio: {output_path}")
        print("=" * 70)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main program"""
    display_header()
    
    print("\n⏳ Initializing system...")
    
    # Initialize components (lazy loading)
    translator = None
    stt = None
    tts = None
    
    while True:
        print("\n" + "=" * 70)
        print("📋 MAIN MENU:")
        print("   1. Text to Text Translation")
        print("   2. Speech to Text (Audio → Text)")
        print("   3. Text to Speech (Text → Audio)")
        print("   4. Speech to Speech (Audio → Audio)")
        print("   5. Exit")
        print("=" * 70)
        
        choice = input("\nSelect mode (1-5): ").strip()
        
        if choice == '5':
            print("\n👋 Thank you! Goodbye!")
            break
        
        elif choice == '1':
            if translator is None:
                translator = FixedTranslator()
            text_to_text_mode(translator)
        
        elif choice == '2':
            if stt is None:
                stt = SpeechToText()   
            if translator is None:
                translator = FixedTranslator()   
            speech_to_text_mode(stt, translator)
            
        
        elif choice == '3':
            if tts is None:
                tts = TextToSpeech()
            if translator is None:
                translator = FixedTranslator()
            text_to_speech_mode(tts, translator)
        
        elif choice == '4':
            if translator is None:
                translator = FixedTranslator()
            if stt is None:
                stt = SpeechToText()
            if tts is None:
                tts = TextToSpeech()
            speech_to_speech_mode(translator, stt, tts)
        
        else:
            print("❌ Invalid choice!")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

