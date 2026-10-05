# ==============================================================================
#  [Pipeline Suite] AOV Rebuild Pipeline Master Suite - Strict Mode & Pure UI
# ==============================================================================
import nuke

# ====================== 语言包 / Language Pack ======================
lang_pack = {
    "zh": {
        "ui_lang_title": "语言选择",
        "ui_lang_msg": "请选择面板语言：",
        
        # Panel 界面
        "panel_title": "AOV 重构管线主控",
        "mode_label": "重构模式:",
        "mode_opts": "{基础标准 (Basic)} {进阶模式 (Advanced)}",
        "engine_label": "渲染引擎:",
        "engine_opts": "{自动识别} 'Arnold' 'Redshift' 'V-Ray' 'Karma' 'UE5'",
        "qc_label": "运行质量检测 (QC_mode)",
        
        # 错误提示
        "err_invalid_read": "请选择一个有效的Read节点！",
        "err_no_selection": "未选中任何节点，请先选择Read节点。",
        
        # 控制台日志
        "log_locked_renderer": "[管线信息] 已锁定渲染引擎：[{engine}]",
        "log_qc_start": "[QC管线] 正在创建差值对比节点...",
        "log_success": "[管线成功] 完成！完整管线搭建完毕，共 {count} 个分支。",
        
        # QC 报告文本
        "report_title": "【AOV重构QC审计报告】",
        "standard_warn_title": "⚠️ 【EXR层缺失警告】当前模式配方不完整",
        "current_renderer": "当前渲染器：",
        "standard_count": "该模式需 {total} 层核心 | 已包含 {present} 层 | 缺失 {missing} 层",
        "standard_missing_list": "EXR文件中缺少以下必须成分：",
        "standard_note": "说明：由于EXR缺失当前模式所需的层，重构画面将无法完美还原，Difference节点可见残余误差。",
        "standard_ok_title": "✅ 【EXR层完整】当前模式配方齐全",
        "standard_ok_desc": "所需 {total} 层核心成分均已包含<br>理论上重构画面可100%还原原图。",
        
        "extract_error_title": "❌ 【节点提取异常】存在已识别但未生成的层",
        "extract_count": "应提取 {expected} 个，实提取 {actual} 个",
        "extract_missing_list": "共缺失 {count} 个层的Shuffle节点：",
        "extract_ok_title": "✅ 【节点提取正常】所有识别层均已生成",
        "extract_ok_desc": "应提取 {expected} 个，实提取 {actual} 个",
        
        "footer_info": "当前运行模式：{mode} | 渲染引擎：{engine}<br><br><font color='#777777' size='3'>开发者：Michael Pu | 版本号：v1.2.2 Pipeline_Release</font>"
    },
    "en": {
        "ui_lang_title": "Language Selection",
        "ui_lang_msg": "Please select UI language:",
        
        # Panel UI
        "panel_title": "AOV Rebuild Pipeline Master Suite",
        "mode_label": "Rebuild Mode:",
        "mode_opts": "{Basic Standard} {Advanced}",
        "engine_label": "Renderer Engine:",
        "engine_opts": "{Auto Detect} 'Arnold' 'Redshift' 'V-Ray' 'Karma' 'UE5'",
        "qc_label": "Run Quality Control (QC_mode)",
        
        # Error messages
        "err_invalid_read": "Please select an effective Read node!",
        "err_no_selection": "No node has been selected. Please select the Read node first.",
        
        # Console logs
        "log_locked_renderer": "[Pipeline Info] Locked Renderer Engine: [{engine}]",
        "log_qc_start": "[QC Pipeline] Creating Difference check node...",
        "log_success": "[Pipeline Success] Finished! Fully robust pipeline setup complete: {count} branches.",
        
        # QC Report text
        "report_title": "【AOV Rebuild QC Audit Report】",
        "standard_warn_title": "⚠️ 【EXR Layer Warning】Incomplete Recipe for Current Mode",
        "current_renderer": "Renderer: ",
        "standard_count": "Required in this mode: {total} | Present: {present} | Missing: {missing}",
        "standard_missing_list": "Missing essential components in EXR:",
        "standard_note": "Note: Missing these layers will cause a delta between the rebuilt image and the original Beauty.",
        "standard_ok_title": "✅ 【EXR Layers Complete】Recipe is Full",
        "standard_ok_desc": "All {total} required components are present.<br>The rebuilt image can theoretically match the original 100%.",
        
        "extract_error_title": "❌ 【Node Extraction Error】Identified layers not generated",
        "extract_count": "Expected: {expected} | Actually generated: {actual}",
        "extract_missing_list": "Missing Shuffle nodes for {count} layers:",
        "extract_ok_title": "✅ 【Node Extraction OK】All layers extracted",
        "extract_ok_desc": "Expected: {expected} | Actually generated: {actual}",
        
       "footer_info": "Running Mode: {mode} | Render Engine: {engine}<br><br><font color='#777777' size='3'>Developer: Michael Pu | Version: v1.2.2 Pipeline_Release</font>"
    }
}


