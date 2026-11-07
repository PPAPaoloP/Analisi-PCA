"""
/**
 *  @file       AnalisiPCA_main.py
 *  @brief      Entry point eseguibile per l'avvio del programma.
 *
 *  @details
 *              Genera ed accende l'App Context Qt, istanzia il Main_Window
 *              e mantiene pulita la coda (Event Loop System), configurando anche
 *              supporto di display primari ad alta definizione e corretta gestione
 *              DPI (HiDPI scaling) introdotta negli engine Python recenti.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import sys
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
import app_config as cfg
from widgets.main_window import MainWindow

def main():
    # 1. Configurazione avanzata dell'App per schermi ad alta risoluzione 
    # (Obbligatorio nel desktop env embedded)
    if not os.environ.get('QT_ENABLE_HIGHDPI_SCALING'):
        os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

    # 2. Start Contenitore Grafico Standard
    app = QApplication(sys.argv)
    app.setApplicationName(cfg.APP_NAME)
    
    # [Opzionale in futuro] Installare e configurare font custom come Montserrat o Roboto. 
    # font_db = QFontDatabase()

    # 3. Istanzia Master Class e apri a schermo 1920x1080 
    # Usa ".showMaximized()" o solo ".show()" come preferito
    window = MainWindow()
    # Costringiamo Windows a posizionarlo Maximized ed al centro indipendentemente dai monitori collegati! 
    # Così rispetta a tolleranza totale eventuali 125% di font scaling MS
    window.showMaximized()

    # 4. Sys Exit su Chiusura o Kill.
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
