# XTTS-RVC-UI

This is a simple UI that utilize's [Coqui's XTTSv2](https://github.com/coqui-ai/TTS) paired with RVC functionality to improve output quality.

# Prerequisites

- Requires MSVC - VC 2022 C++ x64/x86 build tools.

# Installation

Clone this repository:

`install.sh` does not yet work, but is being worked on.

If you want to try to install it anyways, here is a somewhat manual guide:

```
git clone https://github.com/MagicMari/XTTS-RVC-UI-API.git
pip install -r requirements.txt
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118
```

Then follow these guides, and issuie pages:
https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md
https://github.com/myshell-ai/MeloTTS/pull/124
https://github.com/myshell-ai/OpenVoice/blob/main/docs/USAGE.md#linux-install
https://github.com/vladmandic/automatic/discussions/540

# Usage

Run `start.bat` , `start.sh`

This will create the following folders within the project:

```
\models\xtts
\rvcs
\voices
```
- Relevant models will be downloaded into `\models`. This will be approximately ~2.27GB.
- You can manually add the desired XTTSv2 model files in `\models\xtts`.
- Place RVC models in `\rvcs`. Rename them as needed. If an **identically named** .index file exists in `\rvcs`, it will also be used.
- Place voice samples in `\voices`

