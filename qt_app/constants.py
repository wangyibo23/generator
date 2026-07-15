# -*- coding: utf-8 -*-
"""单位换算与键码预设（对应 index.html）"""

U_TO_PX = 50  # 导出/默认参考比例；显示时由画布按可视宽度动态计算
KEY_SPACING_U = 0.25
ROW_SPACING_U = 0.25
ROW_HEIGHT_U = 1
MOVE_STEP_U = 0.25
KEYS_PER_ROW = 21  # 显示区域每行刚好放下的 1u 按键数


def row_capacity_u(keys_per_row: int = KEYS_PER_ROW) -> float:
    """n 个 1u 按键加间距所占总宽度（u）。"""
    if keys_per_row <= 0:
        return 0.0
    return keys_per_row + (keys_per_row - 1) * KEY_SPACING_U


def u_to_px(u: float, scale=None) -> float:
    return u * (U_TO_PX if scale is None else scale)


def px_to_u(px: float, scale=None) -> float:
    s = U_TO_PX if scale is None else scale
    return round((px / s) * 100) / 100


def fit_u_to_px(available_px: float, keys_per_row: int = KEYS_PER_ROW, padding_px: float = 40.0) -> float:
    """使 available_px 宽度刚好放下 keys_per_row 个 1u 键。"""
    capacity = row_capacity_u(keys_per_row)
    if capacity <= 0:
        return U_TO_PX
    usable = max(100.0, available_px - padding_px)
    return usable / capacity


KEY_TYPE_KEY = "key"
KEY_TYPE_ENCODER = "encoder"

ENCODER_FUNC_LABELS = ("按下", "左滚", "右滚")
ENCODER_LAYER_COUNT = 4
NO_LED = -1  # RGB 索引：无灯珠
NO_LED_LABEL = "NO_LED"


def default_encoder_layers():
    """四层 × [按下, 左滚, 右滚]。"""
    return [
        ["KC_MUTE", "KC_VOLD", "KC_VOLU"],
        ["KC_NO", "KC_NO", "KC_NO"],
        ["KC_NO", "KC_NO", "KC_NO"],
        ["KC_NO", "KC_NO", "KC_NO"],
    ]


