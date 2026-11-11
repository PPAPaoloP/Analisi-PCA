"""
/**
 *  @file       math_dialog.py
 *  @brief      Finestra "Fondamenti matematici e codice del motore PCA".
 *
 *  @details
 *              Mostra, in forma divulgativa, la matematica della PCA e il
 *              codice Python (pca_engine.py) che la implementa, in modo che
 *              ogni passaggio del calcolo sia verificabile dall'utente.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import html

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
import app_config as cfg


# Copia del metodo PCAEngine.fit_transform (pca_engine.py) mostrata nella finestra.
# Se si modifica il motore, aggiornare anche questo blocco.
CODICE_PCA = r'''def fit_transform(self, df: pd.DataFrame, standardize: bool = True) -> bool:
    """Calcola la PCA sulla tabella numerica `df`.

    df          : righe = campioni, colonne = variabili (solo valori numerici).
    standardize : True  -> centratura e scalatura a varianza unitaria
                           (PCA sulla matrice di correlazione);
                  False -> sola centratura (PCA sulla matrice di covarianza).
    Ritorna True se il calcolo riesce, False se `df` è vuoto.
    """
    if df is None or df.empty:
        return False

    self.feature_names = df.columns.tolist()

    # Modelli ricreati a ogni chiamata: nessuno stato residuo tra i calcoli
    self.scaler = StandardScaler(copy=True)
    self.pca = PCA(n_components=3, svd_solver='full')

    # Copia di lavoro: il DataFrame originale non viene mai modificato
    data_matrix = np.array(df.values, dtype=float, copy=True)

    # Fase 1 - Pre-elaborazione
    if standardize:
        # Z = (X - media) / deviazione standard, colonna per colonna
        data_matrix = self.scaler.fit_transform(data_matrix)
    else:
        # Sola centratura: le variabili con valori più grandi pesano di più
        data_matrix = data_matrix - np.mean(data_matrix, axis=0)

    # Fasi 2-4 - Covarianza, autovettori e proiezione (SVD di scikit-learn).
    # Solver 'full' = SVD esatta; il segno di ogni PC è fissato da sklearn
    # (svd_flip), quindi a parità di dati il risultato è sempre lo stesso.
    self.scores = self.pca.fit_transform(data_matrix)          # (n x 3)
    self.loadings = self.pca.components_.T                     # (p x 3)
    self.variance = self.pca.explained_variance_ratio_ * 100   # % su var. totale

    return True'''


def _eq(contenuto: str) -> str:
    """Riquadro scuro centrato per una formula (HTML compatibile con Qt)."""
    return ("<table width='100%' cellpadding='8'><tr>"
            "<td bgcolor='#0A0E12' align='center'>"
            "<span style='color:#00E676; font-family:Consolas,monospace; "
            f"font-size:12pt;'>{contenuto}</span></td></tr></table>")


def _codice(sorgente: str) -> str:
    """Riquadro scuro per un blocco di codice (testo escapato)."""
    return ("<table width='100%' cellpadding='10'><tr>"
            "<td bgcolor='#0A0E12'>"
            "<pre style='color:#E0E0E0; font-family:Consolas,monospace; "
            f"font-size:10pt;'>{html.escape(sorgente)}</pre>"
            "</td></tr></table>")


EQ_STD = _eq("X<sub>c</sub> = X − μ<br/>"
             "Z<sub>ij</sub> = ( x<sub>ij</sub> − μ<sub>j</sub> ) / σ<sub>j</sub>")
EQ_COV = _eq("C = 1/(n−1) · Z<sup>T</sup> Z")
EQ_EIG = _eq("C · v<sub>k</sub> = λ<sub>k</sub> · v<sub>k</sub><br/>"
             "λ<sub>1</sub> ≥ λ<sub>2</sub> ≥ … ≥ λ<sub>p</sub>")
EQ_VAR = _eq("Varianza spiegata da PC<sub>k</sub> [%] = "
             "100 · λ<sub>k</sub> / Σ<sub>j</sub> λ<sub>j</sub>")
EQ_SVD = _eq("Z = U · S · V<sup>T</sup><br/>"
             "λ<sub>k</sub> = s<sub>k</sub><sup>2</sup> / (n−1)")
EQ_SCORE = _eq("T = Z · V<sub>3</sub><br/>"
               "(n × p) · (p × 3) = (n × 3)")

TESTO_HTML = f"""
<h2 style='color:#00E676; text-align:center;'>
  FONDAMENTI MATEMATICI DELLA PCA<br/>
  <span style='font-size:11pt; color:#4FC3F7;'>Analisi delle Componenti Principali</span>
</h2>

<p>La PCA riduce una tabella con molte variabili (decine di misure chimiche e
granulometriche per ogni campione) a poche nuove variabili, le
<b>Componenti Principali (PC)</b>, che conservano la maggior parte della
variabilità originale. Sul grafico 2D i campioni simili risultano vicini e
quelli diversi lontani.</p>

<p><b>Notazione.</b> La tabella dati è una matrice <b>X</b> di <i>n</i> righe
(campioni) e <i>p</i> colonne (variabili). I dati originali non vengono mai
modificati: i calcoli lavorano su una copia.</p>

