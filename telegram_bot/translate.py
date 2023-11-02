import speech_recognition as sr
from deep_translator import GoogleTranslator


class SpeechToText:
    def __init__(self, audio_file):
        self.audio_file = audio_file 
        self.recognizer = sr.Recognizer()

            
    def recognize_speech(self):
        with sr.AudioFile(self.audio_file) as source: #  читаем содержимое файла
            audio_data = self.recognizer.record(source)

        try:
            text = self.recognizer.recognize_google(audio_data, language="ru")
            return text # Возвращаем распознанный текст
            
        except sr.UnknownValueError:
            print("Google не смог распознать текст")
            
        except sr.RequestError as e:
            print("Произошла ошибка подключения к google: {0}".format(e))
  
            
class WriteToFile:
    def __init__(self, text) -> None:
        self.text = text 
        
    def writing(self):
        with open("result.txt", "w", encoding="utf-8") as file:
            file.write(self.text)


class TranslateText:
    def __init__(self, text) -> None:
        self.text = text 
        
    def write_translated(self, target_language):
        translator = GoogleTranslator(source="auto", target=target_language)
        with open("translated.txt", "w", encoding="utf-8") as file:
            file.write(translator.translate(self.text))
        

def main(audio_file, target_language): 
    stt = SpeechToText(audio_file) #  создаем ЭК и передаем ему наш аудио файл
    recognized_speech = stt.recognize_speech()
    
    writer = WriteToFile(recognized_speech)
    writer.writing()
    
    text_translator = TranslateText(recognized_speech)
    text_translator.write_translated(target_language)
