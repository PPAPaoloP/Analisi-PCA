"""
/**
 *  @file       data_handler.py
 *  @brief      Caricamento e validazione dei dati (CSV / Excel) tramite Pandas.
 *
 *  @details
 *              Legge il file, separa le etichette dei campioni dalle variabili
 *              numeriche e verifica la qualità dei dati prima della PCA.
 *
 *              Politica sui dati non validi: i valori mancanti o non numerici
 *              non vengono mai inventati (nessuna imputazione). Le variabili e
 *              i campioni incompleti sono esclusi dall'analisi e ogni esclusione
 *              è registrata in `warnings`, così l'utente può verificarla.
 *              Il file originale non viene mai modificato e, se l'importazione
 *              fallisce, i dati caricati in precedenza restano invariati.
 *
 *  @version    1.1.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-11
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import os

import numpy as np
import pandas as pd

# Una variabile con più di questa frazione di valori mancanti viene esclusa:
# è preferibile perdere una variabile che molti campioni.
MAX_FRAZIONE_MANCANTI = 0.30

# La PCA a 3 componenti richiede almeno 3 campioni e 3 variabili.
MIN_CAMPIONI = 3
MIN_VARIABILI = 3

# Numero massimo di elementi elencati in ogni messaggio.
MAX_ELENCO = 8


def _elenco(voci, sep=", ") -> str:
    """Elenco compatto per i messaggi: 'a, b, c ... (+N altri)'."""
    voci = [str(v) for v in voci]
    testo = sep.join(voci[:MAX_ELENCO])
    if len(voci) > MAX_ELENCO:
        testo += f" ... (+{len(voci) - MAX_ELENCO} altri)"
    return testo


def _pl(n: int, singolare: str, plurale: str) -> str:
    """'1 campione' / '3 campioni'."""
    return f"{n} {singolare if n == 1 else plurale}"


class DataHandler:
    """Caricamento, validazione e partizionamento etichette/variabili."""

    def __init__(self):
        self.raw_df = None        # Tabella letta dal file (senza righe/colonne vuote)
        self.features_df = None   # Solo variabili numeriche valide, senza NaN
        self.labels = []          # Etichette dei campioni, allineate a features_df
        self.warnings = []        # Dati esclusi o anomali, da mostrare all'utente

    # ------------------------------------------------------------------
    # Lettura file
    # ------------------------------------------------------------------
    def load_file(self, filepath: str) -> str:
        """Legge CSV o Excel. Ritorna "OK_DATA: ..." se riuscito, altrimenti
        un messaggio d'errore. In caso di errore lo stato non viene modificato."""
        if not os.path.exists(filepath):
            return "File non trovato."

        ext = os.path.splitext(filepath)[1].lower()

        try:
            if ext == ".csv":
                raw_df = self._read_csv(filepath)
            elif ext in (".xls", ".xlsx"):
                raw_df = pd.read_excel(filepath)
            else:
                return "Formato non supportato. Richiesto .CSV o .XLSX"

            return self._process_dataframe(raw_df)

        except Exception as e:
            return f"Errore di lettura del file: {e}"

    @staticmethod
    def _read_csv(filepath: str) -> pd.DataFrame:
        """Legge un CSV con separatore ',' o ';' e codifica UTF-8 o Windows-1252."""
        for encoding in ("utf-8-sig", "cp1252"):
            try:
                df = pd.read_csv(filepath, sep=',', encoding=encoding)
                if len(df.columns) <= 1:          # separatore probabile: ';'
                    df = pd.read_csv(filepath, sep=';', encoding=encoding)
                return df
            except UnicodeDecodeError:
                continue
        raise ValueError("codifica non riconosciuta (usare UTF-8 o Windows-1252)")

    @staticmethod
    def _to_numeric(serie: pd.Series) -> pd.Series:
        """Converte in numeri; ciò che non è convertibile diventa NaN.
        Accetta anche la virgola decimale ("1,5") e ignora gli spazi."""
        if not pd.api.types.is_numeric_dtype(serie):
            serie = serie.astype(str).str.strip().str.replace(',', '.', regex=False)
        conv = pd.to_numeric(serie, errors='coerce').astype(float)
        return conv.replace([np.inf, -np.inf], np.nan)

    # ------------------------------------------------------------------
    # Validazione
    # ------------------------------------------------------------------
    def _process_dataframe(self, raw_df: pd.DataFrame) -> str:
        """Separa etichette e variabili, esclude i dati non utilizzabili.
        Lo stato dell'oggetto viene aggiornato solo a validazione riuscita."""
        avvisi = []

        df = raw_df.dropna(axis=0, how='all').dropna(axis=1, how='all')
        if df.empty:
            return "Errore: il file non contiene dati elaborabili (vuoto)."

        # Etichette: colonna con "sample" nel nome, altrimenti la prima colonna
        cols_id = [c for c in df.columns if 'sample' in str(c).lower()]
        if cols_id:
            id_col = cols_id[0]
            labels = df[id_col].fillna("Campione_X").astype(str)
        else:
            id_col = df.columns[0]
            labels = df[id_col].fillna("Senza_ID").astype(str)
        work_df = df.drop(columns=[id_col])
        n_campioni_file, n_variabili_file = work_df.shape

        # 1) Conversione numerica di ogni colonna
        numeric_df = pd.DataFrame(
            {col: self._to_numeric(work_df[col]) for col in work_df.columns},
            index=work_df.index)

        # 2) Colonne senza alcun valore numerico (note, testo): ignorate
        col_testo = [c for c in numeric_df.columns if numeric_df[c].notna().sum() == 0]
        if col_testo:
            avvisi.append("Colonne senza valori numerici, ignorate: "
                          f"{_elenco(col_testo)}.")
            numeric_df = numeric_df.drop(columns=col_testo)

        # 3) Variabili con troppi valori mancanti: escluse
        frazione = numeric_df.isna().mean()
        col_scarse = frazione[frazione > MAX_FRAZIONE_MANCANTI].index.tolist()
        if col_scarse:
            dettaglio = _elenco(f"{c} ({frazione[c]:.0%})" for c in col_scarse)
            avvisi.append(f"Variabili escluse perché con oltre il "
                          f"{MAX_FRAZIONE_MANCANTI:.0%} di valori mancanti: {dettaglio}.")
            numeric_df = numeric_df.drop(columns=col_scarse)

        # 4) Celle di testo non numerico nelle variabili rimaste (es. "n.d.", "<0.1"):
        #    trattate come mancanti. Segnalate per capirne l'origine.
        celle_testo = []
        for col in numeric_df.columns:
            orig = work_df[col]
            non_valida = (numeric_df[col].isna() & orig.notna()
                          & (orig.astype(str).str.strip() != ""))
            for idx in orig.index[non_valida]:
                celle_testo.append(f"'{orig[idx]}' [{col}, campione {labels[idx]}]")
        if celle_testo:
            avvisi.append("Celle non numeriche trattate come valori mancanti: "
                          f"{_elenco(celle_testo, sep='; ')}.")

        # 5) Campioni con valori mancanti: esclusi (nessuna imputazione)
        incompleti = numeric_df.isna().any(axis=1)
        if incompleti.any():
            voci = []
            for idx in numeric_df.index[incompleti]:
                mancanti = numeric_df.columns[numeric_df.loc[idx].isna()]
                voci.append(f"{labels[idx]} (manca: {_elenco(mancanti)})")
            avvisi.append("Campioni esclusi perché con valori mancanti: "
                          f"{_elenco(voci, sep='; ')}.")
            numeric_df = numeric_df[~incompleti]
            labels = labels[~incompleti]

        # 6) Dati sufficienti per la PCA?
        n, p = numeric_df.shape
        if n < MIN_CAMPIONI or p < MIN_VARIABILI:
            return (f"Dati insufficienti dopo la verifica: restano {n} campioni e "
                    f"{p} variabili (ne servono almeno {MIN_CAMPIONI} e "
                    f"{MIN_VARIABILI}).\n" + "\n".join(avvisi))

        # Validazione riuscita: aggiornamento dello stato
        self.raw_df = df
        self.features_df = numeric_df.reset_index(drop=True)
        self.labels = labels.tolist()
        self.warnings = avvisi

        msg = f"OK_DATA: Caricati {n} campioni analizzabili con {p} variabili continue."
        if avvisi:
            msg += (f" Esclusi {_pl(n_campioni_file - n, 'campione', 'campioni')} e "
                    f"{_pl(n_variabili_file - p, 'variabile', 'variabili')} (vedi avviso).")
        return msg

    def has_data(self) -> bool:
        """True se sono presenti dati validi per l'analisi."""
        return self.features_df is not None and not self.features_df.empty