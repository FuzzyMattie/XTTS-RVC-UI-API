import numpy as np
import librosa
import soundfile as sf
import tensorflow as tf
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel
from nemo.collections.tts.models import Tacotron2Model
import torchaudio
from torchaudio import transforms
import torch
import nemo.collections.asr as nemo_asr

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained("titanet_large")
tts_model = FastPitchModel.from_pretrained("tts_en_fastpitch")
vocoder = HifiGanModel.from_pretrained(model_name="nvidia/tts_hifigan")

# Load reference audio
audio_path = "test2.wav"
audio, sr = torchaudio.load(audio_path)

# Ensure audio is of the right length (e.g., 3-5 seconds)
if audio.shape[1] > sr * 5:
    audio = audio[:, :sr * 5]

# Extract speaker embedding
with torch.no_grad():
    speaker_embedding = speaker_model.forward(input_signal=audio, input_signal_length=audio.shape[1])

# Define your input text
text = "This is an example of zero-shot voice cloning using NVIDIA NeMo."

# Parse the text into tokens
parsed = tts_model.parse(text)

# Generate the mel-spectrogram conditioned on the speaker embedding
with torch.no_grad():
    spectrogram = tts_model.generate_spectrogram(tokens=parsed, speaker_embeddings=torch.tensor(speaker_embedding).unsqueeze(0))

# Convert the mel-spectrogram to audio waveform using the vocoder
with torch.no_grad():
    audio_waveform = vocoder.convert_spectrogram_to_audio(spec=spectrogram)

# Save the audio file
torchaudio.save("cloned_voice_output.wav", np.ravel(audio_waveform.to("cpu").detach().numpy()), 22050)


