# NHANES 2021–2023 Dataset Construction (English)

The notebook 01_import_clean.ipynb prepares the base dataset used to train models predicting diabetes and high cholesterol from a representative sample of the U.S. population (NHANES 2021–2023).  
Its purpose is to:
- merge demographic, clinical, nutritional, sleep, physical activity and smoking data,
- keep only a curated set of relevant features,
- export a unified CSV file for downstream notebooks.

---

## 1. Imports and Setup
Imports: `pandas`, `numpy`.  
Display configuration: `max_columns = 100`.  
Environment check message confirming that imports are successful.

---

## 2. Loading NHANES Files (2021–2023)

Ten SAS XPORT `.xpt` files are read using `pd.read_sas`:
- Demographics  
- Diet Day 1  
- Diet Day 2  
- Body Measures  
- Total Cholesterol  
- Diabetes Questionnaire  
- Physical Activity  
- Alcohol  
- Sleep  
- Smoking  

All tables are loaded with `encoding="latin1"` and their dimensions are displayed.

---

## 3. Merging the 10 Tables into a Single DataFrame

The tables are merged step by step using the common identifier `SEQN`:

```python
df = (demo
      .merge(diet1, on="SEQN", how="left")
      .merge(diet2, on="SEQN", how="left")
      .merge(bmx,  on="SEQN", how="left")
      .merge(chol, on="SEQN", how="left")
      .merge(diq,  on="SEQN", how="left")
      .merge(paq,  on="SEQN", how="left")
      .merge(alq,  on="SEQN", how="left")
      .merge(slq,  on="SEQN", how="left")
      .merge(smq,  on="SEQN", how="left"))
```

Left joins ensure all individuals from the demographic file are retained even when some questionnaires are missing.

---

## 4. Selecting Relevant Variables

A curated list of 37 variables is kept, covering:
- **Demographics:** age, sex, ethnicity  
- **Biological markers:** total cholesterol `LBXTC`  
- **Diabetes status:** `DIQ010`  
- **Anthropometry:** BMI, waist, weight, height, etc.  
- **Nutrition (Day 1 & Day 2):** calories, protein, sugars, fiber, fats, alcohol, carbs  
- **Alcohol frequency:** `ALQ121`  
- **Physical activity:** PAD680, PAD790Q/U, PAD800, PAD810Q/U, PAD820  
- **Sleep:** `SLD012`  
- **Smoking:** `SMQ020`  

Missing columns are identified and reported.  
A filtered DataFrame `df_selected` is created and its dimensions verified.

---

## 5. Exporting the Dataset

The selected dataset is exported:

```python
df_selected.to_csv("nhanes_selected_2021_2023.csv", index=False)
```

This CSV is the standard input for all forthcoming notebooks (cleaning, feature engineering, modeling, deployment).

---

## 6. Role in the Project

This notebook:
- consolidates 10 NHANES sources into a single DataFrame,
- keeps only medically meaningful variables,
- provides a reproducible entry point for the full modeling pipeline.

It does not yet perform cleaning or modeling, but ensures the entire project starts from a consistent, standardized dataset.

---

# Construction du jeu de données NHANES 2021–2023 (Français)

Ce notebook prépare le jeu de données utilisé pour entraîner les modèles de prédiction du diabète et du cholestérol élevé à partir d’un échantillon représentatif de la population américaine (NHANES 2021–2023).  
Objectifs :
- fusionner les données démographiques, cliniques, nutritionnelles, sommeil, activité physique et tabac,
- ne garder qu’un ensemble pertinent de variables,
- exporter un fichier CSV unique pour la suite du pipeline.

---

## 1. Imports et configuration
Imports : `pandas`, `numpy`.  
Configuration de l’affichage (`max_columns = 100`).  
Message confirmant que l’environnement est prêt.

---

## 2. Lecture des fichiers NHANES (2021–2023)

Dix fichiers SAS XPORT `.xpt` sont lus :
- Démographie  
- Alimentation jour 1  
- Alimentation jour 2  
- Mesures corporelles  
- Cholestérol total  
- Questionnaire diabète  
- Activité physique  
- Alcool  
- Sommeil  
- Tabac  

Les dimensions de chaque table sont affichées.

---

## 3. Fusion des 10 tables dans un DataFrame unique

Fusion progressive via `SEQN` :

```python
df = (demo
      .merge(diet1, on="SEQN", how="left")
      .merge(diet2, on="SEQN", how="left")
      .merge(bmx,  on="SEQN", how="left")
      .merge(chol, on="SEQN", how="left")
      .merge(diq,  on="SEQN", how="left")
      .merge(paq,  on="SEQN", how="left")
      .merge(alq,  on="SEQN", how="left")
      .merge(slq,  on="SEQN", how="left")
      .merge(smq,  on="SEQN", how="left"))
```

Jointures `left` pour conserver tous les individus du fichier démographique.

---

## 4. Sélection des variables pertinentes

Un ensemble de 37 variables est retenu :  
- **Démographie :** âge, sexe, ethnie  
- **Biologie :** cholestérol total `LBXTC`  
- **Diabète :** `DIQ010`  
- **Anthropométrie :** taille, poids, IMC, tour de taille…  
- **Nutrition (jour 1 & 2) :** calories, protéines, sucres, fibres, graisses, alcool, glucides  
- **Alcool (fréquence) :** `ALQ121`  
- **Activité physique :** PAD680, PAD790Q/U, PAD800, PAD810Q/U, PAD820  
- **Sommeil :** `SLD012`  
- **Tabac :** `SMQ020`  

Les colonnes manquantes sont identifiées.  
Un DataFrame filtré `df_selected` est créé.

---

## 5. Export du jeu de données

```python
df_selected.to_csv("nhanes_selected_2021_2023.csv", index=False)
```

Ce fichier CSV est le point d’entrée standard pour le nettoyage, l’ingénierie des données et les modèles.

---

## 6. Rôle dans le projet

Ce notebook :
- consolide 10 sources NHANES dans un seul DataFrame,
- sélectionne les variables cliniquement pertinentes,
- fournit un point de départ reproductible pour tout le pipeline.

Il ne réalise pas encore le nettoyage ni la modélisation, mais garantit un socle cohérent et standardisé pour toute la suite.

