# AOV Rebuild Pipeline Master Suite
A production-oriented Nuke Python plugin for automated cross-renderer AOV reconstruction and built-in quality validation.

## Features
- Auto-detects 5 render engines: Arnold / Redshift / V-Ray / Karma / UE5
- Two rebuild modes: Basic (fast additive) / Advanced (raw×filter, direct/indirect split)
- Built-in 2-tier QC: layer completeness check + pixel-level difference audit
- Dual language UI: English / 中文
- Clean structured node graph layout
- Supports Nuke 14.0 ~ 17.x | Python 3

## Installation
### Windows / Mac
1. Download the `AOV_Rebuild_Pipeline` folder
2. Open your Nuke user config directory:
   - Windows: `C:/Users/Your_name/.nuke/`
   - Mac: `~/.nuke/`
3. Edit or create `menu.py` in that folder, add this line:
    ```python
    nuke.pluginAddPath("/your_path/AOV_Rebuild_Pipeline")
