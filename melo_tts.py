from melo.api import TTS

def melo_init(pSpeed, pDevice, pLanguage):
    print("Using melo")
    global speed
    global model
    global speaker_ids
    speed = pSpeed #1.0
    device = pDevice #auto
    model = TTS(language=pLanguage, device=device)
    speaker_ids = model.hps.data.spk2id


#tts.tts_to_file(text=text, speaker_wav="./rvcs/"+ modelname + "/" + modelname + ".wav", language=language, file_path="./output.wav")
def tts_to_file(text, speaker_wav, language, file_path):
    print("generating melo")
    model.tts_to_file(text, speaker_ids['EN-US'], file_path, speed=speed)
