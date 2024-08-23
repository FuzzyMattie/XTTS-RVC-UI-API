#!/bin/sh
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

pip install torch==2.2.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118

pip install transformers==4.33.0
pip install librosa==0.10.0

git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip install -e .
python -m unidic download
