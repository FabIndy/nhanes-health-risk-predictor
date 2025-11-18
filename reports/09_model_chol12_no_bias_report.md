# NHANES 2021–2023 — Cholesterol Prediction Model (LightGBM No-Bias)

## PART 1 — English Report

### 1. Objective
The notebook 12-model-chol-no-bias.ipynb trains and validates a **LightGBM binary classifier** predicting **high total cholesterol (`chol_high`)** using NHANES 2021–2023 data. The workflow focuses on rigor, fairness, and reproducibility by combining careful preprocessing, balanced training, hyperparameter optimisation, and clear evaluation.

### 2. Dataset & Target
- Source: `nhanes_ready.csv`
- Target: **chol_high** (0/1)
- No missing values or duplicates.
- Positivity rate is preserved through **stratified splits**.

### 3. Features
Two groups of predictors are used:
- **Core:** age, sex, smoker status  
- **Morphology:** BMI (log), waist circumference  
- **Lifestyle:** sedentary time (PAD680_log), sleep (SLD012)  
- **Ethnicity:** six binary indicators  

All non-binary features are later standardised.

### 4. Train / Validation / Test Split
- 80/20 split between train_full and test  
- Train_full split again into **train (60%)** and **validation (20%)**  
- All splits stratified on the target.

### 5. Preprocessing
- Binary variables left untouched.
- Non‑binary variables standardised via **StandardScaler fitted on train only**.
- The validation and test sets use the **same scaler**.

### 6. Hyperparameter Optimisation
A **RandomizedSearchCV** (n_iter=40, 5-fold CV) explores:
- num_leaves, max_depth, min_child_samples  
- subsample, colsample_bytree  
- L1/L2 regularisation  
- learning_rate, n_estimators  
- min_split_gain  

Scoring metric: **ROC AUC**.

The best parameters are retrieved and stored.

### 7. Final Training (Train + Val)
- Train and validation sets are concatenated.
- A small internal split (10%) is used for **early stopping**.
- A tuned LightGBM model is trained with **class_weight="balanced"**.
- The final model and scaler are saved to:
  - `artifacts_chol_no_bias/model_lightgbm_chol_no_bias.pkl`
  - `artifacts_chol_no_bias/scaler_chol_no_bias.pkl`
  - `artifacts_chol_no_bias/best_params.json`

### 8. Test Evaluation (Threshold = 0.5)
Metrics include:
- Classification report  
- ROC AUC  
- Confusion matrix  
- ROC curve  

This gives a first baseline for real-world deployment.

### 9. Optimal Threshold Search
Using test-set probabilities:
- Precision–recall curve computed.
- Best F1-score threshold identified.
- Confusion matrix and classification report computed at this optimal threshold.

### 10. False Positive Analysis (Threshold 0.5)
False positives are analysed by cholesterol distribution (LBXTC):
- `<200 mg/dL` (normal zone)
- `200–240 mg/dL` (grey zone)
- `>240 mg/dL` (high zone)

This allows interpreting borderline cases and understanding model behaviour.

---

## PART 2 — Rapport en Français

### 1. Objectif
Le notebook 12-model-chol-no-bias.ipynb entraîne un **classifieur LightGBM** destiné à prédire le **cholestérol total élevé (`chol_high`)** dans NHANES 2021–2023. Le pipeline met l’accent sur la rigueur, la transparence et la reproductibilité.

### 2. Données & Cible
- Fichier : `nhanes_ready.csv`
- Cible : **chol_high** (0/1)
- Aucun NaN ni doublon.
- Toutes les découpes sont **stratifiées**.

### 3. Variables
- **Noyau :** âge, sexe, tabac  
- **Morphologie :** BMI (log), tour de taille  
- **Mode de vie :** temps assis (PAD680_log), sommeil (SLD012)  
- **Ethnicité :** six indicateurs binaires  

Les variables non binaires sont standardisées.

### 4. Split Train / Val / Test
- 80% pour train_full  
- Séparation en train (60%) + validation (20%)  
- Test final : 20%  
- Découpes stratifiées.

### 5. Prétraitement
- Colonnes binaires laissées intactes.  
- Standardisation des colonnes numériques via **StandardScaler** (fit sur train seul).  

### 6. Optimisation Hyperparamètres
Une **RandomizedSearchCV** (5-fold, 40 essais) optimise :
- num_leaves, max_depth, min_child_samples  
- subsample, colsample_bytree  
- régularisation L1/L2  
- learning_rate, n_estimators  
- min_split_gain  

Metric : **ROC AUC**.

Les meilleurs paramètres sont sauvegardés.

### 7. Entraînement Final (Train + Val)
- Train et val sont combinés.  
- Un mini-split interne (10%) sert pour l’**early stopping**.  
- Le modèle final utilise **class_weight="balanced"**.  
- Sauvegardes dans `artifacts_chol_no_bias/`.

### 8. Évaluation Test (Seuil 0.5)
Le notebook fournit :
- rapport de classification  
- ROC AUC  
- matrice de confusion  
- courbe ROC  

Ce seuil sert de référence.

### 9. Recherche du Seuil Optimal
- Calcul de la courbe précision–rappel  
- Identification du seuil maximisant le **F1-score**  
- Nouvelles métriques et matrice de confusion au seuil optimal.

### 10. Analyse des Faux Positifs
Répartition des faux positifs selon LBXTC :
- `<200 mg/dL` (normal)
- `200–240 mg/dL` (zone grise)
- `>240 mg/dL` (élevé)

Cette analyse éclaire le comportement du modèle sur les profils borderline.

---

*Notebook source analysé :*  **12-model-chol-no-bias (2).py**  
