"""
/**
 *  @file       app_config.py
 *  @brief      Configurazioni globali e costanti per l'applicazione Analisi PCA.
 *
 *  @details
 *              Questo modulo contiene tutte le costanti statiche di UI, temi, 
 *              layout grafici e metadati del programma, fungendo da sorgente 
 *              unica della verità (SSOT - Single Source Of Truth).
 *              
 *              Architettura del progetto corrente:
 *              /AnalisiPCA/
 *              ├── app_config.py             <- Colori, Versione, Testi, Font
 *              ├── AnalisiPCA_main.py        <- Entry point per avviare l'eseguibile PyQt6
 *              │
 *              ├── /core/                    <- Logica dati e matematica
 *              │   ├── data_handler.py       <- Lettura/Sanificazione DataFrame (Pandas)
 *              │   └── pca_engine.py         <- Motore matematico PCA (scikit-learn)
 *              │
 *              └── /widgets/                 <- Elementi dell'interfaccia utente grafica
 *                  ├── main_window.py        <- Finestra Master
 *                  ├── top_banner.py         <- Striscia 10% (Titolo, Data/Ora real-time, versione)
 *                  ├── main_tab_panel.py     <- Struttura e gestore dei TAB
 *                  ├── plot_canvas.py        <- Disegno del grafico, assi e vettori
 *                  └── control_column.py     <- Colonna di destra con Slider e Pulsanti
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

# ==========================================
# METADATI DELL'APPLICAZIONE
# ==========================================
APP_NAME = "Analisi PCA"
APP_VERSION = "Ver 1.0.0"
APP_AUTHOR = "Ing. Paolo Parrino"

# ==========================================
# IMPOSTAZIONI FINESTRA
# ==========================================
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
# Rapporto spazio UI (Corpo 90% in altezza, Header 10%. Larghezza laterale destra 30%)
HEADER_HEIGHT_RATIO = 0.10
RIGHT_COLUMN_WIDTH_RATIO = 0.30

# ==========================================
# PALETTE COLORI
# ==========================================
COLOR_BACKGROUND_APP   = "#0A0E12"  # Sfondo nerissimo dell'app intera
COLOR_BACKGROUND_BOX   = "#12181F"  # Sfondo delle aree contenitive (GroupBox/Tab)
COLOR_BORDER_NORMAL    = "#2E3D4A"  # Bordi grafici
COLOR_TEXT_MAIN        = "#B9C6CE"  # Colore standard testo / scritte generiche
COLOR_TEXT_DIMMED      = "#6C7A82"  # Colore note sottotitolo o disabilitati
COLOR_ACCENT_GREEN     = "#00E676"  # Il tuo "Verde Smeraldo" per titoli e valori forti
COLOR_ACCENT_BLUE      = "#4FC3F7"  # Blu azzurro per indicatori asse X/Y e cursori

COLOR_BTN_BACKGROUND_NORMAL = "#0057B8"  # Sfondo base bottoni 
COLOR_BTN_BACKGROUND_HOVER  = "#007BFF"  # Sfondo pulsante premuto
COLOR_BTN_BACKGROUND_ACTIVE = "#003F82"

# ==========================================
# CSS STYLE_SHEET GLOBALE DI BASE
# ==========================================
# Il template format fa sì che vengano rimpiazzati al momento con i parametri cromatici esatti.
GLOBAL_STYLE = f"""
    QWidget {{
        background-color: {COLOR_BACKGROUND_APP};
        color: {COLOR_TEXT_MAIN};
        font-family: 'Consolas', 'DejaVu Sans Mono', monospace;
        font-size: 11pt;
    }}
    
    QGroupBox {{
        background-color: {COLOR_BACKGROUND_BOX};
        border: 1px solid {COLOR_BORDER_NORMAL};
        border-radius: 4px;
        margin-top: 14px;
        font-weight: bold;
    }}
    
    QPushButton {{
        background-color: {COLOR_BTN_BACKGROUND_NORMAL};
        color: white;
        border-radius: 4px;
        padding: 8px;
        font-weight: bold;
    }}
    
    QPushButton:hover {{
        background-color: {COLOR_BTN_BACKGROUND_HOVER};
    }}
    
    QPushButton:pressed {{
        background-color: {COLOR_BTN_BACKGROUND_ACTIVE};
    }}
"""

# ==========================================
# IMPOSTAZIONI PCA MATEMATICA E PLOTTING
# ==========================================
# Se servirà, qui salveremo variabili grafiche (tipo dimensioni markers e font canvas).
PLOT_POINT_SIZE = 45
PLOT_ARROW_WIDTH = 0.005