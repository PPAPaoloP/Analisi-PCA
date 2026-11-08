"""
/**
 *  @file       pca_engine.py
 *  @brief      Motore algebrico per Principal Component Analysis (Scikit-Learn).
 *
 *  @details
 *              Standardizza i dati in input e implementa la riduzione
 *              dimensionale a due componenti (PC1 e PC2). Restituisce 
 *              coordinate campioni, coordinate vettoriali (loadings) 
 *              e relative percentuali di varianza descritta.
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
    """Implementazione dell'algoritmo di decomposizione multivariata."""
    def __init__(self):
        self.pca = PCA(n_components=3) # Consente accesso logico all'Autovettore PC3!
        self.scaler = StandardScaler()
        
        # Array NumPy finali 
        self.scores = None         # Coordinata x,y per ogni campione (row)
        self.loadings = None       # Peso e direzione (x,y) per ogni feature/colonna
        self.variance = [0.0, 0.0] # Spiegazione varianza [%] di PC1 e PC2
        self.feature_names = []    # Mappatura etichette vettori

    def fit_transform(self, df: pd.DataFrame, standardize: bool = True) -> bool:
        """Esegue fit statistico calcolando matrice covarianze ed autovettori."""
        if df is None or df.empty:
            return False

        self.feature_names = df.columns.tolist()
        data_matrix = df.values

        # La standardizzazione azzera le disparità di scala numerica (es. percentuale vs grammi/Kg)
        if standardize:
            data_matrix = self.scaler.fit_transform(data_matrix)
        else:
            # Centra in ogni caso i dati intorno alla media senza normalizzare varianze
            data_matrix = data_matrix - np.mean(data_matrix, axis=0)

        # 1. Coordinate finali Punti 2D
        self.scores = self.pca.fit_transform(data_matrix)
        
        # 2. Direzione vettoriale degli originari assi feature
        # (Coefficienti delle componenti linearizzate normalizzati)
        self.loadings = self.pca.components_.T 
        
        # 3. Informazioni ritenzione diagnostiche (es. PC1 descrive 70% realtà)
        self.variance = self.pca.explained_variance_ratio_ * 100

        return True