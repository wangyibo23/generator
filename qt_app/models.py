# -*- coding: utf-8 -*-
"""按键与硬件配置数据模型及布局计算"""

from __future__ import annotations

import copy
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .constants import (
    KEY_SPACING_U,
    KEY_TYPE_ENCODER,
    KEY_TYPE_KEY,
    NO_LED,
    NO_LED_LABEL,
    ROW_HEIGHT_U,
    ROW_SPACING_U,
    U_TO_PX,
    default_encoder_layers,
    u_to_px,
)


def generate_id() -> str:
    return f"key-{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"


@dataclass
class Key:
    id: str
    row: int
    order: int
    width_u: float = 1.0
    height_u: float = 1.0
    offset_x: float = 0.0
    rgb_index: int = 0  # NO_LED (-1) 表示无灯珠
    matrix_row: int = 0
    matrix_col: int = 0
    key_type: str = KEY_TYPE_KEY  # "key" | "encoder"
    # 普通键：四层功能
    layers: List[str] = field(default_factory=lambda: ["KC_NO", "KC_NO", "KC_NO", "KC_NO"])
    # 滚轮：四层 × [按下, 左滚, 右滚]
    encoder_layers: List[List[str]] = field(default_factory=default_encoder_layers)

    @property
    def is_encoder(self) -> bool:
        return self.key_type == KEY_TYPE_ENCODER

    @property
    def has_led(self) -> bool:
        return self.rgb_index != NO_LED

    def ensure_encoder_layers(self) -> None:
        while len(self.encoder_layers) < 4:
            self.encoder_layers.append(["KC_NO", "KC_NO", "KC_NO"])
        for i in range(4):
            row = list(self.encoder_layers[i])
            while len(row) < 3:
                row.append("KC_NO")
            self.encoder_layers[i] = row[:3]

    def encoder_funcs(self, layer: int) -> List[str]:
        self.ensure_encoder_layers()
        layer = max(0, min(3, layer))
        return list(self.encoder_layers[layer])

    def copy(self) -> "Key":
        return copy.deepcopy(self)


def parse_rgb_index(value) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        if value.strip().upper() in (NO_LED_LABEL, "NO LED", "-1"):
            return NO_LED
        try:
            return int(value.strip())
        except ValueError:
            return 0
    try:
        v = int(value)
        return NO_LED if v < 0 else v
    except (TypeError, ValueError):
        return 0


def export_rgb_index(rgb_index: int):
    if rgb_index == NO_LED:
        return NO_LED_LABEL
    return rgb_index


@dataclass
class HwConfig:
    row_count: int = 5
    col_count: int = 14
    rgb_led_count: int = 64
    side_led_enabled: bool = False
    side_led_count: int = 0
    logo_led_enabled: bool = False
    logo_led_count: int = 0
    has_screen: bool = False
    usb_device_name: str = "Custom Keyboard"
    pid: str = "0x6060"
    vid: str = "0xFEED"
    version: str = "1.0.0"
    bluetooth_names: List[str] = field(default_factory=lambda: ["BT_KB_1", "BT_KB_2", "BT_KB_3"])
    has_mode_switch: bool = False
    max_brightness: int = 255
    brightness_levels: int = 5
    speed_levels: int = 5


