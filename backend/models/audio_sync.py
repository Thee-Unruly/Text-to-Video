import torch
from TTS.api import TTS

# laod coqui TTS model
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to("cuda")

def generate_audio(text):
    tts.tts_to_file(text=text, file_path = "output.wav")
    return "output.wav"                
                    
# Free & Open-source
# Works fully offline
# Supports multiple languages