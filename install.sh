#!/bin/sh
pip install bitarray
pip install hydra-core
pip install omegaconf
pip install sacrebleu>=1.4.12
pip install cffi
pip install cython
pip install torchaudio>=0.8.0
pip install faiss_cpu==1.7.4
pip install gradio==4.7.1
pip install librosa==0.10.0
pip install numpy==1.22.0
pip install praat-parselmouth
pip install pyworld==0.3.4
pip install Requests==2.31.0
pip install scipy==1.11.4
pip install torch==2.2.0
pip install torchcrepe==0.0.22
pip install TTS==0.21.1
pip install botocore>=1.34.98
pip install cached_path>=1.6.2
pip install --no-deps fairseq==0.12.2

pip install torch==2.2.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118

conda install conda-forge::mecab-python3

git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip install -e .
python -m unidic download
cd ../

git clone https://github.com/myshell-ai/OpenVoice.git
cd OpenVoice
pip install -e .
cd ../

conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit
python3 -m pip install nvidia-cudnn-cu11==8.9.2.26
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/:$CUDNN_PATH/lib' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

wget -O checkpoints.zip https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip
wget -O checkpoints_v2.zip https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip

unzip checkpoints.zip -d ./OpenVoice
unzip checkpoints_v2.zip -d ./OpenVoice

