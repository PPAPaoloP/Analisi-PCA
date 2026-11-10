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
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class PlotCanvas(QWidget):
    """Estensione di QWidget che fonde in finestra schema DataPlot emettendo Signals proprietari."""
    
    # Canale trasmissivo UI Custom Event
    point_hovered = pyqtSignal(str)

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
        
        # Riferimenti Memoria Punti Correnti Canvas Render
        self.scatters = None
        self.current_labels = []
        
        # Abilita il collegamento nativo dell'ispezione mouse a hardware Qt/Matplotlib Bridge Canvas C
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)
        
        self.clear_and_format_axis("PC 1", "PC 2")

    def on_hover(self, event):
        """Attivatore silenzioso ed esclusivo emette Testo senza stampare su grafico sovraffollandolo."""
        if event.inaxes == self.ax and self.scatters is not None:
            cont, ind = self.scatters.contains(event)
            if cont:
                idx = ind["ind"][0] 
                lbl = self.current_labels[idx]
                self.point_hovered.emit(f"{lbl}")
            else:
                self.point_hovered.emit("---")
        else:
             self.point_hovered.emit("---")


    def clear_and_format_axis(self, xlab, ylab, g_alpha=0.7, g_ticks=8, g_x=True, g_y=True):
        # Ricostruzione totale: nessuno stato può sopravvivere tra un disegno e l'altro
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#FFFFFF')
        self.ax.tick_params(colors='black')
        for s in self.ax.spines.values():
            s.set_color('black')
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(g_ticks))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(g_ticks))

        axis_opt = 'both' if (g_x and g_y) else 'x' if g_x else 'y' if g_y else None
        if axis_opt:
            self.ax.grid(True, axis=axis_opt, linestyle='--', linewidth=0.5,
                         alpha=g_alpha, color='grey')
        self.ax.axhline(0, color='black', linewidth=1.2, zorder=1)
        self.ax.axvline(0, color='black', linewidth=1.2, zorder=1)
        self.ax.set_xlabel(xlab, fontweight='bold', color='black')
        self.ax.set_ylabel(ylab, fontweight='bold', color='black')


    def draw_biplot(self, scores, loadings, features, labels, v1, v2,
                    load_thr, arr_scale, pt_size, pt_shape, pt_color,
                    g_a, g_n, g_rx, g_ry, ax_names=("PC 1", "PC 2")):
        shapes_map = {"Cerchio": "o", "Quadrato": "s", "Diamante": "D", "Triangolo": "^"}
        color_map = {"Blu Scuro": "#0057B8", "Verde Foresta": "green",
                     "Rosso Rame": "#d92323", "Arancio Brillante": "orange"}
        m_s = shapes_map.get(pt_shape, "o")
        m_c = color_map.get(pt_color, "blue")

        self.clear_and_format_axis(f"{ax_names[0]} ({v1:.1f}%)", f"{ax_names[1]} ({v2:.1f}%)",
                                   g_alpha=g_a, g_ticks=g_n, g_x=g_rx, g_y=g_ry)
        self.current_labels = labels

        self.scatters = self.ax.scatter(scores[:, 0], scores[:, 1], c=m_c, s=pt_size,
                                        marker=m_s, edgecolor='black', alpha=0.9, zorder=3)

        # Scala frecce coerente con i punti: con arr_scale=2.5 la freccia più lunga
        # arriva a ~80% del punto più lontano, sia con std ON che OFF.
        max_score = max(np.abs(scores).max(), 1e-12)
        max_load = max(np.linalg.norm(loadings, axis=1).max(), 1e-12)
        k = (0.8 * max_score / max_load) * (arr_scale / 2.5)

        xs, ys = list(scores[:, 0]), list(scores[:, 1])
        for i, fname in enumerate(features):
            lx, ly = loadings[i, 0], loadings[i, 1]
            # soglia sulla magnitudine "grezza" del loading: indipendente dai dati
            if np.hypot(lx, ly) * arr_scale >= load_thr:
                x, y = lx * k, ly * k
                self.ax.annotate('', xy=(x, y), xytext=(0, 0), zorder=4,
                                 arrowprops=dict(arrowstyle='-|>', color='red', alpha=0.6, lw=1.5))
                self.ax.text(x * 1.08, y * 1.08, fname, color='darkred', ha='center',
                             va='center', fontweight='bold', fontsize=9, zorder=5)
                xs += [x * 1.15]; ys += [y * 1.15]

        # Limiti espliciti, sempre includendo l'origine
        def lim(v):
            lo, hi = min(min(v), 0), max(max(v), 0)
            pad = 0.1 * (hi - lo if hi > lo else 1.0)
            return lo - pad, hi + pad
        self.ax.set_xlim(*lim(xs))
        self.ax.set_ylim(*lim(ys))

        self.canvas.draw()

    '''
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
    '''