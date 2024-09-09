# XTTS-RVC-UI

This is a simple UI that utilize's [Coqui's XTTSv2](https://github.com/coqui-ai/TTS) paired with RVC functionality to improve output quality.

# Prerequisites

- Requires MSVC - VC 2022 C++ x64/x86 build tools.

# Installation

Clone this repository:

```
git clone https://github.com/MagicMari/XTTS-RVC-UI-API.git
```

Then follow the instructions in the `install_guide.txt`.


# Usage

Run `python main.py`.

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

