import pandas as pd
from faker import Faker
import random

# Inicializamos Faker con el locale de Chile para generar RUTs válidos
fake = Faker('es_CL')

def simular_features_pacs008(n_records=500):
    datos = []
    bancos = ['Banco de Chile', 'Santander', 'BCI', 'BancoEstado', 'Scotiabank', 'Itaú']
    
    for _ in range(n_records):
        datos.append({
            'MsgId': fake.uuid4(),                                    # ID del mensaje
            'CreDtTm': fake.date_time_between(start_date='-7d', end_date='now').isoformat(), # Timestamp
            'InstdAmt': round(random.uniform(5000, 2500000), 0),      # Monto
            'Dbtr_Id': fake.rut(),                                    # RUT Origen
            'Dbtr_Agt': random.choice(bancos),                        # Banco Origen
            'Cdtr_Id': fake.rut(),                                    # RUT Destino
            'Cdtr_Agt': random.choice(bancos),                        # Banco Destino
            'is_fraud': random.choices([0, 1], weights=[0.98, 0.02])[0] # 2% de fraude simulado
        })
    return pd.DataFrame(datos)

if __name__ == '__main__':
    print("Generando dataset aplanado basado en etiquetas pacs.008...")
    df = simular_features_pacs008(1000)
    
    # Lo guardamos en tu carpeta data
    output_path = '../data/dataset_transferencias.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Listo. 1000 transferencias guardadas en: {output_path}")
    print(df.head())
