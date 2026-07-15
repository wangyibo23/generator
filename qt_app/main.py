# -*- coding: utf-8 -*-
"""键盘配置工具 - PyQt5 入口

运行：
    python -m qt_app.main
或：
    python qt_app/main.py
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    # 允许直接 python qt_app/main.py 运行
    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        print("[ERROR] 缺少 PyQt5，请执行：pip install PyQt5", file=sys.stderr)
        return 1

    from qt_app.constants import APP_STYLESHEET
    from qt_app.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLESHEET)
    window = MainWindow()
    window.showFullScreen()
    from PyQt5.QtCore import QTimer

    QTimer.singleShot(100, window._apply_splitter_ratio)
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
