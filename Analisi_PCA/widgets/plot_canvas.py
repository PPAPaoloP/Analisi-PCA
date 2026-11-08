"""
/**
 *  @file       plot_canvas.py
 *  @brief      Interfaccia visiva per disegno di diagrammi Matplotlib su PyQt6.
 *
 *  @details
 *              Incapsula i Subplot del sistema PCA generati, impostando ambiente
 *              luminoso "Sfondo Bianco" per refertazione stampa analitica e 
 *              gestendo logicamente i vettori Freccia e Hover Punti campionamento.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-08
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import numpy as np
import matplotlib
matplotlib.use('QtAgg') # Imposta motore backend integrato Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class PlotCanvas(QWidget):
    """Estensione di QWidget che fonde in finestra lo schema nativo DataPlot e Strumenti mouse."""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Formattazione grafica figura globale
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.fig.patch.set_facecolor('#FFFFFF') # Corpo bordo finestratura
        
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#FFFFFF')        # Corpo zona matematica centrale
        
        # Instanzia barra Standard per lo Zoom box ed esportazione .png di sistema
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Metadati per gestione cursori informativi popup
        self.scatters = None
        self.current_labels = []
        self._init_annotation()
        
        # Pulisce assi pronti a primo utilizzo vuoto
        self.clear_and_format_axis("PC 1", "PC 2")

    def _init_annotation(self):
        """Prepara componente nativo tooltip in attesa posizionamento per label dei punti."""
        self.annot = self.ax.annotate(
            "", xy=(0,0), xytext=(12, 12), textcoords="offset points",
            bbox=dict(boxstyle="round4", fc="yellow", alpha=0.9, lw=0.5),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
        )
        self.annot.set_visible(False)
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

    def on_hover(self, event):
        """Attivato dalla callback hardware del puntatore interno alle figure"""
        if event.inaxes == self.ax and self.scatters is not None:
            cont, ind = self.scatters.contains(event)
            if cont:
                # Estrae identificativo puntato tramite logiche index dell'array array coordinate
                idx = ind["ind"][0] 
                self.annot.xy = self.scatters.get_offsets()[idx]
                self.annot.set_text(self.current_labels[idx])
                self.annot.set_visible(True)
                self.canvas.draw_idle()
            else:
                if self.annot.get_visible():
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()

    def clear_and_format_axis(self, xlab: str, ylab: str):
        """Azzera e uniforma stili, ortogonalità centrate ad origine, tick nere ad elevato contrasto."""
        self.ax.clear()
        
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color('black') 
        self.ax.spines['right'].set_color('black')
        self.ax.spines['left'].set_color('black')
        self.ax.tick_params(colors='black')
        self.ax.yaxis.label.set_color('black')
        self.ax.xaxis.label.set_color('black')

        self.ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7, color='grey')
        # Centra fisicamente linee passanti orignini per evidenziare clustering
        self.ax.axhline(0, color='black', linewidth=1.2)
        self.ax.axvline(0, color='black', linewidth=1.2)
        
        self.ax.set_xlabel(xlab, fontweight='bold')
        self.ax.set_ylabel(ylab, fontweight='bold')

    def draw_biplot(self, scores, loadings, features, labels, v1: float, v2: float, load_thr: float, arr_scale: float):
        """Stampa fisica componenti su figure-frame usando logica ibrida Vettori + Dispersione(Scatter)."""
        self.clear_and_format_axis(f"PC 1 ({v1:.1f}%)", f"PC 2 ({v2:.1f}%)")
        self.current_labels = labels
        
        # Rendering Scores 
        self.scatters = self.ax.scatter(scores[:, 0], scores[:, 1], c='blue', s=45, edgecolor='black', alpha=0.8, zorder=3)
        
        # Calcolo modulo delle rette dei Loadings, con normalizzazione per visibilità estetica
        for i, fname in enumerate(features):
            x = loadings[i, 0] * arr_scale
            y = loadings[i, 1] * arr_scale
            magnitude = np.sqrt(x**2 + y**2)
            
            # Filtro pulizia sovraffollamento tramite Cursore di Magnitudine laterale 
            if magnitude >= load_thr:
                # Traccia un Dardo 
                self.ax.arrow(0, 0, x, y, color='red', alpha=0.6, width=0.005, head_width=0.06)
                # Applica marcatore testo testata finale a contrasto sul fondo bianco
                self.ax.text(x * 1.05, y * 1.05, fname, color='darkred', ha='center', va='center', fontweight='bold', fontsize=9)
        
        self.canvas.draw()