KEYCODE_PRESETS = [
    "KC_F1", "KC_F2", "KC_F3", "KC_F4", "KC_F5", "KC_F6", "KC_F7", "KC_F8", "KC_F9", "KC_F10", "KC_F11", "KC_F12",
    "KC_NO", "KC_A", "KC_B", "KC_C", "KC_D", "KC_E", "KC_F", "KC_G", "KC_H", "KC_I", "KC_J", "KC_K", "KC_L", "KC_M",
    "KC_N", "KC_O", "KC_P", "KC_Q", "KC_R", "KC_S", "KC_T", "KC_U", "KC_V", "KC_W", "KC_X", "KC_Y", "KC_Z",
    "KC_1", "KC_2", "KC_3", "KC_4", "KC_5", "KC_6", "KC_7", "KC_8", "KC_9", "KC_0",
    "KC_PRINT_SCREEN", "KC_SCROLL_LOCK", "KC_PAUSE", "KC_INSERT", "KC_HOME", "KC_PAGE_UP", "KC_DELETE", "KC_END",
    "KC_PAGE_DOWN", "KC_RIGHT", "KC_LEFT", "KC_DOWN", "KC_UP", "KC_NUM_LOCK", "KC_KP_SLASH", "KC_KP_ASTERISK", "KC_KP_MINUS",
    "KC_KP_PLUS", "KC_KP_ENTER", "KC_KP_1", "KC_KP_2", "KC_KP_3", "KC_KP_4", "KC_KP_5", "KC_KP_6", "KC_KP_7", "KC_KP_8",
    "KC_KP_9", "KC_KP_0", "KC_KP_DOT", "KC_NONUS_BACKSLASH", "KC_APPLICATION", "KC_KB_POWER", "KC_KP_EQUAL",
    "KC_ENTER", "KC_ESC", "KC_BSPACE", "KC_TAB", "KC_SPACE", "KC_LCTRL", "KC_LALT", "KC_LGUI", "KC_RCTRL", "KC_RALT",
    "KC_F13", "KC_F14", "KC_F15", "KC_F16", "KC_F17", "KC_F18", "KC_F19", "KC_F20", "KC_F21", "KC_F22", "KC_F23", "KC_F24",
    "KC_AUDIO_MUTE", "KC_AUDIO_VOL_UP", "KC_AUDIO_VOL_DOWN", "KC_MEDIA_NEXT_TRACK", "KC_MEDIA_PREV_TRACK", "KC_MEDIA_STOP",
    "KC_MEDIA_PLAY_PAUSE", "KC_MEDIA_SELECT", "KC_MEDIA_EJECT", "KC_MAIL", "KC_CALCULATOR", "KC_MY_COMPUTER",
    "KC_WWW_SEARCH", "KC_WWW_HOME", "KC_WWW_BACK", "KC_WWW_FORWARD", "KC_WWW_STOP", "KC_WWW_REFRESH", "KC_WWW_FAVORITES",
    "KC_MEDIA_FAST_FORWARD", "KC_MEDIA_REWIND",
    "KC_BRIGHTNESS_UP", "KC_BRIGHTNESS_DOWN", "KC_CONTROL_PANEL", "KC_ASSISTANT", "KC_MISSION_CONTROL", "KC_LAUNCHPAD",
    "KC_NO_DISTURB",
    "KC_MS_UP", "KC_MS_DOWN", "KC_MS_LEFT", "KC_MS_RIGHT", "KC_MS_BTN1", "KC_MS_BTN2", "KC_MS_BTN3", "KC_MS_BTN4",
    "KC_MS_BTN5", "KC_MS_BTN6", "KC_MS_BTN7", "KC_MS_BTN8", "KC_MS_WH_UP", "KC_MS_WH_DOWN", "KC_MS_WH_LEFT", "KC_MS_WH_RIGHT",
    "KC_MS_ACCEL0", "KC_MS_ACCEL1", "KC_MS_ACCEL2",
    "KC_LEFT_CTRL", "KC_LEFT_SHIFT", "KC_LEFT_ALT", "KC_LEFT_GUI", "KC_RIGHT_CTRL", "KC_RIGHT_SHIFT", "KC_RIGHT_ALT", "KC_RIGHT_GUI",
    "LT(1, KC_SPC)", "TG(1)", "KC_TRNS",
    "MO(0)", "MO(1)", "MO(2)", "MO(3)", "MO(4)", "MO(5)", "MO(6)", "MO(7)",
    "TO(0)", "TO(1)", "TO(2)", "TO(3)", "TO(4)", "TO(5)", "TO(6)", "TO(7)",
    "KC_ENT", "KC_BSPC", "KC_SPC", "KC_MINS", "KC_EQL", "KC_LBRC", "KC_RBRC", "KC_BSLS", "KC_NUHS",
    "KC_SCLN", "KC_QUOT", "KC_GRV", "KC_COMM", "KC_SLSH", "KC_CAPS", "KC_PSCR", "KC_SCRL", "KC_BRMD", "KC_PAUS", "KC_BRK",
    "KC_BRMU", "KC_INS", "KC_PGUP", "KC_DEL", "KC_PGDN", "KC_RGHT", "KC_NUM", "KC_PSLS", "KC_PAST", "KC_PMNS",
    "KC_PPLS", "KC_PENT", "KC_P1", "KC_P2", "KC_P3", "KC_P4", "KC_P5", "KC_P6", "KC_P7", "KC_P8", "KC_P9", "KC_P0",
    "KC_PDOT", "KC_NUBS", "KC_APP", "KC_PEQL", "KC_EXEC", "KC_SLCT", "KC_AGIN", "KC_PSTE", "KC_LCAP", "KC_LNUM",
    "KC_LSCR", "KC_PCMM", "KC_INT1", "KC_INT2", "KC_INT3", "KC_INT4", "KC_INT5", "KC_INT6", "KC_INT7", "KC_INT8",
    "KC_INT9", "KC_LNG1", "KC_LNG2", "KC_LNG3", "KC_LNG4", "KC_LNG5", "KC_LNG6", "KC_LNG7", "KC_LNG8", "KC_LNG9",
    "KC_ERAS", "KC_SYRQ", "KC_CNCL", "KC_CLR", "KC_PRIR", "KC_RETN", "KC_SEPR", "KC_CLAG", "KC_CRSL", "KC_EXSL",
    "KC_PWR", "KC_SLEP", "KC_WAKE", "KC_MUTE", "KC_VOLU", "KC_VOLD", "KC_MNXT", "KC_MPRV", "KC_MSTP", "KC_MPLY",
    "KC_MSEL", "KC_EJCT", "KC_CALC", "KC_MYCM", "KC_WSCH", "KC_WHOM", "KC_WBAK", "KC_WFWD", "KC_WSTP", "KC_WREF",
    "KC_WFAV", "KC_MFFD", "KC_MRWD", "KC_BRIU", "KC_BRID", "KC_CPNL", "KC_ASST", "KC_MCTL", "KC_LPAD",
    "KC_MS_U", "KC_MS_D", "KC_MS_L", "KC_MS_R", "KC_WH_U", "KC_WH_D", "KC_WH_L", "KC_WH_R",
    "KC_ACL0", "KC_ACL1", "KC_ACL2",
    "KC_LCTL", "KC_LSFT", "KC_LOPT", "KC_LCMD", "KC_LWIN",
    "KC_RCTL", "KC_RSFT", "KC_ROPT", "KC_ALGR", "KC_RGUI", "KC_RCMD", "KC_RWIN",
    "MC_0", "MC_1", "MC_2", "MC_3", "MC_4", "MC_5", "MC_6", "MC_7", "MC_8", "MC_9", "MC_10", "MC_11", "MC_12", "MC_13",
    "MC_14", "MC_15", "MC_16", "MC_17", "MC_18", "MC_19", "MC_20", "MC_21", "MC_22", "MC_23", "MC_24", "MC_25",
    "MC_26", "MC_27", "MC_28", "MC_29", "MC_30", "MC_31",
    "RGB_TOG", "RGB_MODE_FORWARD", "RGB_MODE_REVERSE", "RGB_HUI", "RGB_HUD", "RGB_SAI", "RGB_SAD", "RGB_VAI", "RGB_VAD",
    "RGB_SPI", "RGB_SPD", "RGB_MODE_PLAIN", "RGB_MODE_BREATHE", "RGB_MODE_RAINBOW", "RGB_MODE_SWIRL", "RGB_MODE_SNAKE",
    "RGB_MODE_KNIGHT", "RGB_MODE_XMAS", "RGB_MODE_GRADIENT", "RGB_MODE_RGBTEST", "RGB_MODE_TWINKLE",
    "RGB_MOD", "RGB_RMOD", "RGB_M_P", "RGB_M_B", "RGB_M_R", "RGB_M_SW", "RGB_M_SN", "RGB_M_K", "RGB_M_X", "RGB_M_G",
    "RGB_M_T", "RGB_M_TW",
    "KC_K29", "KC_K42", "KC_K45", "KC_K56", "KC_K14", "KC_K132", "KC_K131", "KC_K133", "KC_K151", "KC_K150",
    "MD_24G", "MD_BLE1", "MD_BLE2", "MD_BLE3", "MD_USB", "QK_BAT", "QK_WLO", "SIX_N", "TEST_CL", "QK_DEB", "TIME_ST", "TIME_DT",
    "L_HOME", "L_KEY", "L_GIF", "L_LOOP", "L_LOOP1", "L_GIFCH", "L_SHUT", "L_BOOT", "L_RE_BO", "L_NEXT", "L_PREV", "L_ENT", "L_OPEN",
    "QMK_KB_MODE_2P4G", "QMK_KB_MODE_BLE1", "QMK_KB_MODE_BLE2", "QMK_KB_MODE_BLE3", "QMK_KB_MODE_USB", "QMK_BATT_NUM", "QMK_WIN_LOCK",
    "QMK_KB_SIX_N_CH", "QMK_TEST_COLOUR", "IOS_SIRI", "RGB_RTOG", "U_EE_CLR", "QMK_DEBOUNCE", "QMK_TIME_SET", "QMK_DTIME_SET",
    "HOME_MODE", "KEY_MODE", "GIF_MODE", "LOOP_MODE", "GIF_CHAGE", "LVGL_SHUTDOWN", "LVGL_BOOT", "LVGL_RESET_BOOT", "LVGL_OPEN", "LOOP_MODE_1",
    "LOGO_TOG", "LOGO_MOD", "LOGO_RMOD", "LOGO_HUI", "LOGO_HUD", "LOGO_SAI", "LOGO_SAD", "LOGO_VAI", "LOGO_VAD", "LOGO_SPI", "LOGO_SPD",
    "SIDE_TOG", "SIDE_MOD", "SIDE_RMOD", "SIDE_HUI", "SIDE_HUD", "SIDE_SAI", "SIDE_SAD", "SIDE_VAI", "SIDE_VAD", "SIDE_SPI", "SIDE_SPD",
    "QMK_KB_2P4G_PAIR", "QMK_KB_BLE1_PAIR", "QMK_KB_BLE2_PAIR", "QMK_KB_BLE3_PAIR", "LVGL_NEXT", "LVGL_PREV", "LVGL_ENT",
]

