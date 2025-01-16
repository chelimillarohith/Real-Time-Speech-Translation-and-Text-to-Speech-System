import tkinter as tk
from tkinter import messagebox
import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import os
import platform
import unicodedata
import sys

sys.stdout.reconfigure(encoding='utf-8')

def recognize_speech(recog, source):
    try:
        recog.adjust_for_ambient_noise(source, duration=0.2)
        audio = recog.listen(source)
        text = recog.recognize_google(audio)
        return text
    except Exception as e:
        print(e)
        return None

def process_speech():
    language_input = language_var.get()
    language_map = {
        'Hindi': 'hi',
        'Telugu': 'te',
        'Tamil': 'ta',
        'English': 'en',
    }
    if language_input not in language_map:
        messagebox.showerror("Invalid Language", "Please select a valid language.")
        return
    language_code = language_map[language_input]
    mc = spr.Microphone()
    with mc as source:
        Mytext = recognize_speech(recog1, source)
    
    if Mytext:
        spoken_label.config(text=f"Spoken Text: {Mytext}")
        translator = Translator()
        detected_language = translator.detect(Mytext).lang
        detected_language_label.config(text=f"Detected Language: {detected_language}")
        try:
            if not os.path.exists('outputs'):
                os.makedirs('outputs')
            translated = translator.translate(Mytext, src=detected_language, dest=language_code)
            translated_text = unicodedata.normalize('NFKD', translated.text)
            translated_label.config(text=f"Translated Text: {translated_text}")
            speak = gTTS(text=translated_text, lang=language_code, slow=False)
            audio_file = "outputs/translated_text.mp3"
            speak.save(audio_file)
            info_label.config(text="Playing translated speech...")
            os.system(f"start {audio_file}") 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during translation: {e}")
    else:
        spoken_label.config(text="Spoken Text: No speech input detected.")
        detected_language_label.config(text="Detected Language: N/A")
        translated_label.config(text="Translated Text: N/A")
        info_label.config(text="No speech input detected.")

root = tk.Tk()
root.title("Speech Translation System")
root.geometry("400x500")

instruction_label = tk.Label(root, text="Select target language and speak:")
instruction_label.pack(pady=20)

language_var = tk.StringVar()
language_var.set("English")
language_dropdown = tk.OptionMenu(root, language_var, 'Hindi', 'Telugu', 'Tamil', 'English')
language_dropdown.pack(pady=10)

process_button = tk.Button(root, text="Start Speech Recognition", command=process_speech)
process_button.pack(pady=20)

info_label = tk.Label(root, text="Results will be displayed here.", wraplength=350)
info_label.pack(pady=10)

spoken_label = tk.Label(root, text="Spoken Text: None", wraplength=350)
spoken_label.pack(pady=10)

detected_language_label = tk.Label(root, text="Detected Language: None", wraplength=350)
detected_language_label.pack(pady=10)

translated_label = tk.Label(root, text="Translated Text: None", wraplength=350)
translated_label.pack(pady=10)

recog1 = spr.Recognizer()

root.mainloop()
