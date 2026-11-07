"""
/**
 *  @file       top_banner.py
 *  @brief      Barra superiore (Top Banner) dell'applicazione.
 *
 *  @details
 *              Questo widget costituisce il 10% dell'header della schermata
 *              principale. Comprende la casella dei suggerimenti/stati a sx, 
 *              il titolo del software in centro e il running-time combinato a 
 *              metadati (Versione + pulsante modale '?') sulla dx.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import datetime
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget)

import app_config as cfg
from widgets.about_dialog import AboutDialog


class TopBanner(QWidget):
    """Fascia dell'header globale con orologio realtime, titolo e pannello hint."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._start_clock()

    def _build_ui(self):
        """Costruisce la testata con una struttura 80% (SX) / 20% (DX)."""
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)
        
        # ==========================================
        # COLONNA SINISTRA (80% Spazio Globale)
        # ==========================================
        left_col = QVBoxLayout()
        
        # -- Titolo
        title_lbl = QLabel(cfg.APP_NAME)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Consolas", 24, QFont.Weight.Bold)
        title_lbl.setFont(title_font)
        title_lbl.setStyleSheet(f"color: {cfg.COLOR_ACCENT_GREEN};")
        
        # -- Status / Hint Textbox (espanso sotto il titolo)
        self.status_box = QLabel()
        self.status_box.setWordWrap(True)
        # Altezza stimata fissa per le 2 righe, espandendosi sulla colonna intera (100% dell'80%)
        self.status_box.setMinimumHeight(44)
        self.status_box.setMaximumHeight(54)
        self.status_box.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.status_box.setStyleSheet(
            f"border: 1px solid {cfg.COLOR_BORDER_NORMAL}; border-radius: 4px; padding: 4px; "
            f"color: {cfg.COLOR_ACCENT_BLUE}; background-color: {cfg.COLOR_BACKGROUND_BOX}; "
            f"font-size: 10pt;"
        )
        
        clean_desc = cfg.APP_DESCRIPTION.replace("\n", " ")
        self.status_box.setText(clean_desc)
        
        left_col.addWidget(title_lbl)
        left_col.addWidget(self.status_box)
        
        # ==========================================
        # COLONNA DESTRA (20% Spazio Globale)
        # ==========================================
        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        right_col.setSpacing(6)
        
        # -- Orologio / Data
        self.clock_lbl = QLabel()
        self.clock_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.clock_lbl.setStyleSheet(f"color: {cfg.COLOR_TEXT_MAIN}; font-size: 11pt; font-weight: bold;")
        
        # -- Layout riga Versione + About '?'
        ver_btn_row = QHBoxLayout()
        ver_btn_row.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        ver_lbl = QLabel(cfg.APP_VERSION)
        ver_lbl.setStyleSheet(f"color: {cfg.COLOR_TEXT_DIMMED}; font-size: 10pt; font-weight: bold;")
        ver_lbl.setContentsMargins(0, 0, 10, 0)
        
        self.btn_about = QPushButton("?")
        self.btn_about.setFixedSize(30, 30)
        font_about = QFont("Consolas", 12, QFont.Weight.Bold)
        self.btn_about.setFont(font_about)
        self.btn_about.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_about.setToolTip("Mostra le informazioni dell'Applicazione")
        self.btn_about.clicked.connect(self._show_about)
        
        ver_btn_row.addWidget(ver_lbl)
        ver_btn_row.addWidget(self.btn_about)
        
        right_col.addWidget(self.clock_lbl)
        right_col.addLayout(ver_btn_row)
        
        # Assegnazione proporzioni: sx factor 4, dx factor 1 (4/5 vs 1/5 => 80/20)
        main_layout.addLayout(left_col, 4)
        main_layout.addLayout(right_col, 1)
        
        self.setLayout(main_layout)

    def _start_clock(self):
        """Inizializza un Timer virtuale a 1 Hz per aggiornare i secondi on-screen."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        """Preleva orario usando vettore stringhe per formato '07 Novembre 2026 - 15:30:10'."""
        now = datetime.datetime.now()
        mesi_it = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                   "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
                  ] 
        nome_mese = mesi_it[now.month - 1]
        
        # %d preserva lo Zero iniziale (01, 02.. 07.. etc). 
        time_str = now.strftime(f"%d {nome_mese} %Y - %H:%M:%S")
        self.clock_lbl.setText(time_str)

    def _show_about(self):
        """Crea ed esegue modalmente la finestra in merito."""
        dialog = AboutDialog(self)
        dialog.exec()
        
    def set_status_text(self, text: str):
        """Metodo per aggiornare la status box e mantenere l'allineamento a sinistra-alto."""
        self.status_box.setText(text)
        self.status_box.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)