APP_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 12px;
}
QScrollArea {
    border: none;
    background: #1a1a1a;
}
QPushButton {
    background: #3c3c3c;
    border: none;
    color: white;
    padding: 6px 12px;
    border-radius: 8px;
}
QPushButton:hover {
    background: #4e4e4e;
}
QPushButton:checked {
    background: #6c5ce7;
}
QPushButton#dangerBtn {
    background: #8b5a5a;
}
QPushButton#dangerBtn:hover {
    background: #b16e6e;
}
QPushButton#importBtn {
    background: #4a6c8f;
}
QPushButton#exportBtn {
    background: #2c6e2c;
}
QPushButton#reassignBtn {
    background: #6c5ce7;
}
QPushButton#saveHwBtn {
    background: #2c6e2c;
}
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background: #1e1e1e;
    border: 1px solid #444;
    color: white;
    padding: 4px 6px;
    border-radius: 6px;
}
QGroupBox {
    background: #2c2c2c;
    border: 1px solid #3a3a3a;
    border-left: 4px solid #6c5ce7;
    border-radius: 12px;
    margin-top: 12px;
    padding: 12px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
    color: #ddd;
}
QLabel#hintLabel {
    color: #aaa;
    font-size: 11px;
}
QToolTip {
    background: #1e1e1e;
    color: #e0e0e0;
    border: 1px solid #555;
}
"""
