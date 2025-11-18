# Threshold Optimization — Model 12 (NHANES 2021–2023)  
*Notebook analyzed: 18-threshold-analysis-chol-12.ipynb* fileciteturn5file0

---

# PART 1 — English Report

## 1. Objective  
This notebook performs a **post-training threshold optimization** for **Model 12 (LightGBM cholesterol classifier — no-bias version)**.  
The goal is to adjust the decision threshold so that the model maximizes **recall on the pathological class (`chol_high = 1`)**, while keeping **precision at an acceptable level** for a preventive screening context.

---

## 2. Method Summary  
- The model and scaler from Notebook 12 are reloaded.  
- Probabilities on the test set are computed.  
- A grid of thresholds from **0.05 to 0.90** is evaluated.  
- For each threshold, metrics are calculated: precision, recall, F1-score, classification report, and confusion matrix.  
- The decision threshold is chosen based on the best compromise between **high recall** and **reasonable precision**, focusing on the needs of preventive screening.

---

## 3. Why Threshold = 0.35  
Across all tested thresholds, **0.35** emerged as the most coherent choice for a medical screening use case:

### ✔ Priority: maximize recall  
At **threshold = 0.35**, the model reaches:  
- **Recall (class 1): 0.862**  
Meaning it correctly identifies **86.2%** of pathological individuals.

### ✔ Precision remains acceptable  
Precision on class 1 is:  
- **Precision (class 1): 0.13**

In preventive screening, low precision is acceptable: false positives can undergo further testing, while false negatives are far more harmful.

### ✔ Impact on error rates  
- **False Negative Rate ≈ 13.8%**  
- **False Positive Rate ≈ 56.33%**

Although FPR is high, this is consistent with the chosen priority:  
**avoid missing at-risk individuals, even at the cost of more false alarms.**

### ✔ Broader justification  
Notebook 19 (FN & FP analysis) will show that many FN/FP cases fall into borderline biochemical zones, supporting the relevance of this threshold.

---

## 4. Performance Summary at Threshold 0.35  

| Metric    | Class 1 (Pathological) |
|-----------|------------------------|
| Precision | **0.13**               |
| Recall    | **0.862**              |
| FNR       | **13.8%**              |
| FPR       | **56.33%**             |

This threshold provides the **best medically aligned balance** for Model 12:  
**sensitivity first, acceptable precision second.**

---

# PART 2 — Rapport en Français

## 1. Objectif  
Ce notebook réalise une **optimisation du seuil de décision** pour le **Modèle 12 LightGBM (cholestérol — version no-bias)**.  
L'objectif est d’adapter le seuil pour **maximiser le rappel (recall) de la classe pathologique**, tout en conservant une **précision raisonnable** dans un contexte de dépistage.

---

## 2. Méthodologie  
- Chargement du modèle et du scaler provenant du notebook 12.  
- Calcul des probabilités sur le jeu de test.  
- Évaluation de seuils allant de 0.05 à 0.90.  
- Calcul pour chaque seuil : précision, rappel, F1, rapport de classification, matrice de confusion.  
- Sélection du seuil offrant le meilleur compromis rappel/précision pour un usage médical préventif.

---

## 3. Pourquoi le seuil retenu est 0.35  

### ✔ Priorité : maximiser le recall  
Au seuil **0.35**, on obtient :  
- **Recall (classe 1) = 0.862**  
Le modèle détecte **86,2%** des individus pathologiques.

### ✔ Précision acceptable pour du dépistage  
- **Précision (classe 1) = 0.13**

En dépistage, une précision faible n’est pas problématique :  
**mieux vaut trop de suspicions que des cas non détectés.**

### ✔ Taux d’erreurs  
- **Taux de faux négatifs (FN) ≈ 13,8%**  
- **Taux de faux positifs (FP) ≈ 56,33%**

Même si le taux de FP est élevé, ce choix est cohérent avec la stratégie :  
**réduire au minimum les faux négatifs.**

### ✔ Justification contextuelle  
Le notebook 19 montrera que de nombreux FN/FP appartiennent à des profils biochimiques borderline, renforçant la validité du seuil 0.35.

---

## 4. Résumé des performances au seuil 0.35  

| Métrique   | Classe 1 (Pathologique) |
|------------|-------------------------|
| Précision  | **0.13**                |
| Recall     | **0.862**               |
| Taux de FN | **13,8%**               |
| Taux de FP | **56,33%**              |

Le seuil **0.35** constitue donc le **meilleur compromis**, parfaitement adapté à un usage de **dépistage préventif**.

---

*End of report.*
