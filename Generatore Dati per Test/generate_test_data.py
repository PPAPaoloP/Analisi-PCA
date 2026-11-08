import pandas as pd
import numpy as np
import os

def create_synthetic_soil(filename, n_samples, sample_prefix, means_dict):
    cols = ['Sample','Fe (g/kg)','Cu (g/kg)','Zn (g/kg)','V (g/kg)','Cr (g/kg)',
            'Al (g/kg)','Si (g/kg)','Mn (g/kg)','Ti (g/kg)','Ca (g/kg)','K (g/kg)',
            'Fe(d) (g/kg)','Fe(ox) (g/kg)','Al(d) (g/kg)','Al(ox) (g/kg)',
            'sand(%)','silt(%)','clay(%)']
    
    data = {}
    data['Sample'] = [f"{sample_prefix}-{i+1}" for i in range(n_samples)]
    
    # Inietta un "disturbo" per generare valori veritieri coi numeri gaussiani 
    for col in cols[1:]:
        mean_val = means_dict.get(col, 10.0) # Se dimentico di assegnare, di default media 10
        # Aggiunge +/- 10-15% di disturbo attorno alla media:
        noise = np.random.normal(loc=mean_val, scale=mean_val*0.15, size=n_samples) 
        # Per la composizione, forziamo il valore maggiore di zero (np.clip):
        data[col] = np.round(np.clip(noise, 0.1, None), 2)
        
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[{filename}] Generato con successo ({n_samples} righe)!")

# Generiamo! 
# Orizzonte A (Superficie): Tanta Sabbia (sand%), scarso in argilla (clay)
create_synthetic_soil("Test_Orizzonte_A_Top.csv", 20, "A01", {
    'sand(%)': 65.0, 'silt(%)': 20.0, 'clay(%)': 15.0, 'Fe (g/kg)': 25.0, 'Cu (g/kg)': 12.0
})
# Orizzonte B (Profondo): Elevato in Ossidi di Ferro e Alluminio (Fe(ox), Al(ox)), media argilla.
create_synthetic_soil("Test_Orizzonte_B_Mid.csv", 20, "B02", {
    'sand(%)': 35.0, 'silt(%)': 25.0, 'clay(%)': 40.0, 'Fe (g/kg)': 85.0, 'Fe(ox) (g/kg)': 45.0, 'Al(ox) (g/kg)': 30.0
})
# Orizzonte C e D (Rocciosi): Moltissimo Silicio (Si), Titanio, Calcio. Niente sostanza morbida
create_synthetic_soil("Test_Orizzonte_C_Base.csv", 18, "C03", {
    'sand(%)': 80.0, 'silt(%)': 10.0, 'clay(%)': 10.0, 'Si (g/kg)': 400.0, 'Ca (g/kg)': 250.0, 'K (g/kg)': 100.0
})
create_synthetic_soil("Test_Orizzonte_D_Rock.csv", 12, "D04", {
    'sand(%)': 85.0, 'silt(%)': 10.0, 'clay(%)': 5.0, 'Si (g/kg)': 650.0, 'Ti (g/kg)': 85.0, 'Mn (g/kg)': 35.0
})