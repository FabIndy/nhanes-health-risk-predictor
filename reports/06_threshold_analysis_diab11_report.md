# Threshold Optimization for Diabetes Model (Notebook 11) — EN + FR  
_Source: 16-threshold-analysis-diab-11.ipynb_

---

# A. English Version

## Objective
This notebook analyzes multiple decision thresholds for the **diabetes model from Notebook 11** (the no-bias LightGBM model).  
The goal is to identify a threshold that **maximizes recall for the pathological class (diabetes = 1)** while maintaining **acceptable precision**, ensuring a clinically relevant compromise between:

- **minimizing false negatives** (critical for screening),  
- **controlling false positives** (important for usability).  

The analysis evaluates thresholds from **0.05 to 0.90** and compares their performance.

---

## 1. Model and Data Loading
The notebook loads:
- the tuned LightGBM model: `model_lightgbm_diab_no_bias.pkl`
- the fitted scaler: `scaler_diab_no_bias.pkl`
- the held‑out test split (`X_test_chol.csv`, `y_test_chol.csv`)

The numeric variables are scaled consistently with the training phase, and prediction probabilities are computed.

---

## 2. Threshold Evaluation
For each threshold in {0.05, 0.10, …, 0.90}, the notebook computes:
- predicted labels,  
- precision and recall for each class,  
- the full classification report,  
- the confusion matrix.

All results are compiled into a summary table.

---

# 3. Key Findings

## A. Recall increases as the threshold decreases  
Lower thresholds systematically catch more pathological cases but may degrade precision.  
Higher thresholds do the opposite.

## B. A clinically meaningful trade‑off appears around thresholds 0.35–0.45  
In this region, the model:
- captures a **large proportion of true positives**,  
- keeps precision and false‑positive rates within a tolerable range.

---

# 4. **Selected Threshold: 0.40**

After reviewing all results, threshold **0.40** was chosen because it offers the **best operational trade‑off** for clinical screening.

### **Performance at threshold = 0.40**
- **False Negative Rate (FN rate): ~11.6%**  
  → The model misses only about **1 case out of 9**, which is strong for a screening tool.  
- **False Positive Rate (FP rate): ~37.9%**  
  → A moderate but acceptable rate given the priority of maximizing recall.

### Why 0.40 was chosen
- It significantly reduces false negatives compared to the default threshold 0.50.  
- It avoids the excessive false positives observed at thresholds ≤ 0.30.  
- It maintains a **reasonable balance between sensitivity and alert overload**.  
- It represents the most clinically acceptable compromise among all tested values.

### Note  
This choice will be **validated and refined in Notebook 17**, which performs a detailed qualitative analysis of:
- false negatives (FN),
- false positives (FP),
- their profile and potential clinical implications.

---

## Conclusion
Threshold **0.40** is the recommended operating point for the diabetes model from Notebook 11.  
It provides:
- strong recall,  
- controlled false positive levels,  
- clinically relevant behavior,  
and will serve as the threshold for subsequent analyses and the deployment pipeline.

---

# B. Version Française

## Objectif
Ce notebook analyse différents seuils de décision pour le modèle diabète du **notebook 11** (LightGBM sans variables nutritionnelles).  
L’objectif est de trouver un seuil qui **maximise le rappel (recall) sur la classe pathologique** tout en conservant une **précision acceptable**, afin d’obtenir un compromis pertinent entre :

- **réduction des faux négatifs**, cruciale en dépistage,  
- **contrôle des faux positifs**, important pour éviter trop d’alertes.

Les seuils de 0,05 à 0,90 ont été testés et comparés.

---

## 1. Chargement du modèle et des données
Le notebook charge :
- le modèle LightGBM optimisé : `model_lightgbm_diab_no_bias.pkl`
- le scaler associé : `scaler_diab_no_bias.pkl`
- le jeu de test mis de côté (`X_test_chol.csv`, `y_test_chol.csv`)

Les variables numériques sont re‑standardisées, puis les probabilités prédites sont calculées.

---

## 2. Méthode d’évaluation
Pour chaque seuil dans {0.05, 0.10, …, 0.90}, le notebook calcule :
- les prédictions binaires,  
- la précision et le rappel,  
- le rapport de classification,  
- la matrice de confusion.

Les résultats sont synthétisés dans un tableau final.

---

# 3. Résultats principaux

## A. Le rappel augmente à mesure que le seuil diminue  
Les seuils bas détectent davantage de vrais positifs mais augmentent les faux positifs.  
Les seuils élevés font l’inverse.

## B. Zone d’équilibre vers 0,35–0,45  
Cette plage permet :
- un rappel élevé,  
- une précision encore acceptable,  
- un bon compromis clinique.

---

# 4. **Seuil retenu : 0,40**

Après analyse complète, le seuil **0,40** a été choisi car il offre **le meilleur compromis opérationnel** pour un usage de dépistage.

### **Performances au seuil = 0,40**
- **Taux de faux négatifs (FN) ≈ 11,6 %**  
  → Le modèle manque seulement **1 cas sur 9**, ce qui est excellent pour un outil de screening.  

- **Taux de faux positifs (FP) ≈ 37,9 %**  
  → Un niveau modéré, acceptable compte tenu de la priorité donnée au rappel.

### Pourquoi 0,40 ?
- Baisse nette des faux négatifs par rapport au seuil 0,50.  
- Moins de faux positifs qu’avec un seuil ≤ 0,30.  
- Bon équilibre entre sensibilité et surcharge d’alertes.  
- Comportement globalement cohérent sur le plan clinique.

### Remarque  
Ce choix sera **confirmé et approfondi dans le notebook 17**, dédié à l’analyse des faux négatifs et des faux positifs avec ce seuil.

---

## Conclusion
Le seuil **0,40** est retenu pour le modèle diabète du notebook 11.  
Il permet :
- un rappel élevé,  
- des faux positifs contenus,  
- une pertinence clinique solide.

Ce seuil sera utilisé dans les analyses suivantes et dans le pipeline de déploiement.

---

# End of Report
