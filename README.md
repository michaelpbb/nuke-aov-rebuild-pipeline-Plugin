# AOV Rebuild Pipeline Master Suite
A production-oriented Nuke Python plugin for automated cross-renderer AOV reconstruction and built-in quality validation.

## Features
- Auto-detects 5 render engines: Arnold / Redshift / V-Ray / Karma / UE5
- Two rebuild modes: Basic (fast additive) / Advanced (raw×filter, direct/indirect split)
- Built-in 2-tier QC: layer completeness check + pixel-level difference audit
- Dual language UI: English / 中文
- Clean, structured auto-generated node graph
- Native depth and motion vector utility pass setup

##  Compatibility
| Category | Support |
| --- | --- |
| Nuke Version | 14.0 ~ 17.x |
| Python | Python 3 |
| Render Engines | Arnold, Redshift, V-Ray, Karma, UE5 |
| OS | Windows, macOS |

##  Installation
1. Download the `AOV_Rebuild_Pipeline` folder from the latest release.
2. Open your Nuke user config directory:
   - Windows: `C:\Users\YourName\.nuke\`
   - macOS: `/Users/YourName/.nuke/`
3. Edit (or create) the `menu.py` file in that folder, add this line at the end:
    ```python
    nuke.pluginAddPath("/your_path/AOV_Rebuild_Pipeline")

##  Usage
1. Select a Read node loaded with EXR AOV footage in your Node Graph.
2. Launch the plugin from the Nuke menu.
3. In the panel:
   - Choose **Rebuild Mode**: Basic / Advanced
   - Choose **Renderer**: Auto Detect or manually select
   - Toggle **Run Quality Control** to enable QC audit
4. Click OK. The full reconstruction node graph will be generated automatically.

##  QC Audit System
The built-in quality control runs two checks automatically:
1. **Layer Completeness Check** – verifies all required layers for the current mode are present in the EXR
2. **Pixel-level Difference Check** – creates a Difference node to compare rebuilt output with original beauty

It generates a full text report with missing layer list and extraction status.

##  License
MIT License – feel free to use and modify in production, just keep the original copyright notice.

##  Author
Developed by Michael Pu 

