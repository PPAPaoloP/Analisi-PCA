"""
/**
 *  @file       pca_engine.py
 *  @brief      Motore di calcolo per l'Analisi delle Componenti Principali (PCA).
 *
 *  @details
 *              Standardizzazione opzionale delle variabili e PCA a 3 componenti
 *              tramite scikit-learn. Il motore non conserva stato tra le chiamate:
 *              ogni fit_transform() ricrea i modelli e lavora su una copia dei
 *              dati, quindi il risultato dipende solo da input e parametri.
 *
 *  @version    1.0.0
 *  @author     Ing. Paolo Parrino
 *  @date       2026-11-08
 *
 *  @copyright  Copyright (c) 2026 Ing. Paolo Parrino.
 *              All rights reserved - CONFIDENTIAL.
 */
"""

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class PCAEngine:
    """Calcola la PCA (3 componenti) su una tabella di variabili numeriche."""

    def __init__(self):
        self.pca = None            # Modello sklearn PCA (ricreato a ogni calcolo)
        self.scaler = None         # StandardScaler (ricreato a ogni calcolo)

        self.scores = None         # Coordinate dei campioni sulle PC     (n x 3)
        self.loadings = None       # Pesi delle variabili su ogni PC      (p x 3)
        self.variance = [0.0, 0.0, 0.0]  # Varianza spiegata da PC1..PC3 [%]
        self.feature_names = []    # Nomi delle variabili (colonne)

    def fit_transform(self, df: pd.DataFrame, standardize: bool = True) -> bool:
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

        return True