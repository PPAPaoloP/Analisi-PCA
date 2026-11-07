"""
/**
 *  @file       control_column.py
 *  @brief      Colonna laterale (Destra 30%) con bottoni operativi e slide panel.
 *
 *  @details
 *              Permette l'avvio della lettura file (I/O file-system) e
 *              espone gli slider configuratori dei loadings PCA per
 *              pulizia grafico, varianze e opzioni avanzate scikit-learn.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QGroupBox, QLabel,
                             QSlider, QHBoxLayout)
from PyQt6.QtCore import Qt

import app_config as cfg

class ControlColumn(QWidget):
    """Pannello di destra. Controlla I/O Dati Excel e l'engine analitico PCA."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Larghezza governata dinamicamente proporzionale tramite Main Window
        #self.setFixedWidth(int(cfg.WINDOW_WIDTH * cfg.RIGHT_COLUMN_WIDTH_RATIO))
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 1. GROUP BOTTONI DI DATA I/O (Azioni Primarie)
        io_group = QGroupBox("Operazioni principali")
        io_layout = QVBoxLayout()
        io_layout.setSpacing(10)
        
        self.btn_load = QPushButton("LOAD FILE EXCEL / CSV")
        self.btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_load.setMinimumHeight(40) # Altezze identiche per i pulsanti
        self.btn_load.setStyleSheet(f"background-color: {cfg.COLOR_BTN_BACKGROUND_HOVER};")
        
        self.btn_save_pca = QPushButton("ESPORTA PCA DATA")
        self.btn_save_pca.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save_pca.setMinimumHeight(40) # Altezze identiche per i pulsanti
        
        io_layout.addWidget(self.btn_load)
        io_layout.addWidget(self.btn_save_pca)
        io_group.setLayout(io_layout)
        
        # 2. GROUP STRUMENTI DI CORRELAZIONE E REGOLAZIONE PCA 
        # (Futura espansione slider e parametri per i loading)
        pca_group = QGroupBox("Regolazioni e filtri (Data Science)")
        pca_layout = QVBoxLayout()
        
        # Uno slide "fantoccio" per adesso: Moltiplicatore Grandezza Frecce Loadings.
        pca_layout.addWidget(QLabel("Magnitudo Vettori Loadings [1x - 10x]:"))
        scale_slider = QSlider(Qt.Orientation.Horizontal)
        scale_slider.setRange(10, 100)
        scale_slider.setValue(35)
        
        slider_val_lbl = QLabel("x3.5")
        slider_val_lbl.setStyleSheet(f"color: {cfg.COLOR_ACCENT_BLUE}; font-weight: bold;")
        
        sl_row = QHBoxLayout()
        sl_row.addWidget(scale_slider)
        sl_row.addWidget(slider_val_lbl)
        
        pca_layout.addLayout(sl_row)
        pca_layout.addStretch(1) # Spinge lo slide compatto verso l'alto
        pca_group.setLayout(pca_layout)
        
        # Costruzione master e molla verticale per i restanti bottom frame vuoti.
        main_layout.addWidget(io_group)
        main_layout.addWidget(pca_group)
        main_layout.addStretch(1)
        
        self.setLayout(main_layout)