def create_isolated_node(node_class):
    original_selection = nuke.selectedNodes()
    for node in original_selection: 
        node['selected'].setValue(False)
    new_node = nuke.createNode(node_class, inpanel=False)
    node_name = new_node.name()
    confirmed_node = nuke.toNode(node_name)   
    confirmed_node['selected'].setValue(False)
    for node in original_selection: 
        node['selected'].setValue(True)
    return confirmed_node


# -------------------------------------------------------------------------
# Part 1: 环境检测与语言预选
# -------------------------------------------------------------------------
def set_knob_safe(node, knob_names, value):
    """安全设置 Knob 参数，兼容不同 Nuke 版本的节点字段命名差异"""
    if not node:
        return False
    if isinstance(knob_names, str):
        knob_names = [knob_names]
    for name in knob_names:
        if name in node.knobs():
            try:
                node[name].setValue(value)
                return True
            except Exception:
                pass
    return False
try:
    read_node = nuke.selectedNode()
    if read_node.Class() != "Read":
        nuke.message(lang_pack["en"]["err_invalid_read"] + "\n" + lang_pack["zh"]["err_invalid_read"])
        read_node = None
except ValueError:
    nuke.message(lang_pack["en"]["err_no_selection"] + "\n" + lang_pack["zh"]["err_no_selection"])
    read_node = None

