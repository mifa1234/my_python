  
import speech_recognition as sr

def choose_microphone():
  """Функция для выбора микрофона из доступных."""

  mic_list = sr.Microphone.list_microphone_names()
  print("Доступные микрофоны:")
  for i, mic_name in enumerate(mic_list):
    try:
        mic_name_utf8 = mic_name.encode('cp1251').decode('utf-8') # Предполагаем, что исходная кодировка cp1251
    except UnicodeDecodeError:
        mic_name_utf8 = mic_name  # Если преобразование не удалось
    
    print(f"{i}: {mic_name_utf8}")

  while True:
    try:
      choice = int(input("Выберите номер микрофона: "))
      if 0 <= choice < len(mic_list):
        return sr.Microphone(device_index=choice)
      else:
        print("Неверный номер. Пожалуйста, выберите из списка.")
    except ValueError:
      print("Пожалуйста, введите число.")

def recognize_speech(microphone):
  """Функция для распознавания речи с микрофона."""

  recognizer = sr.Recognizer()
  with microphone as source:
    print("Говорите...")
    audio = recognizer.listen(source)

  try:
    text = recognizer.recognize_google(audio, language='ru-RU') # Распознавание на русском языке
    print(f"Вы сказали: {text}")
  except sr.UnknownValueError:
    print("Google Speech Recognition не смог понять речь.")
  except sr.RequestError as e:
    print(f"Не удалось запросить результаты от Google Speech Recognition; {e}")

if __name__ == "__main__":
  microphone = choose_microphone()
  while True:
    recognize_speech(microphone)        