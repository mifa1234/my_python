import vosk
import sys
import pyaudio
import os
import ast
from langchain_community.llms import Ollama

from gtts import gTTS
import pygame

def text_to_speech(text, language='ru'):
  """Преобразует текст в речь."""
  tts = gTTS(text=text, lang=language)
  tts.save("output.mp3")
  

#text_to_speech("проверка преобразования речи.", language='ru')
  
#pygame.mixer.init()
#pygame.mixer.music.load("output.mp3")
#pygame.mixer.music.play()

#while pygame.mixer.music.get_busy():
#  pass  

#pygame.mixer.quit()
  

llm = Ollama(model="gemma2:2b")
#llm = Ollama(model="llama3.1:8b")


# Проверка наличия модели
#if not os.path.exists("E:\\python_q\\ai_and_audio_text\\vosk-model-ru-0.42"):
if not os.path.exists("E:\\python_q\\ai_and_audio_text\\vosk-model-small-ru-0.22"):
    #print ("Пожалуйста, скачайте модель из https://alphacephei.com/vosk/models")
    sys.exit(1)

# Инициализация модели
#model = vosk.Model("E:\\python_q\\ai_and_audio_text\\vosk-model-ru-0.42")
model = vosk.Model("E:\\python_q\\ai_and_audio_text\\vosk-model-small-ru-0.22")
recognizer = vosk.KaldiRecognizer(model, 44100)

# Инициализация pyaudio
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True)
stream.start_stream()

print("Скажите что-нибудь...")

first_context = "это контекст  с предыдущего диалога. используй его для ответа. не используй смайлики. так же запомни что ты отвечаешь за Assistant, а я отвечаю за User. не используй эту часть для диалога. даже не упоминай про эту часть сообщения. а теперь диалог: "
dialog_context = str(" ")

# Основной цикл
while True:
    data = stream.read(16000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()        
        result =  ast.literal_eval(result)
        keys = list(result.keys())
        if "text" in keys:
            if len(result['text']) > 0:
                print('text: ', result['text'])
                ask_llm = first_context + '\n' + dialog_context + '\n' +result['text']
                llm_answer = llm.invoke(ask_llm)
                #llm_answer = llm(result['text'])
                print(llm_answer)
                
                dialog_context = dialog_context + "\n 'User:' " + result['text']
                dialog_context = dialog_context + "\n 'Assistant:' " + llm_answer
                
                if len(llm_answer) > 3 :
                    if len(llm_answer) > 240: llm_answer = llm_answer[0:239]
                    text_to_speech(llm_answer, language='ru')    
                    pygame.mixer.init()                
                    pygame.mixer.music.load("output.mp3")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                      pass 
                      
                    pygame.mixer.quit()  
                print('>next>')
                
    else:
        # Выводим промежуточный результат
        #result = recognizer.PartialResult()
        
        #result =  ast.literal_eval(result)
        #keys = list(result.keys())
        #if len(result[keys[0]]) > 0:
        #    print("partial: ",result[keys[0]])
        pass