def get_preset_layout() -> List[Key]:
    rows_data = [
        {"row": 0, "keys": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]},
        {"row": 1, "keys": [1.1, 1, 1, 1, 1, 1, 1, 1, 1, 1]},
        {"row": 2, "keys": [1.25, 1, 1, 1, 1, 1, 1, 1, 1, 1.25]},
        {"row": 3, "keys": [5.6]},
    ]
    key_functions = [
        ["KC_ESC", "KC_GRV", "KC_NO", "KC_NO"],
        ["KC_1", "KC_F1", "KC_NO", "KC_NO"],
        ["KC_2", "KC_F2", "KC_NO", "KC_NO"],
        ["KC_3", "KC_F3", "KC_NO", "KC_NO"],
        ["KC_4", "KC_F4", "KC_NO", "KC_NO"],
        ["KC_5", "KC_F5", "KC_NO", "KC_NO"],
        ["KC_6", "KC_F6", "KC_NO", "KC_NO"],
        ["KC_7", "KC_F7", "KC_NO", "KC_NO"],
        ["KC_8", "KC_F8", "KC_NO", "KC_NO"],
        ["KC_9", "KC_F9", "KC_NO", "KC_NO"],
        ["KC_0", "KC_F10", "KC_NO", "KC_NO"],
        ["KC_Q", "KC_1", "KC_NO", "KC_NO"],
        ["KC_W", "KC_2", "KC_NO", "KC_NO"],
        ["KC_E", "KC_3", "KC_NO", "KC_NO"],
        ["KC_R", "KC_4", "KC_NO", "KC_NO"],
        ["KC_T", "KC_5", "KC_NO", "KC_NO"],
        ["KC_Y", "KC_6", "KC_NO", "KC_NO"],
        ["KC_U", "KC_7", "KC_NO", "KC_NO"],
        ["KC_I", "KC_8", "KC_NO", "KC_NO"],
        ["KC_O", "KC_9", "KC_NO", "KC_NO"],
        ["KC_P", "KC_0", "KC_NO", "KC_NO"],
        ["KC_A", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_S", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_D", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_F", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_G", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_H", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_J", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_K", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_L", "KC_NO", "KC_NO", "KC_NO"],
        ["KC_SPACE", "KC_ENTER", "KC_NO", "KC_NO"],
    ]
    keys: List[Key] = []
    order_counter = 0
    for row_data in rows_data:
        for idx, width_u in enumerate(row_data["keys"]):
            funcs = key_functions[order_counter] if order_counter < len(key_functions) else ["KC_NO"] * 4
            keys.append(
                Key(
                    id=generate_id(),
                    row=row_data["row"],
                    order=idx,
                    width_u=float(width_u),
                    height_u=1.0,
                    offset_x=0.0,
                    rgb_index=order_counter,
                    matrix_row=row_data["row"],
                    matrix_col=idx,
                    layers=list(funcs),
                )
            )
            order_counter += 1
    return keys


def calculate_key_positions(keys: List[Key], scale: float = U_TO_PX) -> Dict[str, dict]:
    rows_map: Dict[int, List[Key]] = {}
    for key in keys:
        rows_map.setdefault(key.row, []).append(key)
    for key_list in rows_map.values():
        key_list.sort(key=lambda k: k.order)

    positions: Dict[str, dict] = {}
    current_y = 0.0
    for row_idx in sorted(rows_map.keys()):
        key_list = rows_map[row_idx]
        current_x = 0.0
        for key in key_list:
            width_px = u_to_px(key.width_u, scale)
            height_px = u_to_px(key.height_u, scale)
            offset_x_px = u_to_px(key.offset_x, scale)
            positions[key.id] = {
                "x": current_x + offset_x_px,
                "y": current_y,
                "width": width_px,
                "height": height_px,
            }
            current_x += width_px + u_to_px(KEY_SPACING_U, scale)
        current_y += u_to_px(ROW_HEIGHT_U, scale) + u_to_px(ROW_SPACING_U, scale)
    return positions


def reassign_rgb_indices(keys: List[Key]) -> None:
    """按行/列顺序重新分配灯光索引；已标记 NO_LED 的按键保持不变。"""
    sorted_keys = sorted(keys, key=lambda k: (k.row, k.order))
    next_idx = 0
    for key in sorted_keys:
        if key.rgb_index == NO_LED:
            continue
        key.rgb_index = next_idx
        next_idx += 1


def find_key(keys: List[Key], key_id: str) -> Optional[Key]:
    for key in keys:
        if key.id == key_id:
            return key
    return None


def normalize_row_orders(keys: List[Key], row: int) -> None:
    row_keys = sorted([k for k in keys if k.row == row], key=lambda k: k.order)
    for i, key in enumerate(row_keys):
        key.order = i


