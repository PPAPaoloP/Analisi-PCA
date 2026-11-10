"""
/**
 *  @file       math_dialog.py
 *  @brief      Fondamenti matematici della riduzione dati multi-dim (Dialog Visiva)
 */
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from PyQt6.QtCore import Qt
import app_config as cfg

class MathDialog(QDialog):
    """Manifesto analitico neutrale per attestazione documentale validazione formula SciKit applicata."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Impalcatura Algoritmica Multivariata (Validation Math Core)")
        self.setFixedSize(700, 850)
        self.setStyleSheet(cfg.GLOBAL_STYLE + f" QDialog {{ background-color: {cfg.COLOR_BACKGROUND_BOX}; border: 1px solid {cfg.COLOR_ACCENT_BLUE}; }}")

        # Testo formattato semplice, leggibile, che unisce linguaggio normale e dimostrazione equazione. 
        testo_fondamenti = """
        <h2 style='color:#00E676; text-align:center;'>FONDAMENTI MATEMATICI (PCA - Principal Component Analysis)</h2>
        <br/>
        <p>L'obiettivo di questo strumento software è permettere la visualizzazione di fogli di calcolo contenenti decine di parametri (multidimensionali), riportandoli semplificati su uno schermo a sole 2 o 3 dimensioni. Esso raggiunge lo scopo proteggendo e mostrando al ricercatore la più alta <i>Variabilità Statistica Reale</i> contenuta in partenza, per mostrare rapidamente le similitudini nei suoli studiati.</p>
        
        <h4 style='color:#4FC3F7;'>Fase 1: Preparazione e Standardizzazione (Se Selezionata) </h4>
        <p>Alcuni elementi nel campione (es. Titanio in mg) avranno escursioni ridottissime, altri (es. percentuale sabbia) da 0 a 100%. Senza questo primo calcolo, il Grafico seguirebbe passivamente soltanto le variabili col numero assoluto grande per via della prepotenza matematica delle percentuali. La standardizzazione equalizza gli squilibri usando Media (μ) e Varianza (σ).</p>
        <div style='background-color:#0A0E12; color:#00E676; font-family: monospace; padding:10px;'>
          <pre> Z(i, j) = ( Dato_Originario(i,j) - Media_di_Colonna ) / Deviazione_Standard(j) </pre>
        </div>
        
        <h4 style='color:#4FC3F7;'>Fase 2: Trovare cosa si "Muove Insieme" (Matrice delle Covarianze) </h4>
        <p>Ora l'algoritmo valuta quali dei 20 parametri aumentino (correlazione positiva) e diminuiscano in simultanea sugli elementi confrontati.</p>
        <div style='background-color:#0A0E12; color:#00E676; font-family: monospace; padding:10px;'>
          <pre> C = Trasposta(Matrice_Z) Moltiplicata (Matrice_Z) </pre>
        </div>

        <h4 style='color:#4FC3F7;'>Fase 3: Selezione delle Componenti Maggiori (Autovalori / PC)</h4>
        <p>Il cervello algebrico Scikit-Learn interroga la "Covarianza C". Trova quegli unici Asse1 (PC1) e Asse2 (PC2) dove sparpagliare liberamente le linee minimizzando gli attriti fra variazioni, catturandone al contrario le fette statistiche più evidenti.<br>Il fattore d'accuratezza estratto matematicamente da quegli orientamenti è calcolato per % rispetto a tutte le direzioni escluse dal biplot visivo. Mostrando per tanto quale grado d'importanza coprano le Coordinate attive a Monitor per lo specifico foglio elaborato.</p>

        <h4 style='color:#4FC3F7;'>Fase 4: Riproiezione Finale degli Spazi Punti</h4>
        <p>Ottenuti PC1, PC2 (Autovettori Maggiori): <br>I) Vengono Moltiplicati alle costanti base originarie per estrapolare al termine lo <b>"Score"</b> (Le coordinate x e y reali in centimetri disegnati su Mappa dei rispettivi fogli / Elemento Campione analizzato visibile in tooltip di destra come Punti Sparsi Blu).<br>II) Mentre l'influenza fisica pura d'Equazione del singolo minerale estratta o tracciante che sbilanciò quel peso verrà esibita tramite la relativa Frecce Vettoriale direzionale dipinta assieme a tale elemento nel diagramma.</p>
        
        <br/>
        <hr style='border:1px solid #4FC3F7'/>
        <p style='color:#6C7A82; text-align:right; font-size:12px;'>Architettura software basata nativamente sulla libreria universale aperta: "scikit-learn - sklearn.decomposition.PCA" in ecosistema stabile Python. (Data Protection Isolation and UI Framework: PyQt6 GUI Toolkit Desktop Implementation.)</p>
        """
        
        # Scatolo a scroll testo senza far editare il documento ad Utenti Inerti su sistema HTML Base OS Rendering Qt5 Web C! 
        layout = QVBoxLayout(self)
        display = QTextBrowser()
        display.setOpenExternalLinks(False)
        display.setStyleSheet("background:transparent; border: none; font-size: 13pt; line-height: 1.5; color:#ddd; ")
        display.setHtml(testo_fondamenti)
        
        btn = QPushButton("Convalida e Chiudi Documentazione")
        btn.clicked.connect(self.accept)
        
        layout.addWidget(display)
        layout.addWidget(btn)