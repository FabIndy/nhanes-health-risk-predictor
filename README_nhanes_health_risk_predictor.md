# NHANES Health risk predictor  
Comprehensive metabolic-risk prediction using NHANES 2021–2023  
(Part 1: English — Part 2: Français)

---

# Part 1 — README (English)

## Project overview

This repository contains a complete end-to-end project using the U.S. NHANES 2021–2023 dataset to build two preventive machine-learning models:

1. A model predicting the **risk of diabetes**
2. A model predicting the **risk of high total cholesterol**

Both models are trained exclusively on simple, non-invasive variables collected by NHANES. They are deployed together in a single, easy-to-use application available on Hugging Face:  
https://huggingface.co/spaces/FabIndy/Health-risk-predictor

The goal of the project is prevention. The models act as early-warning tools capable of detecting risk profiles among individuals who may appear healthy.

---

## Dataset

The project uses publicly available data from **NHANES 2021–2023**, produced by the U.S. Centers for Disease Control and Prevention (CDC).  
Several NHANES components were merged:

- demographics  
- body measures  
- cholesterol and diabetes questionnaires  
- sleep  
- physical activity  
- smoking  
- diet and alcohol  
- laboratory metabolic markers

Transformations applied:

- log transformation of skewed measures (BMI → `BMXBMI_log`, sitting time → `PAD680_log`)
- harmonisation and cleaning of categorical variables
- one-hot encoding for ethnicity
- standardisation of numerical features
- stratified train/validation/test split

---

## Features required by the app

The Hugging Face app only asks for nine simple user inputs:

1. age  
2. sex  
3. smoking status  
4. weight  
5. height  
6. waist circumference  
7. sleep duration  
8. sitting time  
9. ethnicity

Internal transformations:

- BMI is computed from weight and height, then transformed into `BMXBMI_log`
- sitting time is transformed into `PAD680_log`
- ethnicity is one-hot encoded
- numerical features are standardised using saved scalers
- the final feature order matches the training pipeline exactly

---

## Models

Two LightGBM classifiers were optimised with thresholds chosen to maximise recall on the pathological class while maintaining reasonable precision:

- diabetes model: threshold = **0.40**
- high-cholesterol model: threshold = **0.35**

SHAP analyses, threshold selection and FN/FP analyses are available in the `reports/` directory.

---

## Performance (test set)

Key screening metrics:

- **false-negative rate (FN)**: proportion of truly sick individuals missed  
- **RFP rate** (“Really False Positives”): proportion of truly healthy individuals incorrectly alerted

### Diabetes model  
- FN rate: **11.6%**  
- RFP rate: **30.7%**

### High-cholesterol model  
- FN rate: **13.8%**  
- RFP rate: **33%**

---

## Intended use

These models are designed for preventive contexts:

- companies / HR wellness programmes  
- community centres  
- primary-care structures  
- medical or paramedical staff  
- schools or universities  
- sports or fitness settings  

They are not diagnostic tools but early-warning screening tools.

---

## Repository structure (GitHub)

```
nhanes_health_risk_predictor/
│
├── Health-risk-predictor/
├── models/
├── notebooks/
├── Pages_html/
├── reports/
│
├── nhanes_env.yml
└── README_nhanes_health_risk_predictor.md
```

## Structure of the Hugging Face application

```
Health-risk-predictor/
│
├── .git/
├── artifacts_chol_no_bias/
├── artifacts_diab_no_bias/
├── .gitattributes
├── app.py
├── README.md
└── requirements.txt
```

---

# Part 2 — README (Français)

## Présentation du projet

Ce dépôt contient un projet complet basé sur la base **NHANES 2021–2023**, visant à construire deux modèles de machine learning destinés à la prévention :

1. un modèle de prédiction du **risque de diabète**
2. un modèle de prédiction du **risque de cholestérol total élevé**

Ces modèles reposent uniquement sur des données simples et non invasives.  
Ils sont déployés ensemble dans une application très simple d’utilisation :  
https://huggingface.co/spaces/FabIndy/Health-risk-predictor

---

## Données

Les données proviennent de l’étude publique NHANES 2021–2023 (CDC).  
Plusieurs modules ont été fusionnés :

- démographie  
- mesures corporelles  
- questionnaires diabète et cholestérol  
- sommeil  
- activité physique  
- tabac  
- alimentation / alcool  
- biomarqueurs métaboliques

Transformations appliquées :

- log-transformations (`BMXBMI_log`, `PAD680_log`)
- harmonisation des catégories
- encodage one-hot pour l’ethnie
- standardisation des variables numériques
- division stratifiée train/validation/test

---

## Variables demandées dans l’application

L’application demande neuf variables simples :

1. âge  
2. sexe  
3. statut fumeur  
4. poids  
5. taille  
6. tour de taille  
7. durée de sommeil  
8. temps assis  
9. ethnie

L’IMC est ensuite calculé automatiquement puis transformé, et les autres variables sont traitées pour correspondre exactement au pipeline d’entraînement.

---

## Modèles

Deux modèles LightGBM ont été optimisés, avec une recherche de seuil visant à maximiser le recall sur la classe pathologique tout en maintenant une précision correcte :

- modèle diabète : seuil = **0.40**
- modèle cholestérol : seuil = **0.35**

---

## Performances (jeu de test)

- **taux de faux négatifs (FN)**  
- **taux de personnes réellement saines alertées à tort (RFP)**

### Modèle diabète  
- FN = **11.6 %**  
- RFP = **30.7 %**

### Modèle cholestérol  
- FN = **13.8 %**  
- RFP = **33 %**

Ces résultats sont cohérents avec un outil de dépistage préventif reposant uniquement sur des données simples.

---

## Public cible

Ces modèles peuvent être utilisés dans :

- les entreprises  
- les centres sociaux  
- les cabinets médicaux  
- les structures paramédicales  
- les établissements scolaires / universitaires  
- les clubs sportifs  

Ils servent de **premier niveau de détection**, sans vocation diagnostique.

---

## Architecture du dépôt GitHub

```
nhanes_health_risk_predictor/
│
├── Health-risk-predictor/
├── models/
├── notebooks/
├── Pages_html/
├── reports/
│
├── nhanes_env.yml
└── README_nhanes_health_risk_predictor.md
```

## Architecture du dossier Hugging Face

```
Health-risk-predictor/
│
├── .git/
├── artifacts_chol_no_bias/
├── artifacts_diab_no_bias/
├── .gitattributes
├── app.py
├── README.md
└── requirements.txt
```
