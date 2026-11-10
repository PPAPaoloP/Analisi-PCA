"""
/**
 *  @file       pca_engine.py
 *  @brief      Motore algebrico per Principal Component Analysis (Scikit-Learn).
 *
 *  @details
 *              Standardizza i dati in input ed implementa riduzione PCA. 
 *              Ad ogni nuova tracciatura (click / update di cursori UI) 
 *              assicura lo snapshotting immacolato in ram sbloccando determinismi 
 *              algebrici (impedendo specularità Random sulle assi Autovettore 2D 
 *              sostituendo memoria dinamica e cache). 
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

import hashlib

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class PCAEngine:
    """Implementazione dell'algoritmo di decomposizione multivariata (Scikit-Learn)"""
    def __init__(self):
        # Inizializziamo a zero/vuoto le tracce rimaste
        self.pca = None                       # PCA(n_components=3) # Consente accesso logico all'Autovettore PC3!
        self.scaler = None                    # StandardScaler()
        
        # Array NumPy finali 
        self.scores = None         # Coordinata x,y per ogni campione (row)
        self.loadings = None       # Peso e direzione (x,y) per ogni feature/colonna
        self.variance = [0.0, 0.0] # Spiegazione varianza [%] di PC1 e PC2
        self.feature_names = []    # Mappatura etichette vettori

    def fit_transform(self, df: pd.DataFrame, standardize: bool = True) -> bool:
        """Esegue fit statistico garantendo intoccabilità file sorgenti e blocca segni-assi a rigidi calcoli (solver=full) deterministico."""
        if df is None or df.empty:
            return False
       
        # @PP Debug section
        '''
        h = pd.util.hash_pandas_object(df, index=True).sum()
        print(f"[PCA] std={standardize} shape={df.shape} hash={h} cols={list(df.columns)[:5]}")
        '''

        # Ancoraggio etichetta features (metalli/esami terreno in array nomi testuale es [Sostanza_Alpha..]) 
        self.feature_names = df.columns.tolist()
        

        # ==============================================================
        # CORE 1: SIGILLO ANTI INVERSIONI ASSE SPECULARI E ISOLAMENTO MATRICE IN RAM
        # ==============================================================
        # Obbliga Scikit (che in Backend C++ scompone iterativamente tramite metodi stocastici come arpack se lasciato decidere da se stesso) 
        # a NON "scegliere Randomicamente o Euristicamente" invertendo asse XY nei Pareggi Parimerito Varianziali: RandomSeed+Full
        self.pca = PCA(n_components=3, svd_solver='full', random_state=42)

        # Si preprara allo scaling rigenerando uno scheletro nuovo anch'esso! (L'omissione di questa istruzione era il famoso NullPointerException di riga 55 poc'anzi!)
        self.scaler = StandardScaler(copy=True)
        
        # Crea Fotocopia isolata dell'astronave Dati Matrice. Disaccoppia Pandas e Scikit dalla tabella GUI salvata su DBase 
        data_matrix = np.array(df.values, dtype=float, copy=True)

        # ==============================================================
        # CORE 2: SINTESI DISTANZIALE NORMALIZZATIVA  
        # ==============================================================
        if standardize:
            # Equazione 1: Prende deviazioni differite del peso atomico/percentuali equiparandone e stirandole equamente a Forza Zero Media Varianza 1 assoluto globale per tutte X Features. 
            data_matrix = self.scaler.fit_transform(data_matrix)
        else:
            # Equazione 2 (Cruda/Raw data senza pesi pareggiati): 
            # Non standardizza a 1 lo schiacciamento; ma Sottrae geometricamente sempre centro Origine Asse Spazio 3D dal Vettore spostandolo esattamente sull'origine grafico per poterlo Plotizzare con origini baricentriche vere Matplotlib . 
            data_matrix = data_matrix - np.mean(data_matrix, axis=0)

        # ==============================================================
        # CORE 3: ACCENDI MOTORE RISOLUTIVO  
        # ==============================================================
        
        # Mappa i Suoli Campione (N) schiacciandoli per punti Cardinali Scatter nello spazio cartesiano asse-vincitori.  (Coordinate Scatter Plot PC1..PCN). 
        self.scores = self.pca.fit_transform(data_matrix)
        
        # I Vettori Direzionali: Orientamento puro pesi direzioni Loadings Traspone C[][] in Array Unidimensionali  .  
        self.loadings = self.pca.components_.T 
        
        # Fattori descrittivi accuratezza modello e potenza in se. (Le label assi '%', salvata e proiettabile!).
        self.variance = self.pca.explained_variance_ratio_ * 100
        
        # @PP Debug
        '''
        np.set_printoptions(precision=6, suppress=True)
        print(f"[PCA] std={standardize}")
        print("loadings:\n", self.loadings)
        print("var%:", self.variance)
        print("scores:\n", self.scores)
        '''

        return True

    