<h4 style='color:#4FC3F7;'>Fase 1 - Centratura e standardizzazione</h4>
<p>Si sottrae a ogni colonna la propria media μ (<i>centratura</i>), così che
la nuvola di campioni sia centrata nell'origine degli assi. Con l'opzione
<b>Standardizzazione</b> attiva si divide anche per la deviazione standard σ di
ogni colonna: tutte le variabili hanno allora media 0 e varianza 1.</p>
{EQ_STD}
<p>Senza standardizzazione contano i valori assoluti: una variabile espressa in
centinaia di g/kg domina su una espressa in percentuale, indipendentemente da
quanto varia davvero. La PCA lavora in questo caso sulla matrice di
<i>covarianza</i>; con la standardizzazione lavora sulla matrice di
<i>correlazione</i>, e ogni variabile pesa allo stesso modo.</p>

<h4 style='color:#4FC3F7;'>Fase 2 - Matrice di covarianza</h4>
<p>Si misura quali variabili variano insieme. La matrice <b>C</b> (<i>p × p</i>,
simmetrica) contiene in posizione (<i>j, k</i>) la covarianza tra le variabili
<i>j</i> e <i>k</i>; sui dati standardizzati coincide con il coefficiente di
correlazione.</p>
{EQ_COV}

<h4 style='color:#4FC3F7;'>Fase 3 - Autovalori e autovettori</h4>
<p>Le Componenti Principali sono gli <b>autovettori</b> <i>v<sub>k</sub></i> di
C: direzioni ortogonali tra loro, di lunghezza 1, nello spazio delle variabili.
Il relativo <b>autovalore</b> <i>λ<sub>k</sub></i> è la varianza dei dati lungo
quella direzione. Ordinandoli dal più grande, PC1 è la direzione di massima
variabilità, PC2 la massima tra quelle ortogonali a PC1, e così via.</p>
{EQ_EIG}
<p>La percentuale mostrata sugli assi del grafico è la quota di varianza
<b>totale</b> catturata da ciascuna componente:</p>
{EQ_VAR}
<p>In pratica scikit-learn non costruisce C esplicitamente: applica la
decomposizione ai valori singolari (SVD) direttamente a Z. Il risultato è
equivalente ma numericamente più stabile; le colonne di V sono gli autovettori.</p>
{EQ_SVD}

<h4 style='color:#4FC3F7;'>Fase 4 - Proiezione e lettura del biplot</h4>
<p>Le coordinate dei campioni (<b>scores</b>, punti blu) si ottengono proiettando
i dati standardizzati sulle prime tre componenti:</p>
{EQ_SCORE}
<p>I pesi delle variabili su ogni componente (<b>loadings</b>, gli autovettori
stessi) sono disegnati come <b>frecce</b>. Per leggere il grafico:</p>
<ul>
  <li><b>Punti vicini</b>: campioni con composizione simile; punti lontani:
      composizione diversa.</li>
  <li><b>Lunghezza della freccia</b>: quanto la variabile contribuisce al piano
      mostrato. Il cursore di visibilità nasconde le frecce più deboli.</li>
  <li><b>Direzione</b>: un punto spostato nel verso di una freccia ha valori
      della variabile superiori alla media. Frecce con angolo piccolo indicano
      variabili correlate positivamente, frecce opposte correlate
      negativamente, frecce perpendicolari non correlate (lettura
      approssimata, tanto più valida quanto più il piano spiega varianza).</li>
</ul>
<p>Il moltiplicatore dei vettori ridimensiona le frecce solo a scopo grafico: non
altera i risultati del calcolo.</p>

<h4 style='color:#4FC3F7;'>Implementazione Python (pca_engine.py)</h4>
<p>Il metodo seguente è il nucleo del motore. I commenti indicano a quale fase
corrisponde ciascun passaggio. Il calcolo è deterministico: stessi dati e
stesse opzioni producono sempre lo stesso grafico.</p>
@@CODEBOX@@

<hr style='border:1px solid #4FC3F7'/>
<p style='color:#6C7A82; text-align:right; font-size:12px;'>Calcolo basato su
scikit-learn (<i>sklearn.decomposition.PCA</i>, <i>StandardScaler</i>);
interfaccia grafica PyQt6, grafici Matplotlib.</p>
"""


class MathDialog(QDialog):
    """Finestra informativa: matematica della PCA e codice che la implementa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fondamenti matematici e codice del motore PCA")
        self.setFixedSize(700, 850)
        self.setStyleSheet(cfg.GLOBAL_STYLE +
                           f" QDialog {{ background-color: {cfg.COLOR_BACKGROUND_BOX};"
                           f" border: 1px solid {cfg.COLOR_ACCENT_BLUE}; }}")

        layout = QVBoxLayout(self)

        display = QTextBrowser()
        display.setOpenExternalLinks(False)
        display.setStyleSheet("background:transparent; border: none; "
                              "font-size: 13pt; color:#ddd;")
        display.setHtml(TESTO_HTML.replace("@@CODEBOX@@", _codice(CODICE_PCA)))

        btn = QPushButton("Chiudi")
        btn.clicked.connect(self.accept)

        layout.addWidget(display)
        layout.addWidget(btn)