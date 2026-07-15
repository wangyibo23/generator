# -*- coding: utf-8 -*-
"""键盘画布与按键控件"""

from __future__ import annotations

from typing import Optional, Set

from PyQt5.QtCore import QPoint, QRect, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QMouseEvent, QPainter, QPen, QResizeEvent, QWheelEvent
from PyQt5.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QLabel,
    QSpinBox,
    QStyle,
    QStyleOption,
    QVBoxLayout,
    QWidget,
)

from .constants import KEY_TYPE_ENCODER, NO_LED, NO_LED_LABEL, U_TO_PX, fit_u_to_px
from .models import Key, calculate_key_positions


class FocusWheelSpinBox(QSpinBox):
    """仅在获得焦点后才响应滚轮，避免悬停误改。"""

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class FocusWheelDoubleSpinBox(QDoubleSpinBox):
    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class FocusWheelComboBox(QComboBox):
    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class KeyWidget(QFrame):
    clicked = pyqtSignal(str, object)  # key_id, modifiers

    def __init__(self, key: Key, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.key_id = key.id
        self._is_encoder = key.is_encoder
        self._selected = False
        self.setObjectName("keyCap")
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(1)
        layout.setAlignment(Qt.AlignCenter)

        self.func_label = QLabel()
        self.func_label.setAlignment(Qt.AlignCenter)
        self.func_label.setWordWrap(True)
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.func_label.setFont(font)

        self.meta_label = QLabel()
        self.meta_label.setAlignment(Qt.AlignCenter)
        meta_font = QFont()
        meta_font.setPointSize(6)
        self.meta_label.setFont(meta_font)
        self.meta_label.setStyleSheet("color: #aaa;")

        layout.addWidget(self.func_label)
        layout.addWidget(self.meta_label)
        self.set_selected(False)

    def update_content(self, key: Key, active_layer: int) -> None:
        self._is_encoder = key.is_encoder
        rgb_text = NO_LED_LABEL if key.rgb_index == NO_LED else f"RGB:{key.rgb_index}"
        cr_text = f"C:{key.matrix_col}/R:{key.matrix_row}"
        if key.is_encoder:
            press, left, right = key.encoder_funcs(active_layer)
            self.func_label.setText(f"滚轮 L{active_layer}\n{press}")
            self.meta_label.setText(f"←{left} →{right}\n{rgb_text}\n{cr_text}")
        else:
            func = key.layers[active_layer] if active_layer < len(key.layers) else "???"
            self.func_label.setText(func)
            self.meta_label.setText(f"{rgb_text}\n{cr_text}")
        self.set_selected(self._selected)

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        if self._is_encoder:
            radius = "999px"
            base_bg = "#1a332a" if not selected else "#2c4434"
            border = "2px solid #f1c40f" if selected else "2px solid #2ecc71"
            hover = "#244438"
        else:
            radius = "8px"
            base_bg = "#2c2c44" if selected else "#1f1f2f"
            border = "2px solid #f1c40f" if selected else "1px solid #5a5a7a"
            hover = "#2e2e48"

        if selected:
            self.setStyleSheet(
                f"""
                QFrame#keyCap {{
                    background: {base_bg};
                    border: {border};
                    border-radius: {radius};
                }}
                """
            )
        else:
            self.setStyleSheet(
                f"""
                QFrame#keyCap {{
                    background: {base_bg};
                    border: {border};
                    border-radius: {radius};
                }}
                QFrame#keyCap:hover {{
                    background: {hover};
                }}
                """
            )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.key_id, event.modifiers())
        super().mousePressEvent(event)


