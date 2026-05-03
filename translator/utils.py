import os
from .config import LANGUAGES, OUTPUT_FOLDER


def display_header():
    print("\n" + "=" * 60)
    print("     LANGUAGE TRANSLATION SYSTEM")
    print("=" * 60)
    print()


def display_languages():
    print("\nSupported Languages:")
    for key, lang in LANGUAGES.items():
        print(f"{key}. {lang['name']}")
    print("5. Exit")
    print("-" * 60)


def get_language_choice(prompt):
    print(f"\n{prompt}")
    choice = input("Enter number (1-4): ")
    return choice


def validate_choice(choice):
    return choice in LANGUAGES or choice == '4'


def save_translation(text, translation, source_lang, target_lang):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    filename = f"{OUTPUT_FOLDER}/translation_{source_lang}_to_{target_lang}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("TRANSLATION OUTPUT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Source: {source_lang}\n")
        f.write(f"Target: {target_lang}\n\n")
        f.write("-" * 60 + "\n")
        f.write("ORIGINAL:\n")
        f.write(text + "\n\n")
        f.write("-" * 60 + "\n")
        f.write("TRANSLATED:\n")
        f.write(translation + "\n")
    
    return filename


def display_result(text, translation, source_lang, target_lang):
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"\nOriginal ({source_lang}):")
    print(text)
    print(f"\nTranslated ({target_lang}):")
    print(translation)
    print("=" * 60)