class KeyboardDocument:
    """文档状态：按键列表、硬件配置、选中项、当前层。"""

    def __init__(self) -> None:
        self.keys: List[Key] = get_preset_layout()
        self.hw = HwConfig()
        self.selected_ids: Set[str] = set()
        self.active_layer: int = 0

    def selected_keys(self) -> List[Key]:
        return [k for k in self.keys if k.id in self.selected_ids]

    def max_rgb_index(self) -> int:
        vals = [k.rgb_index for k in self.keys if k.rgb_index != NO_LED]
        if not vals:
            return -1
        return max(vals)

    def batch_change_width(self, delta_u: float) -> bool:
        if not self.selected_ids:
            return False
        for key in self.selected_keys():
            new_w = max(0.25, round((key.width_u + delta_u) * 100) / 100)
            key.width_u = new_w
        return True

    def batch_change_offset(self, delta_u: float) -> bool:
        if not self.selected_ids:
            return False
        for key in self.selected_keys():
            key.offset_x = round((key.offset_x + delta_u) * 100) / 100
        return True

    def batch_move_order(self, delta: int) -> bool:
        if not self.selected_ids:
            return False
        keys_by_row: Dict[int, List[Key]] = {}
        for key in self.selected_keys():
            keys_by_row.setdefault(key.row, []).append(key)

        for row, selected_in_row in keys_by_row.items():
            row_keys = sorted([k for k in self.keys if k.row == row], key=lambda k: k.order)
            selected_orders = {k.order for k in selected_in_row}
            if delta > 0:
                for key in sorted(row_keys, key=lambda k: k.order, reverse=True):
                    if key.order in selected_orders:
                        next_key = next((k for k in row_keys if k.order == key.order + 1), None)
                        if next_key and next_key.order not in selected_orders:
                            key.order, next_key.order = next_key.order, key.order
            elif delta < 0:
                for key in sorted(row_keys, key=lambda k: k.order):
                    if key.order in selected_orders:
                        prev_key = next((k for k in row_keys if k.order == key.order - 1), None)
                        if prev_key and prev_key.order not in selected_orders:
                            key.order, prev_key.order = prev_key.order, key.order
            normalize_row_orders(self.keys, row)
        return True

    def batch_move_row(self, delta: int) -> bool:
        if not self.selected_ids:
            return False
        new_rows: Set[int] = set()
        for key in self.selected_keys():
            key.row = max(0, key.row + delta)
            new_rows.add(key.row)
        for row in new_rows:
            normalize_row_orders(self.keys, row)
        return True

    def delete_selected(self) -> bool:
        if not self.selected_ids:
            return False
        self.keys = [k for k in self.keys if k.id not in self.selected_ids]
        self.selected_ids.clear()
        rows = {k.row for k in self.keys}
        for row in rows:
            normalize_row_orders(self.keys, row)
        return True

    def add_key_after_selected(self, key_type: str = KEY_TYPE_KEY) -> Optional[Key]:
        if not self.selected_ids:
            return None
        selected_id = next(iter(self.selected_ids))
        selected = find_key(self.keys, selected_id)
        if not selected:
            return None
        row, order = selected.row, selected.order
        for k in self.keys:
            if k.row == row and k.order > order:
                k.order += 1
        if key_type == KEY_TYPE_ENCODER:
            layers = ["KC_NO", "KC_NO", "KC_NO", "KC_NO"]
            enc_layers = default_encoder_layers()
        else:
            layers = ["KC_NO", "KC_NO", "KC_NO", "KC_NO"]
            enc_layers = default_encoder_layers()
        new_key = Key(
            id=generate_id(),
            row=row,
            order=order + 1,
            width_u=1.0,
            height_u=1.0,
            offset_x=0.0,
            rgb_index=self.max_rgb_index() + 1,
            matrix_row=row,
            matrix_col=order + 1,
            key_type=key_type,
            layers=layers,
            encoder_layers=enc_layers,
        )
        self.keys.append(new_key)
        row_keys = sorted([k for k in self.keys if k.row == row], key=lambda k: k.order)
        led_keys = [k for k in row_keys if k.rgb_index != NO_LED]
        first_rgb = min((k.rgb_index for k in led_keys), default=0)
        led_i = 0
        for i, k in enumerate(row_keys):
            k.order = i
            k.matrix_col = i
            if k.rgb_index != NO_LED:
                k.rgb_index = first_rgb + led_i
                led_i += 1
        self.selected_ids = {new_key.id}
        return new_key

    def load_preset(self) -> None:
        self.keys = get_preset_layout()
        self.selected_ids.clear()
        self.active_layer = 0

    def to_export_dict(self) -> dict:
        positions = calculate_key_positions(self.keys)
        sorted_keys = sorted(self.keys, key=lambda k: (k.row, k.order))
        bt_names = list(self.hw.bluetooth_names[:3])
        while len(bt_names) < 3:
            bt_names.append("")
        return {
            "keyboard_info": {
                "name": self.hw.usb_device_name,
                "pid": self.hw.pid,
                "vid": self.hw.vid,
                "version": self.hw.version,
                "bluetooth_name": bt_names[0],
                "bluetooth_names": bt_names,
                "has_mode_switch": self.hw.has_mode_switch,
            },
            "matrix": {
                "rows": self.hw.row_count,
                "cols": self.hw.col_count,
            },
            "rgb": {
                "total_leds": self.hw.rgb_led_count,
                "side_led": {"enabled": self.hw.side_led_enabled, "count": self.hw.side_led_count},
                "logo_led": {"enabled": self.hw.logo_led_enabled, "count": self.hw.logo_led_count},
                "max_brightness": self.hw.max_brightness,
                "brightness_levels": self.hw.brightness_levels,
                "speed_levels": self.hw.speed_levels,
            },
            "has_screen": self.hw.has_screen,
            "keys": [
                self._export_key(k, positions)
                for k in sorted_keys
            ],
        }

    def _export_key(self, k: Key, positions: dict) -> dict:
        item = {
            "id": k.id,
            "type": k.key_type,
            "row": k.row,
            "order": k.order,
            "width_u": k.width_u,
            "height_u": k.height_u,
            "offset_x_u": k.offset_x,
            "x_px": round(positions[k.id]["x"]) if k.id in positions else 0,
            "y_px": round(positions[k.id]["y"]) if k.id in positions else 0,
            "rgb_index": export_rgb_index(k.rgb_index),
            "matrix_row": k.matrix_row,
            "matrix_col": k.matrix_col,
            "layers": k.layers,
        }
        if k.is_encoder:
            k.ensure_encoder_layers()
            item["encoder"] = {
                "layers": [
                    {"press": row[0], "left": row[1], "right": row[2]}
                    for row in k.encoder_layers
                ]
            }
            # 兼容旧格式：顶层 press/left/right 取 Layer 0
            item["encoder"]["press"] = k.encoder_layers[0][0]
            item["encoder"]["left"] = k.encoder_layers[0][1]
            item["encoder"]["right"] = k.encoder_layers[0][2]
        return item

    def export_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_export_dict(), f, ensure_ascii=False, indent=2)

    def import_json(self, path: str) -> Tuple[int, bool]:
        """导入配置。返回 (按键数, 是否有重复 RGB 索引)。"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data.get("keys"), list):
            raise ValueError("无效的配置文件：缺少 keys 数组")

        imported: List[Key] = []
        for k in data["keys"]:
            key_type = k.get("type") or k.get("key_type") or KEY_TYPE_KEY
            if key_type not in (KEY_TYPE_KEY, KEY_TYPE_ENCODER):
                key_type = KEY_TYPE_KEY
            layers = k.get("layers")
            enc_layers = default_encoder_layers()
            if key_type == KEY_TYPE_ENCODER:
                enc = k.get("encoder") or {}
                if isinstance(enc.get("layers"), list) and enc["layers"]:
                    enc_layers = []
                    for row in enc["layers"][:4]:
                        if isinstance(row, dict):
                            enc_layers.append(
                                [
                                    row.get("press", "KC_NO"),
                                    row.get("left", "KC_NO"),
                                    row.get("right", "KC_NO"),
                                ]
                            )
                        elif isinstance(row, list) and len(row) >= 3:
                            enc_layers.append([row[0], row[1], row[2]])
                        else:
                            enc_layers.append(["KC_NO", "KC_NO", "KC_NO"])
                    while len(enc_layers) < 4:
                        enc_layers.append(["KC_NO", "KC_NO", "KC_NO"])
                elif isinstance(enc, dict) and (enc.get("press") or enc.get("left") or enc.get("right")):
                    # 旧格式：仅一层
                    enc_layers = [
                        [enc.get("press", "KC_NO"), enc.get("left", "KC_NO"), enc.get("right", "KC_NO")],
                        ["KC_NO", "KC_NO", "KC_NO"],
                        ["KC_NO", "KC_NO", "KC_NO"],
                        ["KC_NO", "KC_NO", "KC_NO"],
                    ]
                elif isinstance(layers, list) and len(layers) >= 3:
                    enc_layers = [
                        [layers[0], layers[1], layers[2]],
                        ["KC_NO", "KC_NO", "KC_NO"],
                        ["KC_NO", "KC_NO", "KC_NO"],
                        ["KC_NO", "KC_NO", "KC_NO"],
                    ]
                layers = ["KC_NO", "KC_NO", "KC_NO", "KC_NO"]
            elif not (isinstance(layers, list) and len(layers) == 4):
                layers = ["KC_NO", "KC_NO", "KC_NO", "KC_NO"]
            imported.append(
                Key(
                    id=k.get("id") or generate_id(),
                    row=k.get("row", 0),
                    order=k.get("order", 0),
                    width_u=k.get("width_u", 1),
                    height_u=k.get("height_u", 1),
                    offset_x=k.get("offset_x_u", 0),
                    rgb_index=parse_rgb_index(k.get("rgb_index", 0)),
                    matrix_row=k.get("matrix_row", 0),
                    matrix_col=k.get("matrix_col", 0),
                    key_type=key_type,
                    layers=list(layers),
                    encoder_layers=enc_layers,
                )
            )
        self.keys = imported
        self.selected_ids.clear()
        self.active_layer = 0

        info = data.get("keyboard_info") or {}
        if info:
            self.hw.usb_device_name = info.get("name", self.hw.usb_device_name)
            self.hw.pid = info.get("pid", self.hw.pid)
            self.hw.vid = info.get("vid", self.hw.vid)
            self.hw.version = info.get("version", self.hw.version)
            names = info.get("bluetooth_names")
            if isinstance(names, list) and names:
                self.hw.bluetooth_names = [str(n) for n in names[:3]]
                while len(self.hw.bluetooth_names) < 3:
                    self.hw.bluetooth_names.append("")
            elif info.get("bluetooth_name"):
                self.hw.bluetooth_names = [str(info["bluetooth_name"]), "BT_KB_2", "BT_KB_3"]
            if isinstance(info.get("has_mode_switch"), bool):
                self.hw.has_mode_switch = info["has_mode_switch"]

        matrix = data.get("matrix") or {}
        if matrix:
            self.hw.row_count = matrix.get("rows", self.hw.row_count)
            self.hw.col_count = matrix.get("cols", self.hw.col_count)

        rgb = data.get("rgb") or {}
        if rgb:
            self.hw.rgb_led_count = rgb.get("total_leds", self.hw.rgb_led_count)
            side = rgb.get("side_led") or {}
            self.hw.side_led_enabled = bool(side.get("enabled", False))
            self.hw.side_led_count = side.get("count", 0)
            logo = rgb.get("logo_led") or {}
            self.hw.logo_led_enabled = bool(logo.get("enabled", False))
            self.hw.logo_led_count = logo.get("count", 0)
            self.hw.max_brightness = rgb.get("max_brightness", self.hw.max_brightness)
            self.hw.brightness_levels = rgb.get("brightness_levels", self.hw.brightness_levels)
            self.hw.speed_levels = rgb.get("speed_levels", self.hw.speed_levels)

        if isinstance(data.get("has_screen"), bool):
            self.hw.has_screen = data["has_screen"]

        indices = set()
        has_duplicate = False
        for key in self.keys:
            if key.rgb_index == NO_LED:
                continue
            if key.rgb_index in indices:
                has_duplicate = True
                break
            indices.add(key.rgb_index)
        return len(self.keys), has_duplicate
