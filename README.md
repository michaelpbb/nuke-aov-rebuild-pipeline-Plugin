# AOV Rebuild Pipeline Master Suite
A production-oriented Nuke Python plugin for automated cross-renderer AOV reconstruction and built-in quality validation.

## Features
- Auto-detects 5 render engines: Arnold / Redshift / V-Ray / Karma / UE5
- Two rebuild modes: Basic (fast additive) / Advanced (raw×filter, direct/indirect split)
- Built-in 2-tier QC: layer completeness check + pixel-level difference audit
- Dual language UI: English / 中文
<img width="264" height="144" alt="language" src="https://github.com/user-attachments/assets/910ef967-38f3-4a4a-bec8-eabbe0f6424b" />

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
<img width="369" height="182" alt="rebuild mode" src="https://github.com/user-attachments/assets/ee016aa1-e6e8-41a7-8326-52829ff15c61" />

   - Choose **Renderer**: Auto Detect or manually select
<img width="367" height="213" alt="renderer" src="https://github.com/user-attachments/assets/52752a8d-3ec6-4106-a76c-f8db42bce9df" />

   - Toggle **Run Quality Control** to enable QC audit
<img width="369" height="182" alt="qc2" src="https://github.com/user-attachments/assets/45aca7f7-f4dc-46ee-8504-8bb466785ffe" />

4. Click OK. The full reconstruction node graph will be generated automatically.

##  QC Audit System
The built-in quality control runs two checks automatically:
1. **Layer Completeness Check** – verifies all required layers for the current mode are present in the EXR
2. **Pixel-level Difference Check** – creates a Difference node to compare rebuilt output with original beauty
<img width="1013" height="903" alt="difference node" src="https://github.com/user-attachments/assets/2514af0e-17fa-43a3-811b-c87c3b08a60a" />


It generates a full text report with missing layer list and extraction status.
<img width="619" height="393" alt="qcok 1" src="https://github.com/user-attachments/assets/0fd440e9-6c2d-48a8-88ab-1682a7d16321" />


##  License
MIT License – feel free to use and modify in production, just keep the original copyright notice.

##  Author
Developed by Michael Pu 

