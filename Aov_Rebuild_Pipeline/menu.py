# -*- coding: utf-8 -*-
import nuke
import os

def __trigger_untouched_core():
    current_dir = os.path.dirname(__file__)
    core_script_path = os.path.join(current_dir, "aov_core_script.py")
    
    if os.path.exists(core_script_path):
        with open(core_script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            

            context = {}
            context.update(globals())
            context.update(locals())
            
            exec(script_content, context)
    else:
        nuke.message(f"[Pipeline Error]\ncan't find file:\n{core_script_path}")

main_menu = nuke.menu("Nuke")
pipeline_menu = main_menu.addMenu("Pipeline")

pipeline_menu.addCommand(
    "AOV Rebuild Master Suite", 
    "__trigger_untouched_core()", 
    "alt+shift+r"
)