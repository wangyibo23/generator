# -*- coding: utf-8 -*-
"""主窗口：工具栏、硬件配置、按键编辑器"""

from __future__ import annotations

from PyQt5.QtCore import QEvent, QTimer, Qt
from PyQt5.QtGui import QKeyEvent, QShowEvent
from PyQt5.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QCompleter,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .constants import (
    ENCODER_FUNC_LABELS,
    KEY_TYPE_ENCODER,
    KEY_TYPE_KEY,
    KEYCODE_PRESETS,
    MOVE_STEP_U,
    NO_LED,
    NO_LED_LABEL,
)
from .models import KeyboardDocument, reassign_rgb_indices
from .widgets import (
    FocusWheelComboBox,
    FocusWheelDoubleSpinBox,
    FocusWheelSpinBox,
    KeyboardCanvas,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("键盘配置工具 - 智能灯光索引")
        self.resize(1400, 900)
        self.doc = KeyboardDocument()
        self._building_editor = False
        self._building_hw = False
        self._splitter_ratio_set = False

        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(8)

        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.setChildrenCollapsible(False)

        # ----- 上半区：键盘 + 右侧配置（约 60%） -----
        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(12)

        left = QFrame()
        left.setStyleSheet("QFrame { background: #252525; border-radius: 12px; }")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(12, 12, 12, 12)
        toolbar.setSpacing(8)

        self.btn_preset = QPushButton("60% 基础布局")
        self.btn_add = QPushButton("添加按键")
        self.btn_add_encoder = QPushButton("添加滚轮")
        self.btn_delete = QPushButton("删除选中")
        self.btn_delete.setObjectName("dangerBtn")
        self.btn_import = QPushButton("导入 JSON")
        self.btn_import.setObjectName("importBtn")
        self.btn_reassign = QPushButton("重新分配灯光索引")
        self.btn_reassign.setObjectName("reassignBtn")
        self.btn_export = QPushButton("导出 JSON")
        self.btn_export.setObjectName("exportBtn")

        for btn in (
            self.btn_preset,
            self.btn_add,
            self.btn_add_encoder,
            self.btn_delete,
            self.btn_import,
            self.btn_reassign,
        ):
            toolbar.addWidget(btn)

        toolbar.addStretch()
        self.layer_group = QButtonGroup(self)
        self.layer_buttons = []
        for i in range(4):
            btn = QPushButton(f"Layer {i}")
            btn.setCheckable(True)
            btn.setChecked(i == 0)
            self.layer_group.addButton(btn, i)
            self.layer_buttons.append(btn)
            toolbar.addWidget(btn)
        toolbar.addWidget(self.btn_export)

        left_layout.addLayout(toolbar)

        self.canvas_scroll = QScrollArea()
        self.canvas_scroll.setWidgetResizable(True)
        self.canvas_scroll.setStyleSheet("QScrollArea { background: #1a1a1a; border: none; }")
        self.canvas = KeyboardCanvas()
        self.canvas_scroll.setWidget(self.canvas)
        left_layout.addWidget(self.canvas_scroll, 1)
        self.canvas_scroll.viewport().installEventFilter(self)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setMinimumWidth(340)
        right_scroll.setMaximumWidth(420)
        right_scroll.setStyleSheet(
            "QScrollArea { background: #252525; border-radius: 12px; border: 1px solid #3a3a3a; }"
        )
        right_inner = QWidget()
        right_layout = QVBoxLayout(right_inner)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(12)

        self.hw_group = self._build_hw_group()
        right_layout.addWidget(self.hw_group)

        self.editor_host = QVBoxLayout()
        right_layout.addLayout(self.editor_host)

        tips = QGroupBox("使用提示")
        tips_layout = QVBoxLayout(tips)
        tip_text = QLabel(
            "• 空白处拖拽框选；Ctrl+拖拽追加选中\n"
            "• Ctrl+点击多选；←→ 交换 · ↑↓ 移行\n"
            "• 支持普通按键与滚轮（按下/左滚/右滚 · 四层）\n"
            "• 数值框需先点击选中后，滚轮才会改值\n"
            "• Esc 退出全屏 / F11 切换全屏\n"
            "• 底部为单个按键详细设置（约 40%）"
        )
        tip_text.setObjectName("hintLabel")
        tip_text.setWordWrap(True)
        tips_layout.addWidget(tip_text)
        right_layout.addWidget(tips)
        right_layout.addStretch()
        right_scroll.setWidget(right_inner)

        top_layout.addWidget(left, 3)
        top_layout.addWidget(right_scroll, 1)

        # ----- 下半区：单个按键详细设置（约 40%） -----
        bottom = QFrame()
        bottom.setObjectName("detailPanel")
        bottom.setStyleSheet(
            """
            QFrame#detailPanel {
                background: #252525;
                border-radius: 12px;
                border: 1px solid #3a3a3a;
            }
            """
        )
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(12, 8, 12, 12)
        bottom_layout.setSpacing(6)

        detail_title = QLabel("单个按键详细设置")
        detail_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ddd;")
        bottom_layout.addWidget(detail_title)

        self.detail_scroll = QScrollArea()
        self.detail_scroll.setWidgetResizable(True)
        self.detail_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        detail_inner = QWidget()
        self.detail_host = QVBoxLayout(detail_inner)
        self.detail_host.setContentsMargins(0, 0, 0, 0)
        self.detail_host.setSpacing(8)
        self.detail_scroll.setWidget(detail_inner)
        bottom_layout.addWidget(self.detail_scroll, 1)

        self.main_splitter.addWidget(top)
        self.main_splitter.addWidget(bottom)
        self.main_splitter.setStretchFactor(0, 3)
        self.main_splitter.setStretchFactor(1, 2)
        outer.addWidget(self.main_splitter)

        self._connect_signals()
        self.refresh_all()
        QApplication.instance().installEventFilter(self)

    def _build_hw_group(self) -> QGroupBox:
        group = QGroupBox("键盘硬件 & 设备信息")
        layout = QFormLayout(group)
        layout.setSpacing(8)

        self.hw_usb = QLineEdit()
        self.hw_pid = QLineEdit()
        self.hw_vid = QLineEdit()
        self.hw_version = QLineEdit()
        self.hw_bt = [QLineEdit(), QLineEdit(), QLineEdit()]
        self.hw_mode = FocusWheelComboBox()
        self.hw_mode.addItem("支持", True)
        self.hw_mode.addItem("不支持", False)
        self.hw_rows = FocusWheelSpinBox()
        self.hw_rows.setRange(0, 64)
        self.hw_cols = FocusWheelSpinBox()
        self.hw_cols.setRange(0, 64)
        self.hw_rgb = FocusWheelSpinBox()
        self.hw_rgb.setRange(0, 9999)
        self.hw_side_en = FocusWheelComboBox()
        self.hw_side_en.addItem("启用", True)
        self.hw_side_en.addItem("禁用", False)
        self.hw_side_count = FocusWheelSpinBox()
        self.hw_side_count.setRange(0, 9999)
        self.hw_logo_en = FocusWheelComboBox()
        self.hw_logo_en.addItem("启用", True)
        self.hw_logo_en.addItem("禁用", False)
        self.hw_logo_count = FocusWheelSpinBox()
        self.hw_logo_count.setRange(0, 9999)
        self.hw_screen = FocusWheelComboBox()
        self.hw_screen.addItem("是", True)
        self.hw_screen.addItem("否", False)
        self.hw_max_bri = FocusWheelSpinBox()
        self.hw_max_bri.setRange(0, 255)
        self.hw_bri_lv = FocusWheelSpinBox()
        self.hw_bri_lv.setRange(0, 100)
        self.hw_spd_lv = FocusWheelSpinBox()
        self.hw_spd_lv.setRange(0, 100)

        for w in (
            self.hw_rows,
            self.hw_cols,
            self.hw_rgb,
            self.hw_side_count,
            self.hw_logo_count,
            self.hw_max_bri,
            self.hw_bri_lv,
            self.hw_spd_lv,
            self.hw_mode,
            self.hw_side_en,
            self.hw_logo_en,
            self.hw_screen,
        ):
            w.setFocusPolicy(Qt.StrongFocus)

        layout.addRow("USB 设备名", self.hw_usb)
        layout.addRow("PID (hex)", self.hw_pid)
        layout.addRow("VID (hex)", self.hw_vid)
        layout.addRow("版本号", self.hw_version)
        layout.addRow("蓝牙设备名 1", self.hw_bt[0])
        layout.addRow("蓝牙设备名 2", self.hw_bt[1])
        layout.addRow("蓝牙设备名 3", self.hw_bt[2])
        layout.addRow("模式切换开关", self.hw_mode)
        layout.addRow("R 线数量", self.hw_rows)
        layout.addRow("C 线数量", self.hw_cols)
        layout.addRow("RGB 灯珠总数", self.hw_rgb)
        layout.addRow("侧灯支持", self.hw_side_en)
        layout.addRow("侧灯数量", self.hw_side_count)
        layout.addRow("Logo 灯支持", self.hw_logo_en)
        layout.addRow("Logo 灯数量", self.hw_logo_count)
        layout.addRow("支持屏幕", self.hw_screen)
        layout.addRow("最大亮度", self.hw_max_bri)
        layout.addRow("亮度档位", self.hw_bri_lv)
        layout.addRow("速度档位", self.hw_spd_lv)

        # 修改后自动写入文档（无需保存按钮）
        for edit in (self.hw_usb, self.hw_pid, self.hw_vid, self.hw_version, *self.hw_bt):
            edit.textChanged.connect(self._apply_hw_config)
        for spin in (
            self.hw_rows,
            self.hw_cols,
            self.hw_rgb,
            self.hw_side_count,
            self.hw_logo_count,
            self.hw_max_bri,
            self.hw_bri_lv,
            self.hw_spd_lv,
        ):
            spin.valueChanged.connect(self._apply_hw_config)
        for combo in (self.hw_mode, self.hw_side_en, self.hw_logo_en, self.hw_screen):
            combo.currentIndexChanged.connect(self._apply_hw_config)

        self.hw_side_en.currentIndexChanged.connect(self._update_side_logo_visibility)
        self.hw_logo_en.currentIndexChanged.connect(self._update_side_logo_visibility)
        return group

    def _connect_signals(self) -> None:
        self.btn_preset.clicked.connect(self._on_preset)
        self.btn_add.clicked.connect(lambda: self._on_add(KEY_TYPE_KEY))
        self.btn_add_encoder.clicked.connect(lambda: self._on_add(KEY_TYPE_ENCODER))
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_import.clicked.connect(self._on_import)
        self.btn_export.clicked.connect(self._on_export)
        self.btn_reassign.clicked.connect(self._on_reassign)
        self.layer_group.idClicked.connect(self._on_layer)
        self.canvas.selection_changed.connect(self._on_canvas_selection)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and isinstance(event, QKeyEvent):
            key = event.key()
            if key == Qt.Key_F11:
                self._toggle_fullscreen()
                return True
            if key == Qt.Key_Escape and self.isFullScreen():
                self.showNormal()
                return True
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                if not self._focus_in_text_input() and self.isActiveWindow():
                    if key == Qt.Key_Left:
                        self._batch_order(-1, silent=True)
                    elif key == Qt.Key_Right:
                        self._batch_order(1, silent=True)
                    elif key == Qt.Key_Up:
                        self._batch_row(-1, silent=True)
                    else:
                        self._batch_row(1, silent=True)
                    return True
        if obj is self.canvas_scroll.viewport() and event.type() == QEvent.Resize:
            self.canvas.set_viewport_width(self.canvas_scroll.viewport().width())
        return super().eventFilter(obj, event)

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        QTimer.singleShot(50, self._apply_splitter_ratio)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.canvas.set_viewport_width(self.canvas_scroll.viewport().width())
        if not self._splitter_ratio_set:
            self._apply_splitter_ratio()
            self._splitter_ratio_set = True

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        # 全屏后首次尺寸就绪时再对齐一次比例
        if not self._splitter_ratio_set and self.height() > 200:
            self._apply_splitter_ratio()
            self._splitter_ratio_set = True

    def _apply_splitter_ratio(self) -> None:
        total = max(1, self.main_splitter.height())
        self.main_splitter.setSizes([int(total * 0.60), int(total * 0.40)])

    def _focus_in_text_input(self) -> bool:
        w = QApplication.focusWidget()
        return isinstance(w, (QLineEdit, QAbstractSpinBox, QComboBox, QTextEdit))

    def _update_side_logo_visibility(self) -> None:
        self.hw_side_count.setEnabled(self.hw_side_en.currentData() is True)
        self.hw_logo_count.setEnabled(self.hw_logo_en.currentData() is True)

    def refresh_all(self) -> None:
        self.refresh_canvas()
        self.refresh_hw_form()
        self.refresh_editor()

    def refresh_canvas(self) -> None:
        self.canvas.set_data(self.doc.keys, self.doc.selected_ids, self.doc.active_layer)

    def refresh_hw_form(self) -> None:
        self._building_hw = True
        hw = self.doc.hw
        self.hw_usb.setText(hw.usb_device_name)
        self.hw_pid.setText(hw.pid)
        self.hw_vid.setText(hw.vid)
        self.hw_version.setText(hw.version)
        names = list(hw.bluetooth_names[:3])
        while len(names) < 3:
            names.append("")
        for i in range(3):
            self.hw_bt[i].setText(names[i])
        self.hw_mode.setCurrentIndex(0 if hw.has_mode_switch else 1)
        self.hw_rows.setValue(hw.row_count)
        self.hw_cols.setValue(hw.col_count)
        self.hw_rgb.setValue(hw.rgb_led_count)
        self.hw_side_en.setCurrentIndex(0 if hw.side_led_enabled else 1)
        self.hw_side_count.setValue(hw.side_led_count)
        self.hw_logo_en.setCurrentIndex(0 if hw.logo_led_enabled else 1)
        self.hw_logo_count.setValue(hw.logo_led_count)
        self.hw_screen.setCurrentIndex(0 if hw.has_screen else 1)
        self.hw_max_bri.setValue(hw.max_brightness)
        self.hw_bri_lv.setValue(hw.brightness_levels)
        self.hw_spd_lv.setValue(hw.speed_levels)
        self._update_side_logo_visibility()
        self._building_hw = False

    def _clear_layout(self, layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
            elif item.layout() is not None:
                self._clear_layout(item.layout())

    def _clear_host(self, host: QVBoxLayout) -> None:
        while host.count():
            item = host.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
            elif item.layout() is not None:
                self._clear_layout(item.layout())

    def refresh_editor(self) -> None:
        self._building_editor = True
        self._clear_host(self.editor_host)
        self._clear_host(self.detail_host)

        selected = self.doc.selected_keys()
        if not selected:
            box = QGroupBox("按键编辑")
            lay = QVBoxLayout(box)
            lbl = QLabel("点击选中 · 空白处拖拽框选\nCtrl+点击/框选追加 · ←→交换 · ↑↓移行")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #888;")
            lay.addWidget(lbl)
            self.editor_host.addWidget(box)

            placeholder = QLabel("请选择一个按键以在此编辑详细属性")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet("color: #888; font-size: 13px; padding: 24px;")
            self.detail_host.addWidget(placeholder)
            self._building_editor = False
            return

        avg_w = sum(k.width_u for k in selected) / len(selected)
        avg_off = sum(k.offset_x for k in selected) / len(selected)

        batch = QGroupBox(f"批量编辑（已选中 {len(selected)} 个）")
        bl = QVBoxLayout(batch)

        row_w = QHBoxLayout()
        btn_w_dec = QPushButton("-0.25u")
        btn_w_inc = QPushButton("+0.25u")
        btn_w_dec.clicked.connect(lambda: self._batch_width(-MOVE_STEP_U))
        btn_w_inc.clicked.connect(lambda: self._batch_width(MOVE_STEP_U))
        row_w.addWidget(btn_w_dec)
        row_w.addWidget(QLabel(f"平均: {avg_w:.2f}u"))
        row_w.addWidget(btn_w_inc)
        bl.addWidget(QLabel("批量宽度 (u)"))
        bl.addLayout(row_w)

        row_o = QHBoxLayout()
        btn_o_dec = QPushButton("← 左移 0.25u")
        btn_o_inc = QPushButton("右移 0.25u →")
        btn_o_dec.clicked.connect(lambda: self._batch_offset(-MOVE_STEP_U))
        btn_o_inc.clicked.connect(lambda: self._batch_offset(MOVE_STEP_U))
        row_o.addWidget(btn_o_dec)
        row_o.addWidget(QLabel(f"平均: {avg_off:.2f}u"))
        row_o.addWidget(btn_o_inc)
        bl.addWidget(QLabel("独立偏移量 (u)"))
        bl.addLayout(row_o)

        row_ord = QHBoxLayout()
        btn_left = QPushButton("← 向左交换")
        btn_right = QPushButton("向右交换 →")
        btn_left.clicked.connect(lambda: self._batch_order(-1))
        btn_right.clicked.connect(lambda: self._batch_order(1))
        row_ord.addWidget(btn_left)
        row_ord.addWidget(btn_right)
        bl.addWidget(QLabel("行内顺序（← → 键）"))
        bl.addLayout(row_ord)

        row_row = QHBoxLayout()
        btn_up = QPushButton("↑ 上移一行")
        btn_down = QPushButton("↓ 下移一行")
        btn_up.clicked.connect(lambda: self._batch_row(-1))
        btn_down.clicked.connect(lambda: self._batch_row(1))
        row_row.addWidget(btn_up)
        row_row.addWidget(btn_down)
        bl.addWidget(QLabel("上下移动行（↑ ↓ 键）"))
        bl.addLayout(row_row)

        btn_del = QPushButton("删除选中按键")
        btn_del.setObjectName("dangerBtn")
        btn_del.clicked.connect(self._on_delete)
        bl.addWidget(btn_del)
        hint = QLabel("提示：框选 / Ctrl+点击多选；方向键快捷操作")
        hint.setObjectName("hintLabel")
        bl.addWidget(hint)
        self.editor_host.addWidget(batch)

        if len(selected) == 1:
            self._build_detail_panel(selected[0])
        else:
            multi = QLabel(f"已多选 {len(selected)} 个按键\n请只选中一个按键以编辑详细属性")
            multi.setAlignment(Qt.AlignCenter)
            multi.setStyleSheet("color: #888; font-size: 13px; padding: 24px;")
            self.detail_host.addWidget(multi)

        self._building_editor = False

    def _build_detail_panel(self, key) -> None:
        wrap = QWidget()
        wrap_layout = QHBoxLayout(wrap)
        wrap_layout.setContentsMargins(4, 4, 4, 4)
        wrap_layout.setSpacing(24)

        left_box = QGroupBox("基础属性")
        left_form = QFormLayout(left_box)
        left_form.setSpacing(8)

        type_label = QLabel("滚轮" if key.is_encoder else "普通按键")
        type_label.setStyleSheet(
            "color: #2ecc71; font-weight: bold;" if key.is_encoder else "color: #a29bfe; font-weight: bold;"
        )
        left_form.addRow("类型", type_label)

        self.ed_width = FocusWheelDoubleSpinBox()
        self.ed_width.setRange(0.25, 20)
        self.ed_width.setSingleStep(0.25)
        self.ed_width.setDecimals(2)
        self.ed_width.setValue(key.width_u)
        self.ed_width.setFocusPolicy(Qt.StrongFocus)

        self.ed_offset = FocusWheelDoubleSpinBox()
        self.ed_offset.setRange(-20, 20)
        self.ed_offset.setSingleStep(0.25)
        self.ed_offset.setDecimals(2)
        self.ed_offset.setValue(key.offset_x)
        self.ed_offset.setFocusPolicy(Qt.StrongFocus)

        rgb_row = QHBoxLayout()
        self.ed_rgb = FocusWheelSpinBox()
        self.ed_rgb.setRange(0, 9999)
        self.ed_rgb.setFocusPolicy(Qt.StrongFocus)
        self.ed_no_led = QCheckBox(NO_LED_LABEL)
        self.ed_no_led.setToolTip("勾选表示该键不参与灯光索引")
        if key.rgb_index == NO_LED:
            self.ed_no_led.setChecked(True)
            self.ed_rgb.setEnabled(False)
            self.ed_rgb.setValue(0)
        else:
            self.ed_no_led.setChecked(False)
            self.ed_rgb.setEnabled(True)
            self.ed_rgb.setValue(key.rgb_index)
        rgb_row.addWidget(self.ed_rgb, 1)
        rgb_row.addWidget(self.ed_no_led)
        rgb_wrap = QWidget()
        rgb_wrap.setLayout(rgb_row)

        self.ed_col = FocusWheelSpinBox()
        self.ed_col.setRange(0, 255)
        self.ed_col.setValue(key.matrix_col)
        self.ed_col.setFocusPolicy(Qt.StrongFocus)

        self.ed_mrow = FocusWheelSpinBox()
        self.ed_mrow.setRange(0, 255)
        self.ed_mrow.setValue(key.matrix_row)
        self.ed_mrow.setFocusPolicy(Qt.StrongFocus)

        left_form.addRow("宽度 (u)", self.ed_width)
        left_form.addRow("偏移量 (u)", self.ed_offset)
        left_form.addRow("RGB 索引", rgb_wrap)
        left_form.addRow("C 线 (列)", self.ed_col)
        left_form.addRow("R 线 (行)", self.ed_mrow)

        right_box = QGroupBox("滚轮四层功能" if key.is_encoder else "四层按键功能")
        right_layout = QVBoxLayout(right_box)
        right_layout.setSpacing(8)

        completer = QCompleter(KEYCODE_PRESETS)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        self.ed_layers = []
        self.ed_encoder_layers = []  # 4 layers × 3 edits

        if key.is_encoder:
            key.ensure_encoder_layers()
            for layer_i in range(4):
                layer_box = QGroupBox(f"Layer {layer_i}")
                layer_form = QFormLayout(layer_box)
                layer_form.setSpacing(4)
                layer_edits = []
                for func_i, label in enumerate(ENCODER_FUNC_LABELS):
                    edit = QLineEdit(key.encoder_layers[layer_i][func_i])
                    edit.setCompleter(completer)
                    layer_form.addRow(label, edit)
                    layer_edits.append(edit)
                self.ed_encoder_layers.append(layer_edits)
                right_layout.addWidget(layer_box)
        else:
            form = QFormLayout()
            form.setSpacing(8)
            for i in range(4):
                edit = QLineEdit(key.layers[i])
                edit.setCompleter(completer)
                form.addRow(f"Layer {i}", edit)
                self.ed_layers.append(edit)
            right_layout.addLayout(form)

        wrap_layout.addWidget(left_box, 1)
        wrap_layout.addWidget(right_box, 2)
        self.detail_host.addWidget(wrap)

        self.ed_width.valueChanged.connect(self._on_single_change)
        self.ed_offset.valueChanged.connect(self._on_single_change)
        self.ed_rgb.valueChanged.connect(self._on_single_change)
        self.ed_no_led.toggled.connect(self._on_no_led_toggled)
        self.ed_col.valueChanged.connect(self._on_single_change)
        self.ed_mrow.valueChanged.connect(self._on_single_change)
        for edit in self.ed_layers:
            edit.textChanged.connect(self._on_single_change)
        for layer_edits in self.ed_encoder_layers:
            for edit in layer_edits:
                edit.textChanged.connect(self._on_single_change)

    def _on_no_led_toggled(self, checked: bool) -> None:
        self.ed_rgb.setEnabled(not checked)
        self._on_single_change()

    def _on_canvas_selection(self) -> None:
        self.doc.selected_ids = self.canvas.selected_ids
        self.refresh_canvas()
        self.refresh_editor()

    def _on_layer(self, layer_id: int) -> None:
        self.doc.active_layer = layer_id
        self.refresh_canvas()

    def _on_preset(self) -> None:
        self.doc.load_preset()
        self.refresh_all()

    def _on_add(self, key_type: str = KEY_TYPE_KEY) -> None:
        if not self.doc.selected_ids:
            tip = (
                "请先选中一个按键，以便在其右侧添加新滚轮"
                if key_type == KEY_TYPE_ENCODER
                else "请先选中一个按键，以便在其右侧添加新按键"
            )
            QMessageBox.information(self, "提示", tip)
            return
        self.doc.add_key_after_selected(key_type)
        self.refresh_all()

    def _on_delete(self) -> None:
        if not self.doc.selected_ids:
            QMessageBox.information(self, "提示", "请先选中要删除的按键")
            return
        self.doc.delete_selected()
        self.refresh_all()

    def _batch_width(self, delta: float) -> None:
        if not self.doc.batch_change_width(delta):
            QMessageBox.information(self, "提示", "请先选中按键")
            return
        self.refresh_all()

    def _batch_offset(self, delta: float) -> None:
        if not self.doc.batch_change_offset(delta):
            QMessageBox.information(self, "提示", "请先选中按键")
            return
        self.refresh_all()

    def _batch_order(self, delta: int, silent: bool = False) -> None:
        if not self.doc.batch_move_order(delta):
            if not silent:
                QMessageBox.information(self, "提示", "请先选中按键")
            return
        self.refresh_all()

    def _batch_row(self, delta: int, silent: bool = False) -> None:
        if not self.doc.batch_move_row(delta):
            if not silent:
                QMessageBox.information(self, "提示", "请先选中按键")
            return
        self.refresh_all()

    def _on_single_change(self) -> None:
        if self._building_editor:
            return
        selected = self.doc.selected_keys()
        if len(selected) != 1:
            return
        key = selected[0]
        key.width_u = round(self.ed_width.value() * 100) / 100
        key.offset_x = round(self.ed_offset.value() * 100) / 100
        if self.ed_no_led.isChecked():
            key.rgb_index = NO_LED
        else:
            key.rgb_index = self.ed_rgb.value()
        key.matrix_col = self.ed_col.value()
        key.matrix_row = self.ed_mrow.value()
        if key.is_encoder:
            key.ensure_encoder_layers()
            for layer_i, layer_edits in enumerate(self.ed_encoder_layers):
                for func_i, edit in enumerate(layer_edits):
                    key.encoder_layers[layer_i][func_i] = edit.text()
        else:
            while len(key.layers) < 4:
                key.layers.append("KC_NO")
            for i, edit in enumerate(self.ed_layers):
                key.layers[i] = edit.text()
        self.refresh_canvas()

    def _apply_hw_config(self) -> None:
        if self._building_hw:
            return
        hw = self.doc.hw
        hw.usb_device_name = self.hw_usb.text()
        hw.pid = self.hw_pid.text()
        hw.vid = self.hw_vid.text()
        hw.version = self.hw_version.text()
        hw.bluetooth_names = [self.hw_bt[i].text() for i in range(3)]
        hw.has_mode_switch = bool(self.hw_mode.currentData())
        hw.row_count = self.hw_rows.value()
        hw.col_count = self.hw_cols.value()
        hw.rgb_led_count = self.hw_rgb.value()
        hw.side_led_enabled = bool(self.hw_side_en.currentData())
        hw.side_led_count = self.hw_side_count.value() if hw.side_led_enabled else 0
        hw.logo_led_enabled = bool(self.hw_logo_en.currentData())
        hw.logo_led_count = self.hw_logo_count.value() if hw.logo_led_enabled else 0
        hw.has_screen = bool(self.hw_screen.currentData())
        hw.max_brightness = self.hw_max_bri.value()
        hw.brightness_levels = self.hw_bri_lv.value()
        hw.speed_levels = self.hw_spd_lv.value()

    def _on_reassign(self) -> None:
        reassign_rgb_indices(self.doc.keys)
        self.refresh_all()
        QMessageBox.information(
            self, "提示", f"已重新分配 {len(self.doc.keys)} 个按键的灯光索引，按行/列顺序。"
        )

    def _on_export(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "导出 JSON", "keyboard_config.json", "JSON Files (*.json)"
        )
        if not path:
            return
        try:
            self.doc.export_json(path)
            QMessageBox.information(self, "提示", f"已导出到：\n{path}")
        except OSError as exc:
            QMessageBox.critical(self, "导出失败", str(exc))

    def _on_import(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "导入 JSON", "", "JSON Files (*.json)")
        if not path:
            return
        try:
            count, has_dup = self.doc.import_json(path)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            QMessageBox.critical(self, "导入失败", str(exc))
            return

        if has_dup:
            reply = QMessageBox.question(
                self,
                "重复索引",
                "检测到导入的灯光索引有重复，是否自动重新分配所有索引（按行/列顺序）？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if reply == QMessageBox.Yes:
                reassign_rgb_indices(self.doc.keys)

        self.refresh_all()
        QMessageBox.information(self, "提示", f"导入成功！共加载 {count} 个按键")
