import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QSizePolicy,QPushButton
from PyQt5.QtCore import  pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from ChatThread import ChatThread
from RecorderThread import RecordingThread
from TranscriberThread import TranscribeThread
import properties as p 



class MyApp(QWidget):
    stop_recording_signal = pyqtSignal()
    messages = []
    count = 0
    recording = False
    
    def __init__(self):
        
        super().__init__()
        self.setup_ui()
        

    def setUpRecordingThread(self):

        self.thread = RecordingThread()
        self.stop_recording_signal.connect( self.thread.stopRecording)
        return self.thread
    
    def setUpChatThread(self,transcription):
        self.count+=1
        self.messages.append({"role": "user","content": p.SYSTEM_PROMPT_INTERVIEW+transcription})
        self.thread = ChatThread(self.count,self.messages)
        self.thread.update_output_signal.connect(self.update_output)
        self.thread.update_messages_signal.connect(self.update_messages)
        return  self.thread
    def setUpTrascribeThread(self):

        self.thread = TranscribeThread()
        self.thread.transcriptionSignal.connect(self.startChat)
        return  self.thread

    def setup_ui(self):
        # Creazione dei widget di output
        self.log = QTextEdit()
        self.log.setStyleSheet("border: 1px solid red; background-color: white;")
        self.startStopButton = QPushButton("Start Recording")
        self.startStopButton.clicked.connect(self.toggle_recording)

        self.output = QWebEngineView()
        self.output.setStyleSheet("border: 1px solid black; background-color: black;")
        
        
        self.log.setMinimumWidth(200)  # Imposta una larghezza minima
        self.output.setMinimumWidth(200)

        self.log.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.output.setHtml(p.HTML_TEMPLATE)
        self.toggleLogButton = QPushButton("Toggle Log")

        # Layout orizzontale
        hbox = QHBoxLayout()
        hbox.addWidget(self.startStopButton)
        hbox.addWidget(self.toggleLogButton)
        hbox.addWidget(self.log)
        hbox.addWidget(self.output)
        

        self.setLayout(hbox)
        self.setGeometry(300, 300, 900, 600)  # Imposta dimensioni e posizione della finestra
        self.setWindowTitle('My Application')
        

   

   
        
    def toggle_recording(self):
        if not self.recording:
            self.thread = self.setUpRecordingThread()
            self.thread.start()
            self.startStopButton.setText("Stop Recording")
            self.recording = True
        else:
            self.startStopButton.setText("Play Recording")
            self.stop_recording_signal.emit()
            self.thread.wait()
            self.recording = False
            self.thread = self.setUpTrascribeThread()
            self.thread.start()

    def startChat(self,transcription):
        self.update_input(transcription)
        self.thread.wait()
        self.thread = self.setUpChatThread(transcription)

        self.thread.start()
      

    def update_input(self, new_text):
        message_class ="received"
        message_html = f'<div class="message {message_class}">{self.escapedText(new_text)}</div>'
        self.output.page().runJavaScript(f"document.getElementById('chat-container').innerHTML += '{message_html}';")
    
    def update_output(self, new_text):
        id = new_text.split("§")[1]
        new_text = self.escapedText(new_text.split("§")[0])
        message_class = "sent"
        message_html = f'<div id ="{id}" class="message {message_class}">{new_text}</div>'
        script = """
            var messageDiv = document.getElementById('"""+id+"""');
            if (messageDiv)
                messageDiv.parentNode.removeChild(messageDiv)
            document.getElementById('chat-container').innerHTML += '"""+message_html+"""'
            """
        self.output.page().runJavaScript(script)
    def escapedText(self,new_text): return new_text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t").replace("`", "\\`")

    def update_messages(self, message):
        self.messages.append({"role": "assistant","content": message})
# Creazione dell'applicazione Qt
app = QApplication(sys.argv)

# Creazione e visualizzazione dell'interfaccia
interface = MyApp()
interface.show()

# Esecuzione dell'applicazione
sys.exit(app.exec_())