if read_node:
    # 语言预选择器 
    lang_choice = nuke.choice("Language / 语言", "Please select UI language / 请选择面板语言:", ["English", "中文"])
    if lang_choice == -1:
        pass # 用户取消
    else:
        current_lang = "en" if lang_choice == 0 else "zh"
        lang = lang_pack[current_lang]
        
        all_layers = nuke.layers(read_node)
        all_chans = read_node.channels()
        img_metadata = read_node.metadata()
        all_layers_lower = [l.lower() for l in all_layers]
        all_layers_lower = [layer.replace(' ', '_') for layer in all_layers_lower]

        # -------------------------------------------------------------------------
        # Part 2: Nuke Panel 主交互区
        # -------------------------------------------------------------------------
        user_choice = 1      
        engine_override = "auto"
        
        p = nuke.Panel(lang["panel_title"])
        p.addEnumerationPulldown(lang["mode_label"], lang["mode_opts"])
        p.addEnumerationPulldown(lang["engine_label"], lang["engine_opts"])
        p.addBooleanCheckBox(lang["qc_label"], False)

        if p.show():
            mode_val = p.value(lang["mode_label"])
            engine_val = p.value(lang["engine_label"])
            run_qc_mode = p.value(lang["qc_label"])
            
            user_choice = 0 if "Basic" in mode_val or "基础" in mode_val else 1
            run_advanced_mode = (user_choice == 1)

            if "Arnold" in engine_val: engine_override = "arnold"
            elif "Redshift" in engine_val: engine_override = "redshift"
            elif "V-Ray" in engine_val: engine_override = "vray"
            elif "Karma" in engine_val: engine_override = "karma"
            elif "UE" in engine_val or "Unreal" in engine_val: engine_override = "ue5"
            else: engine_override = "auto"

            # -------------------------------------------------------------------------
            # Part 3: 渲染器自动识别
            # -------------------------------------------------------------------------
            software_sign = img_metadata.get('exr/Software', '')
            
            is_ue5 = any(key.startswith('exr/unreal/') for key in img_metadata.keys())
            is_karma = "karma" in str(software_sign).lower() or any(key.startswith('exr/husk:') for key in img_metadata.keys())
            is_redshift = any(key.startswith('exr/rs/') for key in img_metadata.keys())
            if not is_redshift:
                rs_unique_signatures = ['diffuselighting', 'specularlighting', 'reflections', 'refractions']
                hit_count = 0
                for layer in all_layers_lower:
                    layer_clean = layer.split('.')[0] if '.' in layer else layer
                    for sig in rs_unique_signatures:
                        if sig == layer_clean:
                            hit_count += 1
                            break
                if hit_count >= 2:
                    is_redshift = True
            is_vray = any(key.startswith('exr/vray') for key in img_metadata.keys()) or 'exr/vfb2_layers_json' in img_metadata.keys()
            
            if engine_override != "auto":
                current_renderer = engine_override
            else:
                if is_ue5: current_renderer = "ue5"
                elif is_vray: current_renderer = "vray"
                elif is_karma: current_renderer = "karma"
                elif is_redshift: current_renderer = "redshift"
                else: current_renderer = "arnold" 
                
            print(lang["log_locked_renderer"].format(engine=current_renderer.upper()))

            if current_renderer == "ue5":

                # =========================================================
                # UE5 专属节点构建逻辑
                # =========================================================
                for n in nuke.allNodes():
                    n.setSelected(False)

                read_x = read_node.xpos()
                read_y = read_node.ypos()

                # 1. 顶部 Dot
                dot_main = create_isolated_node("Dot")
                dot_main.setXYpos(read_x + 34, read_y + 120)
                dot_main.setInput(0, read_node)

                # 2. 右侧 Cryptomatte 分支
                right_branch_x = read_x + 214
                dot_right = create_isolated_node("Dot")
                dot_right.setXYpos(right_branch_x, read_y + 120)
                dot_right.setInput(0, dot_main)

                try:
                    cryptomatte_node = create_isolated_node("Cryptomatte")
                    cryptomatte_node.setName("Cryptomatte1")
                    cryptomatte_node.setInput(0, dot_right)
                    cryptomatte_node.setXYpos(right_branch_x - 34, read_y + 200)
                except Exception:
                    pass

                # 3. Unpremult -> Premult 链条
                unpremult = create_isolated_node("Unpremult")
                unpremult.setName("Unpremult1")
                unpremult.setInput(0, dot_main)
                unpremult.setXYpos(read_x, read_y + 200)

                premult = create_isolated_node("Premult")
                premult.setName("Premult1")
                premult.setInput(0, unpremult)
                premult.setXYpos(read_x, read_y + 280)

                current_ue_out = premult
                curr_y = read_y + 360

               # 4. Depth 
                ue_depth_chan = None
                depth_candidates = [
                    c for c in all_chans 
                    if 'cutout' not in c.lower() and ('depth' in c.lower() or c.lower().endswith('.z'))
                ]

                # 第一优先级：锁定 .red 或 .r 通道 (UE5 WorldDepth 默认存放在 R 通道)
                for c in depth_candidates:
                    if c.lower().endswith('.red') or c.lower().endswith('.r'):
                        ue_depth_chan = c
                        break

                # 第二优先级：锁定 .z 通道
                if not ue_depth_chan:
                    for c in depth_candidates:
                        if c.lower().endswith('.z'):
                            ue_depth_chan = c
                            break

                # 第三优先级：排除 alpha 后的首个有效通道
                if not ue_depth_chan:
                    for c in depth_candidates:
                        if not (c.lower().endswith('.alpha') or c.lower().endswith('.a')):
                            ue_depth_chan = c
                            break

                # 兜底：若仍未获取则取候选列表首项
                if not ue_depth_chan and depth_candidates:
                    ue_depth_chan = depth_candidates[0]

                if ue_depth_chan:
                    zd = create_isolated_node("ZDefocus2")
                    zd.setName("ZDefocus1")
                    zd.setInput(0, current_ue_out)
                    set_knob_safe(zd, ['depthchannel', 'z_channel', 'depth_channel'], ue_depth_chan)
                    set_knob_safe(zd, 'math', 'far=0')
                    zd.setXYpos(read_x, curr_y)
                    current_ue_out = zd
                    curr_y += 80

                # 5. Motion Vector 
                ue_motion_layer = None
                for c in all_chans:
                    if any(kw in c.lower() for kw in ['motionvector', 'velocity', 'motion']):
                        ue_motion_layer = c.split('.')[0]
                        break

                if ue_motion_layer:
                    vb = create_isolated_node("VectorBlur2")
                    vb.setName("VectorBlur1")
                    vb.setInput(0, current_ue_out)
                    set_knob_safe(vb, ['uv', 'uv_channel', 'uvPop'], ue_motion_layer)
                    set_knob_safe(vb, 'channels', 'all')
                    vb.setXYpos(read_x, curr_y)
                    current_ue_out = vb
                    curr_y += 80

                current_trunk_y = curr_y
                last_merge_or_node = current_ue_out
                final_output_node = current_ue_out
                print(lang["log_success"].format(count=1))
                last_node = final_output_node

            if current_renderer != "ue5":
                # -------------------------------------------------------------------------
                # Part 4: 严格对立的图层过滤逻辑
                # -------------------------------------------------------------------------
                beauty_rebuild_list = []
                advanced_components = {} 
                ignore_list = ['rgb', 'rgba', 'alpha', 'depth', 'z']
                
                # 核心机制：定义每种模式绝对需要哪些层。不存在于当前列表的层一律不提取。
                strict_blueprints = {
                    "arnold": {
                        "basic": ['diffuse', 'specular', 'coat', 'transmission', 'sss', 'volume', 'emission', 'background', 'sheen'],
                      #"advanced": ['diffuse_direct', 'diffuse_indirect', 'specular_direct', 'specular_indirect', 'coat', 'transmission', 'sss', 'volume', 'emission', 'background', 'sheen']
                        "advanced": [
                            'diffusedirect', 'diffuseindirect',
                            'speculardirect', 'specularindirect',
                            'coatdirect', 'coatindirect',
                            'transmissiondirect', 'transmissionindirect',
                            'sssdirect', 'sssindirect',
                            'volumedirect', 'volumeindirect',
                            'sheendirect', 'sheenindirect',
                            'emission', 'background', 'sheen'
                        ]
                    },
    
                    "redshift": {
                        "basic": ['diffuselighting', 'specularlighting', 'emission',  'background', 'gi',  'reflections', 'refractions', 'sss'],
                        "advanced_plus": ['emission', 'background', 'sss', 'specularlighting', 'caustics'],
                        "advanced": [
            'diffuselightingraw', 'diffusefilter', 'reflectionsraw', 'reflectionsfilter', 'refractionsraw', 'refractionsfilter', 'translightingraw', 'transgiraw', 'transtint', 'specularlighting', 'emission', 'background', 'sss'
        ], 
                    },
                        
                    "vray": {
                        "basic": ['lighting', 'gi', 'reflect', 'refract', 'specular', 'sss', 'selfillum', 'caustics', 'background', 'atmosphere'],
                        "advanced_plus": ['sss', 'selfillum', 'caustics', 'background', 'atmosphere', 'specular', 'atmosphere'],
                        "advanced": ['diffuse', 'rawlight', 'rawgi', 'rawreflection', 'reflectionfilter', 'rawrefraction', 'refractionfilter', 'specular', 'sss', 'selfillum', 'caustics', 'background', 'atmosphere'],
                    },
                        
                    "karma": {
                        "basic": ['combineddiffuse', 'combinedglossyreflection', 'sss', 'combinedemission', 'volume', 'glossytransmission'],
                        "advanced_plus": ['sss', 'glossytransmission'],
                        "advanced": ['directdiffuse', 'indirectdiffuse', 'directglossyreflection', 'indirectglossyreflection', 'glossytransmission', 'sss', 'combinedemission', 'volume'],
                    }
                }
    
                for layer in all_layers:
                    layer_lower = layer.lower()
                    if layer_lower in ignore_list or "crypto" in layer_lower:
                        continue
    
                    stripped = "".join([char for char in layer_lower if not char.isdigit()]).strip('_')
                    layer_lower = layer_lower.replace(' ', '_')
                    stripped = stripped.replace(' ', '').replace('_', '')
    
                    # ================= ARNOLD =================
                    if current_renderer == "arnold":
                        if run_advanced_mode:
                            # 高级模式：只允许直接/间接层
                            if ("direct" in layer_lower or "indirect" in layer_lower) or stripped in strict_blueprints["arnold"]["advanced"]:
                                beauty_rebuild_list.append(layer)
                        else:
                            # 基础模式：只允许融合层
                            if "direct" not in layer_lower and "indirect" not in layer_lower:
                                if stripped in strict_blueprints["arnold"]["basic"]:
                                    beauty_rebuild_list.append(layer)
    
                    # ================= REDSHIFT =================
                    elif current_renderer == "redshift":
                        if run_advanced_mode:
                            if "filter" in layer_lower or "tint" in layer_lower:
                                comp = "diffuse" if "diffuse" in layer_lower else ("reflect" if "reflect" in layer_lower else "refract" if "refract" in layer_lower else "trans" if "trans" in layer_lower else None)
                                if comp: advanced_components.setdefault(comp, {"raw": [], "filter": None})["filter"] = layer
                            elif "raw" in layer_lower:
                                if any(x in layer_lower for x in ['diffuse', 'sss', 'caustics', 'gi'])and "trans" not in layer_lower:
                                    advanced_components.setdefault("diffuse", {"raw": [], "filter": None})["raw"].append(layer)
                                elif "reflect" in layer_lower:
                                    advanced_components.setdefault("reflect", {"raw": [], "filter": None})["raw"].append(layer)
                                elif "refract" in layer_lower:
                                    advanced_components.setdefault("refract", {"raw": [], "filter": None})["raw"].append(layer)
                                elif "trans" in layer_lower:
                                    advanced_components.setdefault("trans", {"raw": [], "filter": None})["raw"].append(layer)
                            elif stripped in strict_blueprints["redshift"]["advanced_plus"]:
                                beauty_rebuild_list.append(layer)
                        else:
                            if stripped in strict_blueprints["redshift"]["basic"]:
                                beauty_rebuild_list.append(layer)
    
                    # ================= V-RAY =================
                    elif current_renderer == "vray":
                        if run_advanced_mode:
                            if stripped == "diffuse": advanced_components.setdefault("diffuse", {"raw": [], "filter": None})["filter"] = layer
                            elif "raw" in stripped and ("light" in stripped or "gi" in stripped): advanced_components.setdefault("diffuse", {"raw": [], "filter": None})["raw"].append(layer)
                            elif "reflect" in stripped and "filter" in stripped: advanced_components.setdefault("reflect", {"raw": [], "filter": None})["filter"] = layer
                            elif "reflect" in stripped and "raw" in stripped: advanced_components.setdefault("reflect", {"raw": [], "filter": None})["raw"].append(layer)
                            elif "refract" in stripped and "filter" in stripped: advanced_components.setdefault("refract", {"raw": [], "filter": None})["filter"] = layer
                            elif "refract" in stripped and "raw" in stripped: advanced_components.setdefault("refract", {"raw": [], "filter": None})["raw"].append(layer)
                            elif stripped in strict_blueprints["vray"]["advanced_plus"]:
                                beauty_rebuild_list.append(layer)
                        else:
                            if stripped in strict_blueprints["vray"]["basic"]:
                                beauty_rebuild_list.append(layer)
    
                    # ================= KARMA =================
                    elif current_renderer == "karma":
                        if run_advanced_mode:
                            # 1. 定义需要检测 Direct/Indirect 拆分的核心组件大类
                            core_components = ['diffuse', 'glossyreflection', 'volume', 'emission']
                            
                            # 2. 识别当前处理的层属于哪一个核心组件
                            detected_comp = None
                            for comp in core_components:
                                if comp in layer_lower:
                                    detected_comp = comp
                                    break
                            
                            # 3. 如果属于核心组件，执行动态分支判定
                            if detected_comp:
                                # 利用 all_layers_lower 检索整个 EXR 里是否同时存在该组件的 direct 和 indirect
                                has_direct = any(f"{detected_comp}_direct" in l for l in all_layers_lower)
                                has_indirect = any(f"{detected_comp}_indirect" in l for l in all_layers_lower)
                                
                                if has_direct and has_indirect:
                                    # 【优先轨】如果 direct 和 indirect 都齐活了，只收集带后缀的拆分层
                                    if "direct" in layer_lower or "indirect" in layer_lower:
                                        beauty_rebuild_list.append(layer)
                                else:
                                    # 【Fallback 轨】只要缺了任意一个，就降级收集合并层（过滤掉带单边后缀的残缺层）
                                    if "direct" not in layer_lower and "indirect" not in layer_lower:
                                        # 收集 combined_diffuse 或者基础干净的 diffuse 层
                                        if "combined" in layer_lower or stripped == detected_comp:
                                            beauty_rebuild_list.append(layer)
                            else:
                                # 4. 如果不属于核心组件（如 emission, background 等独立 Plus 层），直接按白名单收集
                                if stripped in strict_blueprints["karma"]["advanced_plus"]:
                                    beauty_rebuild_list.append(layer)
                        else:
                            # 基础模式保持不变
                            if stripped in strict_blueprints["karma"]["basic"]:
                                beauty_rebuild_list.append(layer)
    
                # -------------------------------------------------------------------------
                # Part 5: Node Graph 拼设节点树
                # -------------------------------------------------------------------------
                read_x = read_node.xpos()
                read_y = read_node.ypos()
                last_merge_or_node = None
                last_top_node = read_node
                
                final_output_nodes = []
                column_index = 0
    
                # 进阶模式的 Mtl 构建
                if run_advanced_mode and advanced_components:
                    for comp_name, data in advanced_components.items():
                        raw_list, filter_layer = data["raw"], data["filter"]
                        
                        if raw_list and filter_layer:
                            offset_x = read_x + (column_index * 180)
                            raw_shuffles = []
                            
                            # RAW 层
                            for r_idx, raw_layer in enumerate(raw_list):
                                top_dot = create_isolated_node("Dot")
                                top_dot.setInput(0, last_top_node)
                                top_dot.setXYpos(offset_x + (r_idx * 90) + 34, read_y + 120)
                                last_top_node = top_dot
    
                                shf = create_isolated_node("Shuffle2")
                                shf['in1'].setValue(raw_layer)
                                shf.setName(f"Shuffle_{raw_layer}")
                                shf.setInput(0, top_dot)
                                if 'postage_stamp' in shf.knobs(): shf['postage_stamp'].setValue(True)
                                shf.setXYpos(offset_x + (r_idx * 90), read_y + 250)
                                raw_shuffles.append(shf)
                            
                            # Filter 层 
                            top_dot_f = create_isolated_node("Dot")
                            top_dot_f.setInput(0, last_top_node)
                            top_dot_f.setXYpos(offset_x + (len(raw_list) * 90) + 34, read_y + 120)
                            last_top_node = top_dot_f
    
                            shf_filter = create_isolated_node("Shuffle2")
                            shf_filter['in1'].setValue(filter_layer)
                            shf_filter.setName(f"Shuffle_{filter_layer}")
                            shf_filter.setInput(0, top_dot_f)
                            if 'postage_stamp' in shf_filter.knobs(): shf_filter['postage_stamp'].setValue(True)
                            shf_filter.setXYpos(offset_x + (len(raw_list) * 90), read_y + 250)
                            
                            # Raw 合并 
                            if len(raw_shuffles) > 1:
                                current_raw_chain = raw_shuffles[0]
                                for add_idx in range(1, len(raw_shuffles)):
                                    m_raw_plus = create_isolated_node("Merge2")
                                    m_raw_plus['operation'].setValue('plus')
                                    m_raw_plus.setName(f"Merge_RawCombine_{comp_name}")
                                    m_raw_plus.setInput(0, current_raw_chain)
                                    m_raw_plus.setInput(1, raw_shuffles[add_idx])
                                    m_raw_plus.setXYpos(offset_x, read_y + 340 + ((add_idx - 1) * 40))
                                    current_raw_chain = m_raw_plus
                                core_energy_node = current_raw_chain
                            else:
                                core_energy_node = raw_shuffles[0]
                            
                            # Filter Mtl 相乘节点
                            m_multiply = create_isolated_node("Merge2")
                            m_multiply['operation'].setValue('multiply')
                            m_multiply.setName(f"Merge_Mult_{comp_name}")
                            m_multiply.setInput(0, core_energy_node)
                            m_multiply.setInput(1, shf_filter)
                            m_multiply.setXYpos(offset_x, read_y + 460)
                            
                            final_output_nodes.append((m_multiply, comp_name, offset_x))
                            column_index += (len(raw_list) + 1)
    
                # 基础层的 Plus 合并
                for layer in beauty_rebuild_list:
                    offset_x = read_x + (column_index * 180)
                    
                    top_dot = create_isolated_node("Dot")
                    top_dot.setInput(0, last_top_node)
                    top_dot.setXYpos(offset_x + 34, read_y + 120)
                    last_top_node = top_dot
                    
                    shuffle_node = create_isolated_node("Shuffle2")
                    shuffle_node['in1'].setValue(layer)
                    shuffle_node.setName(f"Shuffle_{layer}")
                    shuffle_node.setInput(0, top_dot)
                    if 'postage_stamp' in shuffle_node.knobs():
                        shuffle_node['postage_stamp'].setValue(True)
                    shuffle_node.setXYpos(offset_x, read_y + 250)
    
                    final_output_nodes.append((shuffle_node, layer, offset_x))
                    column_index += 1
                    
    
                # 主干合成树 Plus 节点群
                for index, (node, layer_name, x_pos) in enumerate(final_output_nodes):
                    m_x = read_x
                    m_y = read_y + 500 + ((index - 1) * 120)
                    current_trunk_y = m_y            
    
                    if index == 0:
                        last_merge_or_node = node
                    else:
                        merge_node = create_isolated_node("Merge2")
                        merge_node['operation'].setValue('plus')
                        merge_node.setName(f"Merge_Plus_{layer_name}")
                        
                        dot_node = create_isolated_node("Dot")
                        dot_node.setInput(0, node)
                        
                        merge_node.setInput(0, last_merge_or_node)
                        merge_node.setInput(1, dot_node)
                        merge_node.setXYpos(m_x, m_y)
                        dot_node.setXYpos(x_pos + 34, m_y + 4)
                        
                        last_merge_or_node = merge_node
            # -------------------------------------------------------------------------
            # Part 6: QC 质量验证模块 (完全匹配当前模式配方)
            # -------------------------------------------------------------------------
            if run_qc_mode and last_merge_or_node:
                print(lang["log_qc_start"])

                qc_merge = create_isolated_node("Merge2")
                qc_merge['operation'].setValue('difference')
                qc_merge.setName("QC_Difference_Check")
                read_side_dot = create_isolated_node("Dot")
                read_side_dot.setInput(0, read_node)
                read_side_dot.setXYpos(int(read_x - 120), int(current_trunk_y + 4))
                qc_merge.setInput(0, read_side_dot)        
                qc_merge.setInput(1, last_merge_or_node)   
                qc_merge.setXYpos(int(read_x), int(current_trunk_y + 150))
                active_viewer = nuke.activeViewer()
                if active_viewer: 
                    active_viewer.node().setInput(0, qc_merge)

                if run_advanced_mode:
                    # 开放 Arnold 和 Redshift 的高级 QC 审计名单
                    if current_renderer in ["arnold", "redshift", "vray"]:
                        mode_key = "advanced"
                    else:
                        # karma  等其他渲染器暂时用 basic 兜底
                        mode_key = "basic" 
                else:
                    mode_key = "basic"
                
                current_keywords = strict_blueprints.get(current_renderer, {}).get(mode_key, [])
                
                missing_in_exr = []
                for keyword in current_keywords:
                    if not any(keyword in layer for layer in all_layers_lower):
                        missing_in_exr.append(keyword)

                # 节点提取校验 (应提取的 vs 实际提取的)
                expected_layers = set(l.lower() for l in beauty_rebuild_list)
                if run_advanced_mode and advanced_components:
                    for comp, data in advanced_components.items():
                        if data["filter"]: expected_layers.add(data["filter"].lower())
                        for rl in data["raw"]: expected_layers.add(rl.lower())

                actually_shuffled = set()
                for n in nuke.allNodes("Shuffle2"):
                    if n.name().startswith("Shuffle_"):
                        actually_shuffled.add(n.name().replace("Shuffle_", "").lower())

                missing_extract = [l for l in (expected_layers - actually_shuffled)]

                # 生成单语种报表
                current_mode_str = "Advanced" if run_advanced_mode else "Basic"
                report_msg = f"<font size='5'><b>{lang['report_title']}</b></font><br><br>"

                total_standard = len(current_keywords)
                missing_count = len(missing_in_exr)
                present_count = total_standard - missing_count

                if missing_in_exr:
                    report_msg += f"<font color='#FFA500' size='4'><b>{lang['standard_warn_title']}</b></font><br>"
                    report_msg += f"{lang['current_renderer']}{current_renderer.upper()}<br>"
                    report_msg += lang["standard_count"].format(total=total_standard, present=present_count, missing=missing_count) + "<br>"
                    report_msg += f"{lang['standard_missing_list']}<br>"
                    for kw in sorted(missing_in_exr):
                        report_msg += f"⚠️ {kw}<br>"
                    report_msg += f"<br><font color='#A9A9A9'>{lang['standard_note']}</font><br>"
                else:
                    report_msg += f"<font color='#00FF7F' size='4'><b>{lang['standard_ok_title']}</b></font><br>"
                    report_msg += lang["standard_ok_desc"].format(total=total_standard) + "<br>"
                report_msg += "<br>"

                actual_count = len(actually_shuffled & expected_layers)
                if missing_extract:
                    report_msg += f"<font color='#FF4500' size='4'><b>{lang['extract_error_title']}</b></font><br>"
                    report_msg += lang["extract_count"].format(expected=len(expected_layers), actual=actual_count) + "<br>"
                    report_msg += lang["extract_missing_list"].format(count=len(missing_extract)) + "<br>"
                    for l in sorted(missing_extract):
                        report_msg += f"❌ {l}<br>"
                    report_msg += "<br>"
                else:
                    report_msg += f"<font color='#00FF7F' size='4'><b>{lang['extract_ok_title']}</b></font><br>"
                    report_msg += lang["extract_ok_desc"].format(expected=len(expected_layers), actual=actual_count) + "<br><br>"

                report_msg += f"<font color='#00FFFF'>{lang['footer_info'].format(mode=current_mode_str.upper(), engine=current_renderer.upper())}</font>"
                nuke.message(report_msg)

