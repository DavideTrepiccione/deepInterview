
from PyQt5.QtCore import QThread, pyqtSignal

# Assumi che le funzioni transcribe e chat2 siano già definite
# e che le credenziali API siano gestite in modo appropriato

class RecordingThread(QThread):
    update_log_signal = pyqtSignal(str)
    update_input_signal = pyqtSignal(str)
    update_output_signal = pyqtSignal(str)
    currentIndex=0
    isStarted=True
    messages=[]

    def __init__(self,currentIndex):
        self.currentIndex=currentIndex
        QThread.__init__(self)
    def run(self):
        self.record_audio()
        

    def record_audio(self,output_filename="prova.wav", chunk_size=1024):
        print("RecordingThread.record_audio start")
        import soundcard as sc
        import soundfile as sf
        source = sc.default_speaker()
        if self.currentIndex == 1:
            source =sc.default_microphone()
        try:
            data =[]
            self.update_log_signal.emit("Inizia la registrazione...")
            SAMPLE_RATE = 48000
            with sc.get_microphone(id=str(sc.default_speaker()), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                    while self.isStarted:
                        block = mic.record(numframes=int(SAMPLE_RATE*1))
                        data.extend(block)
            sf.write(file=output_filename, data=data, samplerate=SAMPLE_RATE)
        except Exception as e:
            print(e)
        print("RecordingThread.record_audio finish")
        return output_filename
  
    def stopRecording(self):
        self.isStarted = False


    