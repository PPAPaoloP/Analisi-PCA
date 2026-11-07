"""
/**
 *  @file       about_dialog.py
 *  @brief      Finestra di dialogo modale con le informazioni sull'applicazione (About).
 *
 *  @details
 *              Visualizza nome applicazione, versione, data di rilascio, autore,
 *              descrizione funzionale, versioni del runtime (Python/PyQt6) e 
 *              nota di copyright, con pulsante 'OK' per la chiusura.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import sys
from PyQt6.QtCore import Qt, PYQT_VERSION_STR
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

import app_config as cfg


class AboutDialog(QDialog):
    """Finestra modale 'About' conforme allo stile grafico dell'applicazione."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Informazioni su {cfg.APP_NAME}")
        self.setModal(True)
        self.setFixedSize(540, 340)

        # Applica bordo e sfondo coerenti col tema scuro
        self.setStyleSheet(
            cfg.GLOBAL_STYLE
            + f"""
            QDialog {{
                background-color: {cfg.COLOR_BACKGROUND_BOX};
                border: 1px solid {cfg.COLOR_ACCENT_GREEN};
            }}
            """
        )

        self._build_ui()

    def _build_ui(self):
        """Costruisce il layout interno della finestra About."""
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        # Titolo applicazione in verde smeraldo
        title_lbl = QLabel(cfg.APP_NAME)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Consolas", 18, QFont.Weight.Bold)
        title_lbl.setFont(title_font)
        title_lbl.setStyleSheet(f"color: {cfg.COLOR_ACCENT_GREEN}; background: transparent;")
        layout.addWidget(title_lbl)

        # Versione e data di rilascio
        ver_lbl = QLabel(f"{cfg.APP_VERSION}   —   Data Rilascio: {cfg.APP_DATE}")
        ver_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver_lbl.setStyleSheet(f"color: {cfg.COLOR_ACCENT_BLUE}; font-weight: bold; background: transparent;")
        layout.addWidget(ver_lbl)

        # Linea separatrice orizzontale
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {cfg.COLOR_BORDER_NORMAL};")
        layout.addWidget(sep)

        # Descrizione sintetica del software
        desc_lbl = QLabel(cfg.APP_DESCRIPTION)
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("background: transparent;")
        layout.addWidget(desc_lbl)

        # Metadati tecnici: Autore e Runtime
        py_ver = sys.version.split()[0]
        info_text = (
            f"Author  : {cfg.APP_AUTHOR}\n"
            f"Runtime : Python {py_ver} | PyQt6 {PYQT_VERSION_STR}"
        )
        info_lbl = QLabel(info_text)
        info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_lbl.setStyleSheet(f"color: {cfg.COLOR_TEXT_MAIN}; font-size: 10pt; background: transparent;")
        layout.addWidget(info_lbl)

        # Copyright in basso attenuato
        copy_lbl = QLabel(cfg.APP_COPYRIGHT)
        copy_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copy_lbl.setStyleSheet(f"color: {cfg.COLOR_TEXT_DIMMED}; font-size: 8.5pt; background: transparent;")
        layout.addWidget(copy_lbl)

        layout.addStretch(1)

        # Pulsante OK centrato per chiudere la finestra
        btn_row = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.setFixedWidth(120)
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.clicked.connect(self.accept)

        btn_row.addStretch(1)
        btn_row.addWidget(ok_btn)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

        self.setLayout(layout)