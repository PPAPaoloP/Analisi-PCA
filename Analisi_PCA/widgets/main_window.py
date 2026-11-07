"""
/**
 *  @file       main_window.py
 *  @brief      Finestra principale / Struttura Master (UI).
 *
 *  @details
 *              La shell primaria (Main Window) che accoglie e ordina gli altri widgets:
 *              TopBanner in alto, layout orizzontale in basso con TAB grafico e controlli destri.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel)
from PyQt6.QtCore import Qt

import app_config as cfg
from widgets.top_banner import TopBanner
from widgets.main_tab_panel import MainTabPanel
from widgets.control_column import ControlColumn

class MainWindow(QMainWindow):
    """L'intelaiatura principale. Configura dimensioni fisse/massime e stili ereditati."""

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(cfg.APP_NAME)
        # 1920x1080 da specifica. Fissiamo per dare il 'look' tipico delle dashboard su hardware
        self.resize(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
        self.setStyleSheet(cfg.GLOBAL_STYLE)
        
        self._build_main_ui()

    def _build_main_ui(self):
        """Struttura logica a cascata."""
        
        # Central widget obbligatorio in una QMainWindow
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Layout principale Verticale 
        master_layout = QVBoxLayout(central_widget)
        master_layout.setContentsMargins(10, 10, 10, 10)
        master_layout.setSpacing(10)
        
        # --- BLOCCO HEADER SUPERIORE (il famoso "10%") ---
        self.top_banner = TopBanner(self)
        master_layout.addWidget(self.top_banner)
        
        # --- BLOCCO CORPO APP PRINCIPALE: SPLIT L/R (70% - 30%) ---
        body_layout = QHBoxLayout()
        body_layout.setSpacing(10)
        
        # 1. Zona Tab a Sx: il Canvas di Scikit-learn Matplotlib grafico a video:
        self.tab_panel = MainTabPanel(self)
        
        # 2. Controlli I/O Operazionali e di Parametrizzazione. 
        self.right_col = ControlColumn(self)
        
        # 7 per occupare proporzione 7/10 del master frame interno, senza rigidezze 
        body_layout.addWidget(self.tab_panel, 88)  
        body_layout.addWidget(self.right_col, 12) 
        
        # Innesta questo blocco espandibile di basso orizzontale in blocco master_layout! 
        master_layout.addLayout(body_layout, 1)