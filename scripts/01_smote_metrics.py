import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

# Cargar datos
df = pd.read_csv('data/creditcard.csv') 

# Separar variables y etiqueta
X = df.drop('Class', axis=1)
y = df['Class']

# Separar ANTES de balancear
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f'Fraudes en entrenamiento ANTES de SMOTE: {sum(y_train == 1)}')

# Entrenar BASE
rf_base = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
rf_base.fit(X_train, y_train)
print('\n--- MODELO BASE (SIN SMOTE) ---')
print(confusion_matrix(y_test, rf_base.predict(X_test)))
print(classification_report(y_test, rf_base.predict(X_test)))

# Aplicar SMOTE
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
print(f'\nFraudes en entrenamiento DESPUES de SMOTE: {sum(y_train_smote == 1)}')

# Entrenar BALANCEADO
rf_smote = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
rf_smote.fit(X_train_smote, y_train_smote)
print('\n--- MODELO BALANCEADO (CON SMOTE) ---')
print(confusion_matrix(y_test, rf_smote.predict(X_test)))
print(classification_report(y_test, rf_smote.predict(X_test)))
