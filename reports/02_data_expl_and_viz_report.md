# 02_data_expl_and_viz — Report (EN + FR)
_Source: 02_data_expl_and_viz.ipynb_

# A. English Version

## 02 — Data Exploration, Cleaning, and Feature Engineering (NHANES 2021–2023)

This notebook performs the full exploratory and preprocessing pipeline on the curated NHANES dataset (`nhanes_selected_2021_2023.csv`). Its goal is to convert the raw merged dataset into a clean, consistent, model‑ready table: **`nhanes_ready.csv`**.

---

## 1. Loading and Initial Checks
- Imports: `pandas`, `numpy`, `matplotlib`, `seaborn`.
- Dataset loaded: 37 selected variables.
- No duplicated rows.
- Initial structure inspected with `df.info()`.

---

## 2. Missing Values Analysis
A complete NaN audit highlights severely missing variables:
- `ALQ121`
- `PAD790Q`, `PAD790U`
- `PAD800`
- `PAD810Q`, `PAD810U`
- `PAD820`

These columns are removed.

---

## 3. Dietary Variable Consolidation
NHANES provides two dietary recall days. Each DR1/DR2 pair is averaged to create a stable variable:
- Calories → `DRKCAL`
- Protein → `DRPROT`
- Sugars → `DRSUGR`
- Fiber → `DRFIBE`
- Total fat → `DRTFAT`
- Alcohol → `DRTALCO`
- Carbohydrates → `DRCARB`
- Water → `DRWATER`

All original DR1/DR2 columns are then removed.

---

## 4. Filtering Individuals
Rows lacking:
- cholesterol (`LBXTC`), or
- diabetes status (`DIQ010`)  
are removed.

---

## 5. Imputation and Smoking Variable Cleaning
### Median Imputation
Variables such as calories, macronutrients, BMI, waist, PA, and sleep are imputed with median values.

### Smoking (SMQ020)
Recoded into a clean binary feature `smoker`:
- 1 → smoker
- 0 → non‑smoker or unknown  
Original column removed.

---

## 6. Diabetes Target Cleaning
`DIQ010` is converted into `diabetes`:
- 1 → diabetic
- 0 → non / borderline
- 7 / 9 → removed  
Rows with unknown status are dropped.

---

## 7. Distribution Analysis and Log Transformations
- Histograms generated for all numeric variables.
- Skewness calculated.
- Ten skewed variables receive `log1p()` transformation, producing new `_log` columns.

---

## 8. Ethnicity One‑Hot Encoding
`RIDRETH3` is mapped to readable labels and fully one‑hot encoded:
- `ethnicity_MexicanAmerican`
- `ethnicity_OtherHispanic`
- `ethnicity_NonHispanicWhite`
- `ethnicity_NonHispanicBlack`
- `ethnicity_NonHispanicAsian`
- `ethnicity_OtherRace`

Original code removed.

---

## 9. Final Variable Conversions
Binary variables cast to `int`:  
`RIAGENDR`, `smoker`, `diabetes`.

---

## 10. Cholesterol Target Creation
A medical threshold is applied:
```
chol_high = 1  if LBXTC > 240
chol_high = 0  otherwise
```

A frequency barplot is generated.

---

## 11. Final Export
The final dataset is exported as:
```
nhanes_ready.csv
```

This file is ready for model training, feature importance, interpretability, and deployment.

---

# B. Version Française

## 02 — Exploration, Nettoyage et Ingénierie des Données (NHANES 2021–2023)

Ce notebook réalise l’ensemble du pipeline d’exploration, de nettoyage et de préparation avancée du dataset NHANES.  
Il produit le fichier final prêt pour la modélisation : **`nhanes_ready.csv`**.

---

## 1. Chargement et vérifications initiales
- Imports : `pandas`, `numpy`, `matplotlib`, `seaborn`.
- Dataset chargé : 37 variables sélectionnées.
- Aucun doublon.
- Structure initiale vérifiée via `df.info()`.

---

## 2. Analyse des valeurs manquantes
Des colonnes extrêmement incomplètes sont supprimées :
- `ALQ121`
- `PAD790Q`, `PAD790U`
- `PAD800`
- `PAD810Q`, `PAD810U`
- `PAD820`

---

## 3. Consolidation des données nutritionnelles
NHANES fournit deux jours de rappel alimentaire. Les variables DR1 et DR2 sont moyennées :
- Calories → `DRKCAL`
- Protéines → `DRPROT`
- Sucres → `DRSUGR`
- Fibres → `DRFIBE`
- Graisses → `DRTFAT`
- Alcool → `DRTALCO`
- Glucides → `DRCARB`
- Eau → `DRWATER`

Les colonnes sources sont retirées.

---

## 4. Filtrage des individus pertinents
Suppression des lignes sans :
- cholestérol (`LBXTC`),
- statut diabète (`DIQ010`).

---

## 5. Imputation et recodage tabac
### Imputation médiane
Toutes les variables continues manquantes sont imputées par la médiane.

### Recodage tabac (SMQ020)
Création d’une variable binaire `smoker` :
- 1 → fumeur
- 0 → non‑fumeur / inconnu  
La colonne d’origine est supprimée.

---

## 6. Nettoyage de la variable cible diabète
`DIQ010` devient la variable binaire `diabetes` :
- 1 → diabétique
- 0 → non / borderline
- 7 / 9 → supprimés  
Les individus au statut indéterminé sont retirés.

---

## 7. Distribution et transformations log
- Histogrammes générés.
- Asymétrie (skewness) mesurée.
- Dix variables fortement asymétriques reçoivent une transformation `log1p()`, créant des colonnes `_log`.

---

## 8. Encodage one‑hot de l’ethnie
`RIDRETH3` est mappée puis encodée en six colonnes :
- `ethnicity_MexicanAmerican`
- `ethnicity_OtherHispanic`
- `ethnicity_NonHispanicWhite`
- `ethnicity_NonHispanicBlack`
- `ethnicity_NonHispanicAsian`
- `ethnicity_OtherRace`

---

## 9. Conversion finale des variables binaires
`RIAGENDR`, `smoker`, `diabetes` convertis proprement en `int`.

---

## 10. Création de la variable cible cholestérol
Application du seuil médical :
```
chol_high = 1  si LBXTC > 240
chol_high = 0  sinon
```

Une visualisation de la distribution est générée.

---

## 11. Export final
Le dataset final, prêt pour la modélisation et le déploiement, est exporté sous :
```
nhanes_ready.csv
```

Il constitue la version nettoyée et structurée utilisée pour les prochaines étapes.

