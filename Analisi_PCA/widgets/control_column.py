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
                             QSlider, QHBoxLayout, QCheckBox, QComboBox)
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
        
        self.btn_load = QPushButton("CARICA FILE EXCEL / CSV")
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
        pca_group = QGroupBox("Regolazioni PCA e filtri")
        pca_layout = QVBoxLayout()
        pca_layout.setSpacing(10)
        
        # A. Preprocessing Checkbox
        self.chk_std = QCheckBox("Standardizzazione Variabili")
        self.chk_std.setChecked(True)
        self.chk_std.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # B. Selezione Dimensione/Assi (Il Combobox mancante)
        combo_lay = QHBoxLayout()
        lbl_assi = QLabel("Piano Assi:")
        lbl_assi.setStyleSheet(f"color: {cfg.COLOR_TEXT_MAIN};")
        
        self.combo_axes = QComboBox()
        self.combo_axes.addItems(["PC1 vs PC2", "PC1 vs PC3", "PC2 vs PC3"])
        self.combo_axes.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_axes.setStyleSheet(f"background-color: {cfg.COLOR_BACKGROUND_APP}; color: {cfg.COLOR_ACCENT_BLUE}; padding: 3px;")
        
        combo_lay.addWidget(lbl_assi)
        combo_lay.addWidget(self.combo_axes)

        # C. Slider: Filtraggio Frecce (Threshold) + Valore Dinamico
        sl_thr_lay = QHBoxLayout()
        self.lbl_thr = QLabel("Visibilità Frecce [Min]:")
        self.lbl_thr.setStyleSheet(f"color: {cfg.COLOR_TEXT_DIMMED}; font-size: 10pt;")
        self.val_thr = QLabel("0.5") 
        self.val_thr.setStyleSheet(f"color: {cfg.COLOR_ACCENT_BLUE}; font-weight: bold;")
        sl_thr_lay.addWidget(self.lbl_thr)
        sl_thr_lay.addStretch(1)
        sl_thr_lay.addWidget(self.val_thr)

        self.sl_thr = QSlider(Qt.Orientation.Horizontal)
        self.sl_thr.setRange(0, 50)
        self.sl_thr.setValue(5)
        
        # D. Slider: Multiplicatore Zoom (Magnitudine) + Valore Dinamico
        sl_scl_lay = QHBoxLayout()
        self.lbl_scl = QLabel("Moltiplicatore Vettori:")
        self.lbl_scl.setStyleSheet(f"color: {cfg.COLOR_TEXT_DIMMED}; font-size: 10pt;")
        self.val_scl = QLabel("x 2.5")
        self.val_scl.setStyleSheet(f"color: {cfg.COLOR_ACCENT_BLUE}; font-weight: bold;")
        sl_scl_lay.addWidget(self.lbl_scl)
        sl_scl_lay.addStretch(1)
        sl_scl_lay.addWidget(self.val_scl)
        
        self.sl_scl = QSlider(Qt.Orientation.Horizontal)
        self.sl_scl.setRange(10, 150)
        self.sl_scl.setValue(25)
        
        # Incastro widget nel layout "Filtri"
        pca_layout.addWidget(self.chk_std)
        pca_layout.addSpacing(4)
        pca_layout.addLayout(combo_lay)
        pca_layout.addSpacing(8)
        pca_layout.addLayout(sl_thr_lay)
        pca_layout.addWidget(self.sl_thr)
        pca_layout.addLayout(sl_scl_lay)
        pca_layout.addWidget(self.sl_scl)
        
        pca_group.setLayout(pca_layout)
        
        main_layout.addWidget(io_group)
        main_layout.addWidget(pca_group)
        main_layout.addStretch(1)
        
        self.setLayout(main_layout)

        # Avvio della cablatura UI locale (Aggiorna testi)
        self.sl_thr.valueChanged.connect(self._update_slider_texts)
        self.sl_scl.valueChanged.connect(self._update_slider_texts)

    def _update_slider_texts(self):
        """Reagisce internamente ai cambi slider restituendo formato ingegneristico sulle mini-labels laterali."""
        v_thr = self.sl_thr.value() / 10.0
        v_scl = self.sl_scl.value() / 10.0
        self.val_thr.setText(f"{v_thr:.1f}")
        self.val_scl.setText(f"x {v_scl:.1f}")