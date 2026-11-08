"""
/**
 *  @file       main_tab_panel.py
 *  @brief      Collettore della logica a Schede per i Canvas / Plot PCA.
 *
 *  @details
 *              Implementa un ambiente MDI (Multiple Document Interface) Tab-Based
 *              simile a un Browser. Ogni scheda ospita e trattiene (istanziandola 
 *              nel backend proprio) una DataHandler Indipendente (il database PCATabNode).
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

from PyQt6.QtWidgets import (QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton)
from PyQt6.QtCore import Qt

import app_config as cfg
from core.data_handler import DataHandler
from core.pca_engine import PCAEngine
from widgets.plot_canvas import PlotCanvas


class PCATabNode(QWidget):
    """Nodo fisico isolato comprendente DB di Memoria e Strati Visuali PCA (Plot)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # CORE DATI (PANDAS E LOGICA SCI-KIT PCA ASSI) RISIEDONO QUI! INDIPENDENTI.
        self.data_backend = DataHandler()  
        self.pca_engine = PCAEngine()
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        
        # TELA 2D (Area Plot Bianca Integrata QT + Strumentazione standard Nav)
        self.plot_surface = PlotCanvas(self)
        
        # Testo Segnalazione/Errore in miniatura sovrastante prima e/o per info caricate 
        self.info_lbl = QLabel(f"Dashboard in stand-by: in attesa della Matrice (Dataset Analisi Orizzonti)")
        self.info_lbl.setStyleSheet(f"color: {cfg.COLOR_TEXT_DIMMED}; font-size: 10pt; font-weight:bold; margin-bottom: 2px;")
        
        self.layout.addWidget(self.info_lbl, 0)
        self.layout.addWidget(self.plot_surface, 1)


class MainTabPanel(QTabWidget):
    """Il master multi-vista Browser Tabs che crea ed ordina l'eliminazione dei TabNode-Suoli."""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setTabsClosable(True)       # <<< QUESTA ABILITA LE [X] Qt System per default.
        self.tabCloseRequested.connect(self._close_tab)
        
        self._apply_dark_style()
        self._setup_add_button()

        # Creazione del Primo e Unico Orizzonte di Default che si auto genererà partendo alla Main Startup! 
        self.add_new_tab(cfg.TAB_NAME_SOIL_A)

    def _apply_dark_style(self):
        """Applica la gerarchia visiva del TabPane, sostituendo inoltre le logiche close."""
        
        # Genera un 'X' di colore  per indicare la chiusura del Tab
        import base64  # Usa lo Standard Library Python
        
        # Appoggia la macro come SVG standard grezzo XML 
        svg_raw = f"<svg viewBox='0 0 10 10' xmlns='http://www.w3.org/2000/svg'><path d='M2.5 2.5 L7.5 7.5 M7.5 2.5 L2.5 7.5' stroke='{cfg.COLOR_ACCENT_BLUE}' stroke-width='1.5' stroke-linecap='round'/></svg>"
        # Bypassa le vulnerabilità dei fogli CSS PyQt mascherando e convertendo binariamente a sicura immagine codificata: 
        svg_b64 = base64.b64encode(svg_raw.encode('utf-8')).decode('utf-8')
        
        # Questa ora possiede colori vivi garantiti dal sistema MS/Windows a prova d'errore
        icon_x = f"data:image/svg+xml;base64,{svg_b64}"

        self.setStyleSheet(
            # Sfondo Pannelli base aperti 
            f"QTabWidget::pane {{ border: 1px solid {cfg.COLOR_BORDER_NORMAL}; border-radius: 4px; background: {cfg.COLOR_BACKGROUND_PANEL}; }}"
            # Schede Spente
            f"QTabBar::tab {{ background: {cfg.COLOR_BACKGROUND_APP}; color: {cfg.COLOR_TEXT_DIMMED}; "
            f"                border: 1px solid {cfg.COLOR_BORDER_NORMAL}; border-bottom: none; "
            f"                padding: 8px 12px; min-width: 140px; font-size: 11pt; "
            f"                border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 4px; }}"
            # Scheda Attiva Selezionata (Nera fucile unificata + verde linea base)
            f"QTabBar::tab:selected {{ background: {cfg.COLOR_BACKGROUND_PANEL}; color: {cfg.COLOR_TEXT_MAIN}; font-weight: bold; border-top: 2px solid {cfg.COLOR_ACCENT_GREEN}; }}"
            
            # Formattazione grafica permanente Box 'X' e stili Mouse Over
            f"QTabBar::close-button {{ border: 1px solid {cfg.COLOR_ACCENT_GREEN}; border-radius: 2px; image: url(\"{icon_x}\"); background: transparent; padding: 2px; margin-top: 1px; }}"
            f"QTabBar::close-button:hover {{ border: 1px solid {cfg.COLOR_ACCENT_GREEN}; background: {cfg.COLOR_BACKGROUND_APP}; }}"
            f"QTabBar::close-button:pressed {{ border: 1px solid {cfg.COLOR_ACCENT_GREEN}; background: {cfg.COLOR_BORDER_NORMAL}; }}"
        )

    def _setup_add_button(self):
        """Genera un Bottone 'PLUS' posizionato nel Top-Right angolo utile."""
        add_btn = QPushButton(" ＋ ")
        add_btn.setToolTip("Aggiungi Tab e Orizzonte di Scarto/Analisi.")
        add_btn.setFixedSize(36, 32) # Leggermente slargato e accorciato
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {cfg.COLOR_ACCENT_GREEN}; "
            f"font-size: 16pt; font-weight: bold; border: 1px solid {cfg.COLOR_BORDER_NORMAL}; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: {cfg.COLOR_BACKGROUND_BOX}; }}"
        )
        add_btn.clicked.connect(lambda: self.add_new_tab("Orizzonte Comparato_N"))
        # Usa i superpoteri base del framework che posiziona come corner default-button una tab header zone bar appositamente. 
        self.setCornerWidget(add_btn, Qt.Corner.TopRightCorner)

    def add_new_tab(self, name="Orizzonte Extra"):
        """Istanziamento reale nuovo nodo (grafica indipendente) integrata a Dati/Handler e aggiunta listati visivi della main gui window."""
        new_node = PCATabNode(self)
        self.addTab(new_node, name)
        self.setCurrentWidget(new_node) # Lo focalizza passandoci sopra (autoshift browser view!). 

    def _close_tab(self, index):
        """Uccide pulendo per evitare memory heap di python il backend frame specifico aperto al plot close()."""
        # (La regola vuole che tu NON resti senza nemmeno un plot aperto) 
        if self.count() > 1: 
            widget = self.widget(index)
            self.removeTab(index)
            widget.deleteLater()  # Richiede QtGarbage di spaccarne ram pointers per sempre di tale df Pandas gigante allocato (sicuro embedded 24-7).