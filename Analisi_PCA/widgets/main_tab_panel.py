"""
/**
 *  @file       main_tab_panel.py
 *  @brief      Collettore della logica a Schede per i Canvas / Plot PCA.
 *
 *  @details
 *              Genera un controllo multi-schermata QTabWidget formattato con i
 *              fogli di stile coerenti alla top-application, destinando lo
 *              spazio alle figure 2D generate da matplotlib del rispettivo tab.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

from PyQt6.QtWidgets import (QTabWidget, QWidget, QVBoxLayout, QLabel)
from PyQt6.QtCore import Qt

import app_config as cfg

class MainTabPanel(QTabWidget):
    """Pannello multi-vista integrato contenitore dell'Orizzonte suolo attivo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_dark_style()
        self._build_tabs()

    def _apply_dark_style(self):
        """Colora con palette coerente i flagellini dei Tabs base e gli sfondi dei content widget."""
        self.setStyleSheet(
            f"QTabWidget::pane {{ border: 1px solid {cfg.COLOR_BORDER_NORMAL}; border-radius: 4px; background: {cfg.COLOR_BACKGROUND_APP}; }}"
            f"QTabBar::tab {{ background: {cfg.COLOR_BACKGROUND_BOX}; color: {cfg.COLOR_TEXT_DIMMED}; "
            f"                border: 1px solid {cfg.COLOR_BORDER_NORMAL}; border-bottom: none; "
            f"                padding: 10px; min-width: 140px; font-weight: bold; font-size: 11pt; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px; }}"
            f"QTabBar::tab:selected {{ background: {cfg.COLOR_BORDER_NORMAL}; color: {cfg.COLOR_ACCENT_GREEN}; }}"
            f"QTabBar::tab:hover:!selected {{ background: {cfg.COLOR_BACKGROUND_APP}; color: {cfg.COLOR_TEXT_MAIN}; }}"
        )

    def _build_tabs(self):
        """Crea i Widget foglio bianco che compongono i moduli delle tab."""
        # 1. TAB A -> Carica come costante stringa
        tab_a_widget = QWidget()
        tab_a_layout = QVBoxLayout()
        
        info_lbl = QLabel(f"Qui posizioneremo il MATPLOTLIB Canvas 2D BiPlot interattivo PCA.\nDataset target relativo alla TAB: {cfg.TAB_NAME_SOIL_A}.")
        info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tab_a_layout.addWidget(info_lbl)
        tab_a_widget.setLayout(tab_a_layout)
        
        self.addTab(tab_a_widget, cfg.TAB_NAME_SOIL_A)