# -------------------------------------------------------------------------
            # Part 7: Final Output Chain (Alpha + Unpremult + Premult + Effects)
            # -------------------------------------------------------------------------
            # 辅助函数：安全设置 Knob 属性，防止因 Nuke 版本/节点类差异引发 NameError 报错
            if current_renderer != "ue5":
                def set_knob_safe(node, knob_names, value):
                    if isinstance(knob_names, str):
                        knob_names = [knob_names]
                    for name in knob_names:
                        knob = node.knob(name)
                        if knob is not None:
                            try:
                                knob.setValue(value)
                                return True
                            except Exception:
                                pass
                    return False
    
                # 辅助函数：安全创建独立节点，强制取消选中，彻底消除自动连到 Read 节点的斜线 Bug
                def create_clean_node(node_class_name):
                    for n in nuke.allNodes():
                        n.setSelected(False)
                    try:
                        return getattr(nuke.nodes, node_class_name)()
                    except AttributeError:
                        return nuke.createNode(node_class_name, inpanel=False)
    
    # ============================== Depth  ============================
                depth_channel_name = None
                channels_lower_map = {chan.lower(): chan for chan in all_chans}
    
                # 第一优先级：精准检索标准 Depth 通道
                priority_channels = ['depth.Z', 'z.red', 'z.r', 'z.z', 'z', 'depth_extra.depth', 'depth_extra.z', 'depth_extra.red', 'depth_extra.r', 'depth.red', 'depth.x', 'pz.r', 'scenedepth.z', 'worlddepth.z', 'worlddepth.r', 'scene_depth.z']
                for target in priority_channels:
                    if target in channels_lower_map:
                        depth_channel_name =channels_lower_map[target]
                        print(f"✅ Priority 1: Found exact match for depth: {depth_channel_name}")
                        break
    
                if not depth_channel_name:
                    exclude_keywords = ['cutout', 'crypto', 'matte', 'shadow', 'mask', 'alpha', 'primvar']
                    for chan in all_chans:
                        c_lower = chan.lower()
                        if any(ex in c_lower for ex in exclude_keywords):
                            continue
                        depth_keywords = ['depth', '.z', 'z.z', 'pz']
                        if any(kw in c_lower for kw in depth_keywords):
                            if c_lower.startswith(('z.', 'pz.')) and not (c_lower.endswith(('.z', '.r', '.red', '.x'))):
                                continue
                            depth_channel_name = chan
                            print(f"✅ Priority 2: Fuzzy match found depth: {depth_channel_name}")
                            break 
                if depth_channel_name:
                    print(f"[Pipeline Info] 成功识别到 Depth 通道: {depth_channel_name}")
                else:
                    print(f"[Pipeline Warning] 识别失败！EXR 包含的所有通道为: {all_channels}")
    
                # 备用方案：若仅匹配到图层名，强制拼接标准的 .Z 通道名
                if not depth_channel_name and depth_layer:
                    depth_channel_name = f"{depth_layer}.Z"
    
                # ========== 2. 智能匹配运动矢量层（排除 Crypto/Primvar 干扰） ==========
                motion_layer = None
                for layer in all_layers:
                    l_lower = layer.lower().strip()
                    if 'crypto' in l_lower or 'primvar' in l_lower:
                        continue
                    if l_lower in ['motion', 'motionvectors', 'motion_vectors', 'velocity', 'mv', 'vector', 'vectors']:
                        motion_layer = layer
                        break
                    elif any(kw in l_lower for kw in ['motionvector', 'motion_vector', 'velocity']):
                        motion_layer = layer
                        break
    
                # 坐标计算：主链垂直对齐，右侧分支与最右列 Dot 同 X 轴对齐
                chain_base_x = read_x
                chain_start_y = current_trunk_y + 180
                current_output = last_merge_or_node
                right_branch_x = read_x + (column_index * 180) + 34 
    
                # ========== 3. Copy Alpha ==========
                alpha_dot_top = create_clean_node("Dot")
                alpha_dot_top.setInput(0, top_dot)
                alpha_dot_top.setXYpos(right_branch_x, read_y + 120)
    
                # 底部 Dot：位于 Copy 节点右侧的直角转弯点
                alpha_dot_bottom = create_clean_node("Dot")
                alpha_dot_bottom.setInput(0, alpha_dot_top)
                alpha_dot_bottom.setXYpos(right_branch_x, chain_start_y + 12)
    
                copy_alpha = create_clean_node("Copy")
                copy_alpha.setName("Copy_Alpha")
                copy_alpha.setInput(0, current_output)
                copy_alpha.setInput(1, alpha_dot_bottom)  # 垂直下拉后横向接入 Input 1
                set_knob_safe(copy_alpha, 'channels', 'alpha')
                copy_alpha.setXYpos(chain_base_x, chain_start_y)
                current_output = copy_alpha
    
                # ========== 4. Unpremult：反预乘 ==========
                unpremult = create_clean_node("Unpremult")
                unpremult.setName("Unpremult_Final")
                unpremult.setInput(0, current_output)
                unpremult.setXYpos(chain_base_x, chain_start_y + 80)
                current_output = unpremult
    
                # ========== 5. Premult：标准预乘 ==========
                premult = create_clean_node("Premult")
                premult.setName("Premult_Final")
                premult.setInput(0, current_output)
                premult.setXYpos(chain_base_x, chain_start_y + 160)
                current_output = premult
    
                effect_offset = 240  # 效果节点起始垂直偏移
    
                # ========== 6. VectorBlur2：新版运动模糊（主干垂直向下） ==========
                if motion_layer:
                    vector_blur = create_clean_node("VectorBlur2")
                    vector_blur.setName("VectorBlur_Final")
                    vector_blur.setInput(0, current_output)
                    set_knob_safe(vector_blur, ['uv', 'uv_channel', 'uvPop'], motion_layer)
                    set_knob_safe(vector_blur, 'channels', 'all')
                    vector_blur.setXYpos(chain_base_x, chain_start_y + effect_offset)
                    current_output = vector_blur
                    effect_offset += 80
    
                # ========== 7. ZDefocus2：景深模糊（指认完整深度通道 depth.Z） ==========
                if depth_channel_name:
                    z_defocus = create_clean_node("ZDefocus2")
                    z_defocus.setName("ZDefocus_Final")
                    z_defocus.setInput(0, current_output)
                    # 传入精确的通道名
                    set_knob_safe(z_defocus, ['depthchannel', 'z_channel', 'depth_channel', 'z', 'Z'], depth_channel_name)
                    set_knob_safe(z_defocus, 'math', 'far=0')
                    z_defocus.setXYpos(chain_base_x, chain_start_y + effect_offset)
                    current_output = z_defocus
                    effect_offset += 80
    
                # 最终输出节点句柄
                final_output_node = current_output
    
                 
    
                print(lang["log_success"].format(count=len(final_output_nodes)))