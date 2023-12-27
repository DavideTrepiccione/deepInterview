import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from openai import *
import properties as p 

api_key = p.API_KEY
client = Client(api_key=p.API_KEY)

# Assumi che le funzioni transcribe e chat2 siano già definite
# e che le credenziali API siano gestite in modo appropriato

class ChatThread(QThread):
    update_output_signal = pyqtSignal(str)
    update_messages_signal = pyqtSignal(str)

    def __init__(self,idCount,messages):
        self.messages = messages
        self.idCount=idCount
        QThread.__init__(self)

    def run(self):      
        print("ChatThread.run start")        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=self.messages,            
            stream = True
        )
        
        chunk_message =""
        for chunk in response:
            if chunk is not None and chunk.choices[0] is not None and chunk.choices[0].delta is not None and chunk.choices[0].delta.content is not None:
                chunk_message += chunk.choices[0].delta.content
                self.update_output_signal.emit(chunk_message+" §"+str(self.idCount))
        print("ChatThread.run start")
        self.update_messages_signal.emit(chunk_message+" §"+str(self.idCount))

    