class KeyboardCanvas(QWidget):
    selection_changed = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(800, 400)
        self.setStyleSheet(
            """
            KeyboardCanvas {
                background: #2b2b2b;
                border-radius: 20px;
                border: 2px solid #444;
            }
            """
        )
        self._keys: list = []
        self._selected_ids: Set[str] = set()
        self._active_layer = 0
        self._widgets: dict = {}
        self._scale = float(U_TO_PX)
        self._viewport_width = 0
        self._rebuild_timer = QTimer(self)
        self._rebuild_timer.setSingleShot(True)
        self._rebuild_timer.timeout.connect(self._rebuild)
        self.setMouseTracking(True)

        # 框选状态
        self._marquee_active = False
        self._marquee_origin = QPoint()
        self._marquee_rect = QRect()
        self._marquee_additive = False
        self._marquee_base: Set[str] = set()
        self._marquee_moved = False

    def set_viewport_width(self, width: int) -> None:
        """由外层滚动区传入可视宽度，用于按 21 键/行适配比例。"""
        if width <= 0:
            return
        if abs(width - self._viewport_width) < 2:
            return
        self._viewport_width = width
        new_scale = fit_u_to_px(float(width))
        if abs(new_scale - self._scale) > 0.01:
            self._scale = new_scale
            self._rebuild_timer.start(50)

    def set_data(self, keys: list, selected_ids: Set[str], active_layer: int) -> None:
        self._keys = keys
        self._selected_ids = set(selected_ids)
        self._active_layer = active_layer
        self._rebuild()

    def _rebuild(self) -> None:
        for w in self._widgets.values():
            w.setParent(None)
            w.deleteLater()
        self._widgets.clear()

        if self._viewport_width > 0:
            self._scale = fit_u_to_px(float(self._viewport_width))

        if not self._keys:
            self.setMinimumSize(max(800, self._viewport_width or 800), 400)
            self.update()
            return

        positions = calculate_key_positions(self._keys, self._scale)
        padding = 20
        max_right = 0.0
        max_bottom = 0.0

        for key in self._keys:
            pos = positions.get(key.id)
            if not pos:
                continue
            widget = KeyWidget(key, self)
            widget.update_content(key, self._active_layer)
            widget.set_selected(key.id in self._selected_ids)
            w = max(20, int(pos["width"]))
            h = max(20, int(pos["height"]))
            if key.key_type == KEY_TYPE_ENCODER:
                side = min(w, h)
                widget.setGeometry(
                    int(pos["x"] + padding + (w - side) / 2),
                    int(pos["y"] + padding + (h - side) / 2),
                    side,
                    side,
                )
            else:
                widget.setGeometry(
                    int(pos["x"] + padding),
                    int(pos["y"] + padding),
                    w,
                    h,
                )
            widget.clicked.connect(self._on_key_clicked)
            widget.show()
            self._widgets[key.id] = widget
            max_right = max(max_right, pos["x"] + pos["width"])
            max_bottom = max(max_bottom, pos["y"] + pos["height"])

        min_w = max(int(self._viewport_width or 800), int(max_right + padding * 2 + 8))
        self.setMinimumSize(min_w, max(300, int(max_bottom + padding * 2 + 40)))
        self.update()

    def _on_key_clicked(self, key_id: str, modifiers) -> None:
        if self._marquee_active:
            return
        ctrl = bool(modifiers & (Qt.ControlModifier | Qt.MetaModifier))
        if ctrl:
            if key_id in self._selected_ids:
                self._selected_ids.discard(key_id)
            else:
                self._selected_ids.add(key_id)
        else:
            self._selected_ids = {key_id}
        self.selection_changed.emit()

    @property
    def selected_ids(self) -> Set[str]:
        return set(self._selected_ids)

    def _key_widget_at(self, pos: QPoint) -> Optional[KeyWidget]:
        w = self.childAt(pos)
        while w is not None and w is not self:
            if isinstance(w, KeyWidget):
                return w
            w = w.parentWidget()
        return None

    def _sync_widget_selection(self) -> None:
        for kid, widget in self._widgets.items():
            widget.set_selected(kid in self._selected_ids)

    def _apply_marquee_hit(self) -> None:
        hit: Set[str] = set()
        if self._marquee_rect.width() >= 3 and self._marquee_rect.height() >= 3:
            for kid, widget in self._widgets.items():
                if self._marquee_rect.intersects(widget.geometry()):
                    hit.add(kid)
        if self._marquee_additive:
            self._selected_ids = set(self._marquee_base) | hit
        else:
            self._selected_ids = hit
        self._sync_widget_selection()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self._key_widget_at(event.pos()) is None:
            self._marquee_active = True
            self._marquee_moved = False
            self._marquee_origin = event.pos()
            self._marquee_rect = QRect(self._marquee_origin, self._marquee_origin)
            self._marquee_additive = bool(event.modifiers() & (Qt.ControlModifier | Qt.MetaModifier))
            self._marquee_base = set(self._selected_ids) if self._marquee_additive else set()
            self.grabMouse()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._marquee_active:
            self._marquee_rect = QRect(self._marquee_origin, event.pos()).normalized()
            if (
                abs(event.pos().x() - self._marquee_origin.x()) > 3
                or abs(event.pos().y() - self._marquee_origin.y()) > 3
            ):
                self._marquee_moved = True
            if self._marquee_moved:
                self._apply_marquee_hit()
            self.update()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._marquee_active and event.button() == Qt.LeftButton:
            self._marquee_active = False
            self.releaseMouse()
            if self._marquee_moved:
                self._apply_marquee_hit()
                self.selection_changed.emit()
            self._marquee_rect = QRect()
            self._marquee_moved = False
            self.update()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def paintEvent(self, event) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        if self._marquee_active and self._marquee_moved and not self._marquee_rect.isNull():
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(QPen(QColor(108, 92, 231), 1, Qt.DashLine))
            painter.setBrush(QColor(108, 92, 231, 50))
            painter.drawRect(self._marquee_rect.adjusted(0, 0, -1, -1))

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        if self._viewport_width <= 0 and self.width() > 100:
            self.set_viewport_width(self.width())
