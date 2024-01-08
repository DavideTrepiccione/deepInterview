from PyQt5.QtCore import QThread, pyqtSignal
from openai import *
from properties import p 

api_key = p["API_KEY"]
client = Client(api_key=api_key)

# Assumi che le funzioni transcribe e chat2 siano già definite
# e che le credenziali API siano gestite in modo appropriato

class TranscribeThread(QThread):
    transcriptionSignal = pyqtSignal(str)
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print("TranscribeThread.run start")
        transcription=""
        try:
            transcription = self.transcribe()
            self.transcriptionSignal.emit(transcription)
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
        print("TranscribeThread.run start",transcription)

    def transcribe(self,audio_file_path="prova.wav"):
        # Assumi che il file audio sia un file .mp3 o un formato supportato
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return response

 