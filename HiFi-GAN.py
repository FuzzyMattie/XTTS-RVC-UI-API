import numpy as np
import librosa
import soundfile as sf
import tensorflow as tf
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel

# Load the FastPitch model (if needed)
# spec_generator = FastPitchModel.from_pretrained("nvidia/tts_en_fastpitch")

# Load the HifiGan vocoder model
model = HifiGanModel.from_pretrained("nvidia/tts_hifigan")

# Load the audio file
my_audio_as_np_array, my_sample_rate = librosa.load("test2.wav", sr=22050)  # Ensure sample rate is 22050

# Compute the mel-spectrogram
spec = librosa.feature.melspectrogram(
    y=my_audio_as_np_array,
    sr=my_sample_rate,
    n_fft=2048,
    hop_length=512,
    win_length=None,
    window='hann',
    center=True,
    pad_mode='reflect',
    power=2.0,
    n_mels=128
)

# Add batch dimension
spec_with_batch = np.expand_dims(spec, axis=0)

# Convert to TensorFlow tensor
tensor_spec = tf.convert_to_tensor(spec_with_batch, dtype=tf.float32)

# Convert the mel-spectrogram to audio using the HifiGan model
# Note: HifiGan expects spectrogram to be on GPU, ensure to move tensor to GPU if needed
spec_with_batch = tf.convert_to_tensor(spec_with_batch, dtype=tf.float32)  # Move tensor to GPU if required
audio = model.convert_spectrogram_to_audio(spec=spec_with_batch)

# Save the audio to disk
sf.write("speech.wav", audio.numpy().flatten(), my_sample_rate)  # Flatten and save
