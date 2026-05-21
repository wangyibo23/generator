#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from datetime import datetime

try:
    from jinja2 import Environment, FileSystemLoader, TemplateError
except ImportError:
    print("[ERROR] 缺少 jinja2 模块，请执行：pip install jinja2", file=sys.stderr)
    sys.exit(1)

DEFAULT_TEMPLATE = "keyboard_config.c.j2"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "generated"
CONFIG_FILE = "config.json"

def parse_config(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"配置文件不存在: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    required = ['keyboard_info', 'matrix', 'rgb', 'keys']
    for field in required:
        if field not in data:
            raise KeyError(f"缺少顶层字段: {field}")
    info = data['keyboard_info']
    if 'pid' not in info or 'vid' not in info:
        raise KeyError("keyboard_info 中缺少 vid 或 pid")
    matrix = data['matrix']
    rows = matrix.get('rows')
    cols = matrix.get('cols')
    if not isinstance(rows, int) or not isinstance(cols, int):
        raise TypeError("matrix.rows 和 matrix.cols 必须是整数")
    rgb = data['rgb']
    total_leds = rgb.get('total_leds', 0)
    if total_leds <= 0:
        raise ValueError("rgb.total_leds 必须 > 0")
    keys = data['keys']
    if not keys:
        raise ValueError("keys 列表为空")
    return data, rows, cols, total_leds, keys, info, rgb

def build_matrix_map(keys, rows, cols, layers_count):
    matrix = [[['KC_NO'] * layers_count for _ in range(cols)] for _ in range(rows)]
    for key in keys:
        r = key.get('matrix_row')
        c = key.get('matrix_col')
        layers = key.get('layers')
        if r is None or c is None:
            continue
        if r >= rows or c >= cols:
            print(f"[警告] 忽略超出矩阵范围的键: row={r}, col={c}", file=sys.stderr)
            continue
        if not layers:
            continue
        for layer_idx, kc in enumerate(layers):
            if layer_idx >= layers_count:
                break
            if kc != 'KC_NO':
                matrix[r][c][layer_idx] = kc
    return matrix

def build_rgb_map(keys, total_leds):
    rgb_map = [None] * total_leds
    for key in keys:
        idx = key.get('rgb_index')
        if idx is None:
            continue
        if idx >= total_leds:
            print(f"[警告] RGB索引 {idx} 超出总LED数 {total_leds}，已忽略", file=sys.stderr)
            continue
        r = key.get('matrix_row')
        c = key.get('matrix_col')
        if r is None or c is None:
            print(f"[警告] 键缺少矩阵位置，无法映射RGB索引 {idx}", file=sys.stderr)
            continue
        if rgb_map[idx] is not None:
            print(f"[警告] RGB索引 {idx} 被重复定义，将覆盖旧值", file=sys.stderr)
        rgb_map[idx] = (r, c)
    valid = [(idx, {'row': r, 'col': c}) for idx, pos in enumerate(rgb_map) if pos is not None]
    if len(valid) < total_leds:
        print(f"[警告] 只有 {len(valid)}/{total_leds} 个LED被配置，其余将保持未使用状态", file=sys.stderr)
    return valid
# ---------- 生成 QMK info.json ----------
def generate_layout_data(keys):
    rows_dict = {}
    for key in keys:
        r = key.get('matrix_row')
        if r is None:
            continue
        rows_dict.setdefault(r, []).append(key)

    layout_rows = []  # 存储每行的按键数据（列表的列表）
    row_y = {0: 0.0, 1: 1.25, 2: 2.25, 3: 3.25, 4: 4.25, 5: 5.25}
    for r in sorted(rows_dict.keys()):
        row_keys = sorted(rows_dict[r], key=lambda k: k.get('order', 0))
        row_entries = []
        x = 0.0
        for key in row_keys:
            entry = {
                "matrix": [r, key['matrix_col']],
                "x": x,
                "y": row_y.get(r, r * 1.25)
            }
            w = key.get('width_u', 1.0)
            if w != 1.0:
                entry["w"] = w
            row_entries.append(entry)
            x += w
        layout_rows.append(row_entries)
    return layout_rows   # 返回二维列表

def main():
    template_name = DEFAULT_TEMPLATE
    if len(sys.argv) > 1:
        template_name = sys.argv[1]
        if not template_name.endswith('.j2'):
            template_name += '.j2'

    template_path = os.path.join(TEMPLATE_DIR, template_name)
    if not os.path.exists(template_path):
        print(f"[错误] 模板文件不存在: {template_path}", file=sys.stderr)
        sys.exit(1)
    
    info_template_name = "info.json.j2"
    info_output_path = os.path.join(OUTPUT_DIR, "info.json")
    
    

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        data, rows, cols, total_leds, keys, info, rgb = parse_config(CONFIG_FILE)
    except Exception as e:
        print(f"[错误] 解析配置文件失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 生成 layout_data
    layout_data = generate_layout_data(keys)
    
    
    
    # 获取层数
    layers_count = len(keys[0].get('layers', [])) if keys else 4
    print(f"检测到层数: {layers_count}")

    # 构建矩阵和RGB映射
    matrix = build_matrix_map(keys, rows, cols, layers_count)
    rgb_map_list = build_rgb_map(keys, total_leds)

    # ===== 预处理设备信息 =====
    # 1. 清理 VID/PID
    vid_clean = info.get('vid', '0x0000').replace('0x', '').replace('0X', '').upper()
    pid_clean = info.get('pid', '0x0000').replace('0x', '').replace('0X', '').upper()
    # 2. 转换版本号为十六进制字符串 (例如 "1.0.0" -> "0100")
    ver_str = info.get('version', '0.0.0')
    ver_parts = ver_str.split('.')
    # 确保有 3 部分
    while len(ver_parts) < 3:
        ver_parts.append('0')
    ver_int = (int(ver_parts[0]) << 8) | (int(ver_parts[1]) << 4) | int(ver_parts[2])
    device_ver_hex = f"{ver_int:04X}"
    
    # 按行和 order 排序，构建每行每层的键列表
    from itertools import groupby

    # 按 row 分组
    keys_by_row = {}
    for key in keys:
        r = key.get('matrix_row')
        if r is None:
            continue
        keys_by_row.setdefault(r, []).append(key)

    # 对每一行内的 keys 按 order 排序，然后按层提取键码
    # row_keys[layer][row] = list of keycodes (按 order)
    row_keys = []
    for layer in range(layers_count):
        layer_rows = []
        for r in range(rows):
            if r not in keys_by_row:
                layer_rows.append([])
                continue
            # 按 order 排序
            sorted_keys = sorted(keys_by_row[r], key=lambda k: k.get('order', 0))
            # 提取该层的键码
            row_keycodes = []
            for k in sorted_keys:
                layers_list = k.get('layers', [])
                kc = layers_list[layer] if layer < len(layers_list) else 'KC_NO'
                # if kc != 'KC_NO':
                #     row_keycodes.append(kc)
                row_keycodes.append(kc)
                # 如果想保留 KC_NO 也显示（不推荐），去掉上面 if 即可
            layer_rows.append(row_keycodes)
        row_keys.append(layer_rows)
    
    # ----- 新增：构建 LED 配置数据 -----
    # 定义 NO_LED 的值（QMK 中通常为 255）
    NO_LED = 255

    # # 获取矩阵尺寸
    # rows = data['matrix']['rows']
    # cols = data['matrix']['cols']
    # total_leds = data['rgb']['total_leds']  # 可能比实际键多，未使用的 LED 后面补占位

    # # 1. 构建 LED 矩阵映射 led_matrix[row][col] = rgb_index 或 NO_LED
    # led_matrix = [[NO_LED] * cols for _ in range(rows)]
    # for key in keys:
    #     r = key.get('matrix_row')
    #     c = key.get('matrix_col')
    #     idx = key.get('rgb_index')
    #     if r is not None and c is not None and idx is not None:
    #         led_matrix[r][c] = idx

    # # 2. 构建坐标数组 led_points[index] = (x, y)
    # # 初始化全为 (0,0)
    # led_points = [(0, 0)] * total_leds
    # # 缩放因子：QMK 中坐标常用 1/10 mm，这里假设 1px = 0.5 单位？示例中坐标很小，可能需要缩放
    # # 你可以根据需要调整缩放系数，例如坐标 = (x_px / 10, y_px / 10)
    # scale = 0.1  # 将像素缩小10倍，得到与示例类似的大小
    # for key in keys:
    #     idx = key.get('rgb_index')
    #     if idx is not None:
    #         x = key.get('x_px', 0) * scale
    #         y = key.get('y_px', 0) * scale
    #         # 转为整数（QMK 坐标通常是整数）
    #         led_points[idx] = (int(x), int(y))
            
    # ----- 重新索引 LED，按行和 order 排序 -----
    # 获取所有需要 LED 的键（有 rgb_index 的）
    valid_keys = [k for k in keys if k.get('rgb_index') is not None]

    # 按 (matrix_row, order) 排序
    valid_keys.sort(key=lambda k: (k.get('matrix_row', 0), k.get('order', 0)))

    # 分配新索引
    new_index_map = {}          # 旧 rgb_index -> 新索引
    new_led_points = []         # 按新索引顺序的坐标
    new_led_flags = []          # 按新索引顺序的标志
    new_row_col_to_new_idx = {} # (row, col) -> 新索引
    
    # 1. 构建 LED 矩阵映射 led_matrix[row][col] = rgb_index 或 NO_LED
    led_matrix = [[NO_LED] * cols for _ in range(rows)]
    for key in keys:
        r = key.get('matrix_row')
        c = key.get('matrix_col')
        idx = key.get('rgb_index')
        if r is not None and c is not None and idx is not None:
            led_matrix[r][c] = idx

    # 你可以根据需要调整缩放系数，例如坐标 = (x_px / 10, y_px / 10)
    scale = 0.160  # 将像素缩小10倍，得到与示例类似的大小
    
    for new_idx, key in enumerate(valid_keys):
        old_idx = key['rgb_index']
        r = key['matrix_row']
        c = key['matrix_col']
        new_index_map[old_idx] = new_idx
        new_row_col_to_new_idx[(r, c)] = new_idx
        
        # 坐标（需要提前计算好，假设之前已计算 led_points 原始坐标）
        x = int(key.get('x_px', 0) * scale)
        y = int(key.get('y_px', 0) * scale)
        new_led_points.append((x, y))
        new_led_flags.append(1)   # 默认 flag，可扩展

    # 更新 led_matrix：将所有旧索引替换为新索引
    for r in range(rows):
        for c in range(cols):
            if led_matrix[r][c] != NO_LED:
                old_val = led_matrix[r][c]
                led_matrix[r][c] = new_index_map.get(old_val, NO_LED)

    # 更新 led_points 和 led_flags
    led_points = new_led_points
    led_flags = new_led_flags
    total_leds = len(led_points)   # 实际 LED 数量
    
    # 3. 构建标志数组 led_flags[index] = flag (默认 1)
    led_flags = [1] * total_leds   # 1 = LED_FLAG_KEYLIGHT
    # 如果有特殊 LED（如底灯、指示等），可另行修改
    
    # 构建按行分组的坐标列表
    led_points_by_row = []
    idx = 0
    for r in range(rows):
        row_points = []
        for c in range(cols):
            if led_matrix[r][c] != NO_LED:
                row_points.append(led_points[idx])
                idx += 1
        led_points_by_row.append(row_points)
    
    led_flags_by_row = []
    idx = 0
    for r in range(rows):
        row_flags = []
        for c in range(cols):
            if led_matrix[r][c] != NO_LED:
                row_flags.append(led_flags[idx])
                idx += 1
        led_flags_by_row.append(row_flags)
        
    # 构建每行的坐标字符串列表
    led_points_lines = []
    led_flag_lines = []
    for r in range(rows):
        points = led_points_by_row[r]
        if points:
            # 将本行所有坐标格式化为 "{x,y}" 并用 ", " 连接
            # line = ", ".join(["{ {{:3d}}, {{:3d}} }}".format(x, y) for (x, y) in points])
            line = ", ".join(["{{ {:3d}, {:3d} }}".format(x, y) for (x, y) in points])
            # 添加缩进（4个空格）
            led_points_lines.append("    " + line)
        flags = led_flags_by_row[r]
        if flags:
            line = ", ".join(["{:3d}".format(flag) for flag in flags])
            # 添加缩进（4个空格）
            led_flag_lines.append("    " + line)
        # 如果某行没有 LED，可以选择忽略（不输出任何内容）
        # 如果希望保留空行注释，可取消下面注释
        # else:
        #     led_points_lines.append("    // no LEDs")


    

    context = {
        'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'info': info,
        'vid_clean': vid_clean,
        'pid_clean': pid_clean,
        'device_ver_hex': device_ver_hex,
        'ver_str' : ver_str,
        'rows': rows,
        'cols': cols,
        'rgb_total': total_leds,
        'rgb_max_brightness': rgb.get('max_brightness', 255),
        'rgb_brightness_steps': rgb.get('brightness_levels', 5),
        'rgb_speed_steps': rgb.get('speed_levels', 5),
        'layers_count': layers_count,
        'matrix': matrix,
        'rgb_map_list': rgb_map_list,
        'raw_data': data,
        'row_keys' : row_keys,
        'led_matrix' : led_matrix,
        'led_points' : led_points,
        'led_flags' : led_flags,
        'NO_LED' : NO_LED,
        'led_points_by_row' : led_points_by_row,
        'led_points_lines' : led_points_lines,
        'led_flag_lines' : led_flag_lines,
        
        'layout_data': layout_data,
        'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    # 将以上数据加入 context

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    try:
        template = env.get_template(template_name)
    except TemplateError as e:
        print(f"[错误] 加载模板失败: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        output_code = template.render(**context)
    except Exception as e:
        print(f"[错误] 渲染模板失败: {e}", file=sys.stderr)
        sys.exit(1)
    

    output_filename = template_name[:-3] if template_name.endswith('.j2') else template_name + '.c'
    output_file = os.path.join(OUTPUT_DIR, output_filename)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_code)
        print(f"成功生成: {output_file}")
    except Exception as e:
        print(f"[错误] 写入文件失败: {e}", file=sys.stderr)
        sys.exit(1)
        
    # 渲染 info.json.j2
    
    try:
        info_template = env.get_template(info_template_name)
        # info_context = {
        #     'info': info,
        #     'layout_data': layout_data,
        #     'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # }
        info_code = info_template.render(**context)
        with open(info_output_path, 'w', encoding='utf-8') as f:
            f.write(info_code)
        print(f"成功生成: {info_output_path}")
    except Exception as e:
        print(f"[警告] 生成 info.json 失败: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()