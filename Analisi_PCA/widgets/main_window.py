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

from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QFileDialog)
from PyQt6.QtCore import Qt, QEvent

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
                      
        # Architettura UI Fisica e Cablaggi
        self._build_main_ui()
        self._connect_signals()

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

    def _connect_signals(self):
        """Assegnazione segnali asincroni e monitoraggi d'evento."""
        self.right_col.btn_load.clicked.connect(self._action_load_file)
        
        # Abilita cattura eventi del mouse sui widget critici per informare l'utente:
        self.right_col.btn_load.installEventFilter(self)
        self.right_col.chk_std.installEventFilter(self)
        self.right_col.combo_axes.installEventFilter(self)
        self.right_col.sl_thr.installEventFilter(self)
        self.right_col.sl_scl.installEventFilter(self)

        # TRIGGER MATEMATICI DINAMICI -> Ogni microtocco farà calcolare il disegno e re-stampare tela!
        self.right_col.chk_std.toggled.connect(self._render_current_plot)
        self.right_col.combo_axes.currentIndexChanged.connect(self._render_current_plot)
        self.right_col.sl_thr.valueChanged.connect(self._render_current_plot)
        self.right_col.sl_scl.valueChanged.connect(self._render_current_plot)

        # TRACCIATI SECONDARI DI RETICOLAZIONE GRAFICA AD ESTESA MANO D'AZIONE. (Re Render Totale Senza Ritocco Scikit) 
        self.right_col.sl_pt_size.valueChanged.connect(self._render_current_plot)
        self.right_col.sl_ticks.valueChanged.connect(self._render_current_plot)
        self.right_col.sl_alpha.valueChanged.connect(self._render_current_plot)
        self.right_col.chk_grid_x.toggled.connect(self._render_current_plot)
        self.right_col.chk_grid_y.toggled.connect(self._render_current_plot)
        self.right_col.cb_shape.currentIndexChanged.connect(self._render_current_plot)
        self.right_col.cb_color.currentIndexChanged.connect(self._render_current_plot)
        
        # Filtro mouse Pulsante ESPORTA e asssegnazione esecuzione per il pulsante d'Esportazione (Nuovo test per Utenti File .CSV Scores puri/Loadings) 
        self.right_col.btn_save_pca.installEventFilter(self)
        self.right_col.btn_save_pca.clicked.connect(self._action_export_pca)

    def eventFilter(self, source, event):
        """Monitoraggio eventi mouse su oggetti ispezionabili e aggiornamento Status Box."""
        msg = None
        
        # Inizio Check Interazioni per Eventi Mouse (Enter/Over):
        if event.type() == QEvent.Type.Enter:
            if source == self.right_col.btn_load:
                msg = ("Carica fogli Dati o database locali (CSV / Excel).\n"
                       "Estirperà formati invalidi preservando le variabili numeriche valide per l'Analisi Multi-variata.")
            
            elif source == self.right_col.btn_save_pca:
                msg = ("Scarica le matrici processate dell'area matematica (Scores/Coordinate Tabella in formatazione NumPy) "
                       "sull'Hdd (Cartella Windows) ad uso import software graficati su base terza in futuro in formato Raw CSV Excel!")

            elif source == self.right_col.chk_std:
                msg = ("Pre-Processamento PCA.\nAbilitandolo (consigliato) rimuove lo sbilanciamento forzato "
                       "quando le misure spaziano da minime (% argilla) ad estreme (metalli alcalini ppm).")
            
            elif source == self.right_col.combo_axes:
                msg = ("Matrice Dimensionale 2D. (PC1: Asse a max varianza residua).\n"
                       "Permette la scansione geometrica analizzando variabili incrociate se i campioni differiscono poco sul fronte primario.")
            
            elif source == self.right_col.sl_thr:
                msg = ("Regolazione Soglia Minima di Plot:\n"
                       "Filtra e non visualizza i Vettori i cui elementi impattano la decomposizione complessiva del biplot solo superficialmente.")
            
            elif source == self.right_col.sl_scl:
                msg = ("Fattore Visuale Scala (Rendering visivo Matplotlib):\n"
                       "Moltiplicatore asse vettore indipendente dalla coordinata Scores punti campioni sparsi. Usa per enfatizzazioni visive direttrici.")
        
        # Condizione pulizia Uscita Cursor
        elif event.type() == QEvent.Type.Leave:
            msg = cfg.APP_DESCRIPTION

        # Disegna se rilevato ed impostato in passaggio
        if msg:
            self.top_banner.set_status_text(msg)
            
        return super().eventFilter(source, event)

    def _action_load_file(self):
        """Metodo invocato via Qt EventLoop. Estrae contesto per lavorare ESCLUSIVAMENTE nella Tab che sta in Front-Page End-User Focus!!!"""
        
        filepath, filter_string = QFileDialog.getOpenFileName(
            self,
            "Seleziona database Orizzonte (Data Input CSV / XLSX)",
            "",
            "Fogli Calcolo Data (*.csv *.xls *.xlsx);;Tutti I file (*.*)"
        )

        if not filepath: # Annullato operazione Browser Popup di MS/Win32 explorer 
            return
            
        self.top_banner.set_status_text(f"Esecuzione Lettura Array Locale (Core File)...")

        # RICERCA INDIRIZZO del TAB ATTIVO (Pointer Fetching di Widget): Prende dal contenitore Qtab master "Quale Node stai Vedendo ora?" 
        current_tab_node = self.tab_panel.currentWidget()
        if not current_tab_node:
            self.top_banner.set_status_text(f"Errore UI Architettura: Impossibile collegare la colonna Dati al Target vuoto..")
            return 
            
        # CARICAMENTO sul Local Backend File della Node specificato Focus, se era in "Index2, lavora tutto nell Array nascosto suo".  
        result = current_tab_node.data_backend.load_file(filepath)

        if "OK_DATA" in result:
            nome_file_puro = filepath.split('/')[-1]
            msg = result.replace('OK_DATA:', '').strip()
            idx = self.tab_panel.indexOf(current_tab_node)
            self.tab_panel.setTabText(idx, f"{nome_file_puro}")
            
            # Stringa ridotta informativa
            current_tab_node.info_lbl.setText(
                f"Importazione Dati completato per il DataBese [{nome_file_puro}].\n"
            )
            self.top_banner.set_status_text(f"File {nome_file_puro} importato con successo.\n[{msg}]")
            # Richiesta di disegno per il Biplot iniziale avendo appena introdotto un DataBase sano
            self._render_current_plot()
        else:
            self.top_banner.set_status_text(f"Interruzione Importazione DB locale.\nCause: {result}")

    def _action_export_pca(self):
        """Costruisce ed esporta tabelle metriche PCA su Hard-Drive via Pandas/openpyxl."""
        node = self.tab_panel.currentWidget()
        
        # Validazione di presenza dei dati processabili
        if not node or not node.data_backend.has_data():
            self.top_banner.set_status_text("Violazione esportazione: Nessun orizzonte numerico al momento è istanziato o letto nel canvas.")
            return

        filepath, filter_string = QFileDialog.getSaveFileName(
            self,
            "Salvataggio Resoconto Multivariata (Punti, Autovettori e Varianza)",
            "Dati_Analisi_Orizzonti.xlsx",
            "File Excel/MS Data (*.xlsx);;Valori Comma Separati CSV (*.csv)"
        )

        if not filepath:
            return  # Esportazione utente respinta

        self.top_banner.set_status_text("Avviata formattazione Matrici... Processamento in attesa I/O sistema file...")
        
        engine = node.pca_engine
        db = node.data_backend
        
        import pandas as pd
        
        try:
            # Matrice A: Posizione Geometrica Scores campioni analizzati (Coordinatometrici)
            df_scores = pd.DataFrame(
                engine.scores, 
                columns=[f"PC{i+1}" for i in range(engine.scores.shape[1])]
            )
            df_scores.insert(0, "Label Identificatore", db.labels)
            
            # Matrice B: Influenza Matematica Elemento per l'inclinamento Bi-plot Loadings vettoriali 
            df_loadings = pd.DataFrame(
                engine.loadings,
                columns=[f"PC{i+1}_Magnitude" for i in range(engine.loadings.shape[1])]
            )
            df_loadings.insert(0, "Feature Osservata", engine.feature_names)

            if filepath.endswith('.csv'):
                # Lo standard Comma-Separated non incapsula multi-tables. Verrà esplicitamente passata sola Coordinatometria campioni
                df_scores.to_csv(filepath, index=False)
                self.top_banner.set_status_text(f"Salvata coordinata su CSV Piatto con Successo in : [{filepath.split('/')[-1]}].")
            else:
                # Estrazione scientifica nativa (Motore engine openpyxl precedentemente fornito nel core env)
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    df_scores.to_excel(writer, sheet_name='Scores_Posizione_Suolo', index=False)
                    df_loadings.to_excel(writer, sheet_name='Pesi_Feature_Loadings', index=False)
                    
                    df_info = pd.DataFrame({
                        'Vettore Assoluto Principale': [f"PC{i+1}" for i in range(len(engine.variance))],
                        'Percentuale Copertura % (Varianza)': engine.variance
                    })
                    df_info.to_excel(writer, sheet_name='Bilancio_Varianza_Apportata', index=False)
                
                self.top_banner.set_status_text(f"Tabulato analitico multi-cartella compilato! Nome asseverato al sistema [{filepath.split('/')[-1]}].")

        except PermissionError:
             self.top_banner.set_status_text("Error System(32) Permission: File temporaneamente occupato e ostruito (Spesso tenuto acceso nel background MS Excel chiuso).")
        except Exception as esx:
             self.top_banner.set_status_text(f"Critical Halt su Write IO Pandas module :\n->  {esx}")


    def _render_current_plot(self):
        """Coordinamento centrale del Canvas Plot Matematico a cura dell'Active Tab Browser!"""
        node = self.tab_panel.currentWidget()
        
        # Filtro preventivo sicurezza 
        if not node or not node.data_backend.has_data():
            return
            
        db = node.data_backend
        # Motore Algebra e Tensor (Individuo tab-dedicato e indipendente) 
        core = node.pca_engine  

        # Legge Hardware Fisico-Sensoriale del UI: Parametria attiva 
        usa_std = self.right_col.chk_std.isChecked()
        lbl_assi = self.right_col.combo_axes.currentText()
        thr = self.right_col.sl_thr.value() / 10.0      # Da Integer Slide a range 0.0 -> 5.0 Magnitudine vettori Filtrata. 
        scl = self.right_col.sl_scl.value() / 10.0      # Moltiplicazione ingrandimento Visiva delle Retta Direzione. (Default è 2.5x per colpa del Canvas ratio piccolo originale)
        
        # Parametri Estetici / Tracciamento Canvas Forme Retini UI Control Variables Array Extractor Base (A/R) e Conversioni Integer - > % Float alfa.. . 
        ui_s = self.right_col.cb_shape.currentText()
        ui_c = self.right_col.cb_color.currentText()
        ui_size = self.right_col.sl_pt_size.value()
        ui_t = self.right_col.sl_ticks.value()
        ui_a = self.right_col.sl_alpha.value() / 100.0  
        b_g_x = self.right_col.chk_grid_x.isChecked()
        b_g_y = self.right_col.chk_grid_y.isChecked()

        # Scelta della Combinatoria su matrice Z Scikit (Mapping per l'Array finale)
        i_x, i_y = 0, 1 # By default (PC1 PC2 indici informatica [0 e 1] di matrice N righe C colonne NumPy Numpy ) 
        if "PC1 vs PC3" in lbl_assi:
            i_y = 2
        elif "PC2 vs PC3" in lbl_assi:
            i_x, i_y = 1, 2
        
        # Genera Analiticamente ad un core fisico hardware Matplotlib C-Optimized C: il DataFrame. Mantenendo Standarizzato/Misti.
        riscontro_algebra_fatta = core.fit_transform(db.features_df, standardize=usa_std)

        if riscontro_algebra_fatta:
            
            var_x = core.variance[i_x] 
            var_y = core.variance[i_y]

            # Affettatore Array per il 2D Piano specificatamente chiesto per estrarne due fasce colonna singola matrice V per Scores D'Analisi . 
            coord_pt = core.scores[:, [i_x, i_y]]
            
            # Idem vettore estrattivo assi lineari Feature e direttrici (V Loadings Matrix Extraction for iX / iY projection axis 2d rendering space canvas ):  
            dir_vt = core.loadings[:, [i_x, i_y]]

            # Invio Dati Core all'Assemblatore QT/Python Esternalizzando tutti e tredici vari input!
            node.plot_surface.draw_biplot(
                scores=coord_pt, loadings=dir_vt, features=core.feature_names,
                labels=db.labels, # La mappatura nominativa etichetta suoli campione ("TestA1...", Etc).
                v1=var_x, v2=var_y, load_thr=thr, arr_scale=scl,
                pt_size=ui_size, pt_shape=ui_s, pt_color=ui_c,
                g_a=ui_a, g_n=ui_t, g_rx=b_g_x, g_ry=b_g_y
            )    