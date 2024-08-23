#!/bin/sh
conda create -n combotts python=3.10.9
conda activate combotts

git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip install -e .
python -m unidic download
cd ../

git clone git@github.com:myshell-ai/OpenVoice.git
cd OpenVoice
pip install -e .
cd ../

conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit
python3 -m pip install nvidia-cudnn-cu11==8.9.2.26
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/:$CUDNN_PATH/lib' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

pip install -r requirements.txt
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118

wget -O checkpoints.zip https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip
wget -O checkpoints_v2.zip https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip

unzip checkpoints.zip -d ./OpenVoice
unzip checkpoints_v2.zip -d ./OpenVoice

