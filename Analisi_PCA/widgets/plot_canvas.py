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
import matplotlib.ticker as ticker
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
        """Callback hardware: attiva annotazione popup eliminando redraws a cascata superflui."""
        if event.inaxes == self.ax and self.scatters is not None:
            cont, ind = self.scatters.contains(event)
            if cont:
                idx = ind["ind"][0] 
                
                # Check logico: Evita lo sfarfallio ritracciandolo solo al netto di variazione target (stato bool od identità punto). 
                current_text = self.annot.get_text()
                new_text = self.current_labels[idx]
                if not self.annot.get_visible() or current_text != new_text:
                    self.annot.xy = self.scatters.get_offsets()[idx]
                    self.annot.set_text(new_text)
                    self.annot.set_visible(True)
                    self.canvas.draw_idle()
            else:
                if self.annot.get_visible():
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()

    def clear_and_format_axis(self, xlab: str, ylab: str, 
                              g_alpha=0.7, g_ticks=8, g_x=True, g_y=True):
        """Inizializza diagrammi con supporto regolazioni lineari MaxNLocator (Qt/Matplotlib)."""
        self.ax.clear()
        
        # Geometrie
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color('black') 
        self.ax.spines['right'].set_color('black')
        self.ax.spines['left'].set_color('black')
        self.ax.tick_params(colors='black')
        
        # Controllo sezioni (n=quantità di fette in cui tagliare l'ascissa orizz/vert). 
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(g_ticks))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(g_ticks))

        # Impostazione selettiva degli ortogonali di riferimento base griglie. 
        # Risolve la casistica ON/OFF orizz e ON/OFF verti.
        axis_opt = 'none'
        if g_x and g_y: axis_opt = 'both'
        elif g_x: axis_opt = 'x'
        elif g_y: axis_opt = 'y'
        
        if axis_opt != 'none':
            self.ax.grid(True, axis=axis_opt, linestyle='--', linewidth=0.5, alpha=g_alpha, color='grey')
            
        self.ax.axhline(0, color='black', linewidth=1.2)
        self.ax.axvline(0, color='black', linewidth=1.2)
        self.ax.set_xlabel(xlab, fontweight='bold', color='black')
        self.ax.set_ylabel(ylab, fontweight='bold', color='black')

    def draw_biplot(self, scores, loadings, features, labels, v1: float, v2: float, 
                    load_thr: float, arr_scale: float, pt_size: float, 
                    pt_shape: str, pt_color: str, g_a: float, g_n: int, g_rx: bool, g_ry: bool):
        """Assegna a Scatter parametri derivati (Forme Marker e densità graficanti)."""
        
        # Mappa da Label in Linguaggio italiano dell'UI utente al Marker puro Matplotlib equivalente
        shapes_map = {"Cerchio": "o", "Quadrato": "s", "Diamante": "D", "Triangolo": "^"}
        color_map = {"Blu Scuro": "#0057B8", "Verde Foresta": "green", "Rosso Rame": "#d92323", "Arancio Brillante": "orange"}
        m_s = shapes_map.get(pt_shape, "o")
        m_c = color_map.get(pt_color, "blue")
        
        # Configura Base e tracciati di densità e alfa impostato UI. 
        self.clear_and_format_axis(f"PC 1 ({v1:.1f}%)", f"PC 2 ({v2:.1f}%)", 
                                   g_alpha=g_a, g_ticks=g_n, g_x=g_rx, g_y=g_ry)
        self.current_labels = labels
        
        # Applica Size personalizzato, marker specifici per suoli differiti, opacità moderata ZOrder prioritario su griglie (1<3)
        self.scatters = self.ax.scatter(scores[:, 0], scores[:, 1], 
                                        c=m_c, s=pt_size, marker=m_s, 
                                        edgecolor='black', alpha=0.9, zorder=3)
        
        # Motore elaborazione frecce direzionali e threshold 
        for i, fname in enumerate(features):
            x = loadings[i, 0] * arr_scale
            y = loadings[i, 1] * arr_scale
            magnitude = np.sqrt(x**2 + y**2)
            if magnitude >= load_thr:
                self.ax.arrow(0, 0, x, y, color='red', alpha=0.6, width=0.005, head_width=0.06)
                self.ax.text(x * 1.05, y * 1.05, fname, color='darkred', ha='center', va='center', fontweight='bold', fontsize=9)
        self.canvas.draw()