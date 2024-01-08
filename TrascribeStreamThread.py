
from google.cloud import speech

client = speech.SpeechClient()

def stream_microphone():
    SAMPLE_RATE = 48000
    buffer = []
    import soundcard as sc
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        while True:
            block = mic.record(numframes=int(SAMPLE_RATE*1))
            buffer.append(block.tobytes())

            if len(buffer) >= 96000:  # Define some buffer limit
                responses = transcribe(buffer)
                for response in responses:
                    if not response.results:
                        continue

                    result = response.results[0]
                    print(result)
                    if result.is_final:
                        print(result)
                        buffer.clear()

def transcribe( audio_data):
    audio = speech.RecognitionAudio(content=b''.join(audio_data))
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)
    return response.results

stream_microphone()