import speech_recognition as spr
from googletrans import Translator 
from gtts import gTTS
import os

recog1 = spr.Recognizer()
mc=spr.Microphone()

def recognize_speech(recog,source):
  try:
    recog.adjust_for_ambient_noise(source,duration=0.2)
    audio=recog.listen(source)
    text=recog.recognize_google(audio)
    return text
  except spr.UnknownValueError:
    print("could understand your audio")
    return None
  except spr.RequestError as e:
    print("could not request results;{0}",format(e))
    return None
  
language_input=input("Enter the Language you want to translate to: ")
language_map={
    'Hindi':'hi',
    'Telugu':'te',
    'Tamil':'ta',
    'English':'en',
}
if language_input not in language_map:
  print("enter valid language which is there in the list")
else:
  language_code=language_map[language_input]
  mc = spr.Microphone()
  with mc as source:
    print("Speak now...")
    Mytext = recognize_speech(recog1, source)
  if Mytext:
    print(f"Recognized Text: {Mytext}")
    translator=Translator()
    detected_language=translator.detect(Mytext).lang
    print(f"Detected Language: {detected_language}")
    try:
      if not os.path.exists('outputs'):
        os.makedirs('outputs')
      translated=translator.translate(Mytext,src=detected_language,dest=language_code)
      if not translated:
        print("Translation failed")
      else:
        translated_text=translated.text
        print(f"Translated Text: {translated_text}")
        speak=gTTS(text=translated_text,lang=language_code,slow=False)
        audio_file="outputs/translated_text.mp3"
        speak.save(audio_file)
        print("Playing translated speech...")
        os.system(f"start {audio_file}")
    except Exception as e:
      print("an error occured during translation:{e}")
  else:
    print("no speech input detected")
      
