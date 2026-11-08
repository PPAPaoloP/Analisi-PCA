"""
/**
 *  @file       data_handler.py
 *  @brief      Gestore Dati tramite Pandas per Input/Output ed Estrazione Features.
 *
 *  @details
 *              Carica in modo sicuro file .CSV o fogli Excel. Separa le 
 *              variabili analitiche continue (elementi chimici e granulometria)
 *              dalle etichette/stringhe testuali del campione, pronte ad essere 
 *              pompate nell'elaborazione matematica PCA.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-07
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import os
import pandas as pd
import numpy as np

class DataHandler:
    """Caricamento, partizionamento testuale/numerico e pulizia dei DataFrames."""

    def __init__(self):
        # Memoria Grezza (Dataframe originario per futuri riferimenti esportativi)
        self.raw_df = None
        
        # Sotto-insiemi strutturati pronti per la Big Data Analysis
        self.features_df = None   # Solo colonne rigorosamente numeriche
        self.labels = []          # Le "targhette testuali" (Nome dei campioni, orizzonti etc.)

    def load_file(self, filepath: str) -> str:
        """
        Interpreta CSV o Excel dipendentemente dall'estensione del Path selezionato.
        Ritorna una stringa col messaggio di status ("Ok" se successo) per il feedback GUI.
        """
        if not os.path.exists(filepath):
            return "File non trovato."

        ext = os.path.splitext(filepath)[1].lower()

        try:
            if ext == ".csv":
                # Carica CSV cercando di decifrare separatori standard (virgola o punto e virgola)
                # Fallback utile per esportazioni europee vs anglosassoni
                try:
                    self.raw_df = pd.read_csv(filepath, sep=',')
                    # Verifica sicurezza (se legge tutta una stringa enorme senza splittare le colonne)
                    if len(self.raw_df.columns) <= 1:
                        self.raw_df = pd.read_csv(filepath, sep=';')
                except Exception as ex_csv:
                    return f"Errore decodifica file CSV: {ex_csv}"
            elif ext in [".xls", ".xlsx"]:
                self.raw_df = pd.read_excel(filepath)
            else:
                return "Formato non supportato. Richiesto .CSV o .XLSX"

        except Exception as e:
            return f"Data parser fault generico: {e}"

        return self._process_dataframe()

    def _process_dataframe(self) -> str:
        """Estrae le features matematiche dalle Label dei Sample. Ripara e controlla integrità dati."""
        
        # Eliminiamo rigorosamente Colonne e Righe composte per il 100% da campi vuoti "NaN" (Not a Number)
        self.raw_df = self.raw_df.dropna(axis=0, how='all')
        self.raw_df = self.raw_df.dropna(axis=1, how='all')

        if self.raw_df.empty:
            return "Errore: Il dataset estratto appare privo di dati elaborabili (Empty)."

        # SEPARAZIONE LOGICA DATA SCIENCE: Identificare la colonna nominale o Etichette:
        # Se esiste una colonna col termine 'Sample' (insensible) usala come base etichette:
        possible_id_cols = [c for c in self.raw_df.columns if 'sample' in str(c).lower()]
        if len(possible_id_cols) > 0:
            id_col_name = possible_id_cols[0]
            self.labels = self.raw_df[id_col_name].fillna("Campione_X").astype(str).tolist()
            work_df = self.raw_df.drop(columns=[id_col_name])
        else:
            # Assumiamo come "Label testuale" la prima primissima colonna
            first_col = self.raw_df.columns[0]
            self.labels = self.raw_df[first_col].fillna(f"Senza_ID").astype(str).tolist()
            work_df = self.raw_df.drop(columns=[first_col])

        # Forza l'estrazione SOLO della roba numerica convertendo campi malmessi
        # in un vero NumPy NaN per saltarli brutalmente invece che abortire il SW:
        self.features_df = work_df.apply(pd.to_numeric, errors='coerce')
        
        # (Futura ottimizzazione PCA) Eliminazione variabili scartate o campioni non utilizzabili 
        # perché presentano 100% dati sporchi anche sulle costanti.
        
        cols_count = len(self.features_df.columns)
        rows_count = len(self.labels)

        return f"OK_DATA: Caricati {rows_count} campioni analizzabili con {cols_count} features (Variabili Continue)."

    def has_data(self) -> bool:
        """Polso diagnostico."""
        return self.features_df is not None and not self.features_df.empty