# Diabetes Model without Nutrition Bias (EN + FR)
_Source: 11-model-diab-no-bias.ipynb fileciteturn4file0_

---

# A. English Version

## LightGBM Diabetes Model without Nutrition Variables (NHANES 2021–2023)

This notebook trains and evaluates a **bias-reduced LightGBM model** for diabetes prediction on NHANES 2021–2023.  
Unlike previous versions, it **excludes all nutrition variables** to avoid declaration bias and reverse causality, and focuses only on:
- demographics,
- morphology,
- lifestyle,
- ethnicity.

The goal is to obtain a **more robust and interpretable model**, free from the artifacts observed in SHAP analyses of dietary features.

---

## 1. Data Loading and Target Definition

- Dataset: `nhanes_ready.csv`
- Checks:
  - No missing values used in features.
  - No duplicated rows.
- Target: `diabetes` (binary 0/1).

The class distribution is printed to confirm imbalance and motivate `class_weight="balanced"` in LightGBM.

---

## 2. Feature Set without Nutrition

Feature families:

- **Core**  
  - `RIDAGEYR` (age)  
  - `RIAGENDR` (sex)  
  - `smoker` (binary)

- **Morphology**  
  - `BMXBMI_log`  
  - `BMXWAIST`

- **Lifestyle**  
  - `PAD680_log` (physical activity)  
  - `SLD012` (sleep duration)

- **Ethnicity (optional, enabled)**  
  - `ethnicity_MexicanAmerican`  
  - `ethnicity_OtherHispanic`  
  - `ethnicity_NonHispanicWhite`  
  - `ethnicity_NonHispanicBlack`  
  - `ethnicity_NonHispanicAsian`  
  - `ethnicity_OtherRace`

**No nutrition variables are included** in `candidate_feats`.  
The final design matrix `X_full` and target vector `y` are built from these features only.

---

## 3. Correlation Analysis

A Pearson correlation matrix is computed on the full dataset.  
The notebook displays the correlations of all variables with the `diabetes` target, confirming:

- strong positive association with age and waist circumference,
- moderate association with BMI,
- weaker but present effects of smoking and ethnicity,
- no reliance on dietary intake.

---

## 4. Stratified Train / Validation / Test Split

The data is split as follows:

- 20% test set  
- remaining 80% → split into:
  - 75% train
  - 25% validation

All splits are **stratified on `diabetes`**, preserving the positive rate across subsets.

---

## 5. Selective Standardization

Columns are separated into:
- **binary variables** (not scaled): `RIAGENDR`, `smoker`, ethnicity dummies.
- **numeric variables** (scaled): age, BMI_log, waist, PAD680_log, SLD012.

A `StandardScaler` is fitted on the training set and applied to validation and test sets using the same parameters.

---

## 6. Hyperparameter Optimization (RandomizedSearchCV)

LightGBM hyperparameters are tuned with `RandomizedSearchCV`:

- Search space includes:
  - `num_leaves`, `max_depth`,
  - `min_child_samples`, `min_split_gain`,
  - `subsample`, `colsample_bytree`,
  - `reg_alpha`, `reg_lambda`,
  - `learning_rate`, `n_estimators`.

- Configuration:
  - 40 iterations  
  - 5-fold stratified CV  
  - Scoring: ROC AUC  
  - `class_weight="balanced"`

The best parameters and best CV AUC are printed.

---

## 7. Final Refit with Early Stopping and Saving Artifacts

Train and validation sets are concatenated, then split internally into:
- training subset (90%)
- early-stopping subset (10%)

A final LightGBM model is trained with:
- best parameters from the search,
- increased `n_estimators`,
- early stopping with 150 rounds.

Saved artifacts:

- `artifacts_diab_no_bias/model_lightgbm_diab_no_bias.pkl`
- `artifacts_diab_no_bias/scaler_diab_no_bias.pkl`
- `artifacts_diab_no_bias/best_params.json`

This model is now the **reference diabetes classifier without nutrition bias**.

---

## 8. Test Evaluation (Threshold 0.5)

On the held-out test set:

- Predicted probabilities and labels at threshold 0.5.
- Metrics:
  - classification report (precision, recall, F1 by class),
  - ROC AUC,
  - ROC curve plot,
  - confusion matrix.

This gives the performance of the tuned model using the standard threshold.

---

## 9. Optimal Threshold (Max F1)

Using `precision_recall_curve`, the notebook computes:

- F1-score across all thresholds,
- best threshold maximizing F1,
- associated precision and recall,
- classification report and confusion matrix at this optimal threshold,
- F1 vs threshold plot with the best point highlighted.

This supports operational choices (e.g., prioritizing recall for screening).

---

## Conclusion

This notebook delivers a **clean, bias-reduced LightGBM model** for diabetes prediction:

- Trained **without nutrition variables**, avoiding declaration bias and reverse causality.
- Using only robust features: age, sex, smoking, body composition, activity, sleep, ethnicity.
- Tuned with a rigorous hyperparameter search and early stopping.
- Evaluated both at the standard threshold 0.5 and at the F1-optimal threshold.
- Exported in reusable form (model + scaler + parameters) for deployment (API, Gradio, etc.).

It becomes the **main diabetes model used in the “no-bias” branch of the NHANES 2021–2023 project.**

---

# B. Version Française

## Modèle diabète LightGBM sans variables nutritionnelles (NHANES 2021–2023)

Ce notebook entraîne et évalue un **modèle LightGBM “sans biais nutritionnel”** pour la prédiction du diabète.  
Contrairement aux versions précédentes, il **retire toutes les variables alimentaires** et ne conserve que :
- la démographie,
- la morphologie,
- le mode de vie,
- l’ethnicité.

Objectif : obtenir un modèle **plus robuste, plus interprétable**, et cohérent avec les biais mis en évidence par SHAP sur les variables nutritionnelles.

---

## 1. Chargement des données et définition de la cible

- Dataset utilisé : `nhanes_ready.csv`
- Vérifications :
  - pas de NaN exploités dans les features,
  - aucun doublon.
- Variable cible : `diabetes` (0/1).

La distribution de la classe est affichée, justifiant l’usage de `class_weight="balanced"`.

---

## 2. Choix des variables sans nutrition

Familles de variables :

- **Noyau**  
  - `RIDAGEYR` (âge)  
  - `RIAGENDR` (sexe)  
  - `smoker` (tabagisme)

- **Morphologie**  
  - `BMXBMI_log`  
  - `BMXWAIST`

- **Mode de vie**  
  - `PAD680_log` (activité physique)  
  - `SLD012` (durée de sommeil)

- **Ethnicité (activée)**  
  - `ethnicity_MexicanAmerican`  
  - `ethnicity_OtherHispanic`  
  - `ethnicity_NonHispanicWhite`  
  - `ethnicity_NonHispanicBlack`  
  - `ethnicity_NonHispanicAsian`  
  - `ethnicity_OtherRace`

Aucune variable nutritionnelle n’est intégrée dans `candidate_feats`.  
`X_full` et `y` sont créés uniquement à partir de ces features.

---

## 3. Analyse de corrélation

Une matrice de corrélation de Pearson est calculée.

Les corrélations avec `diabetes` mettent en évidence :
- un rôle majeur de l’âge et du tour de taille,
- un effet intermédiaire de l’IMC,
- des contributions plus modestes de l’ethnicité, du tabac et des variables de mode de vie.

---

## 4. Split stratifié Train / Validation / Test

Le découpage est le suivant :

- 20 % du dataset en **test**,
- sur les 80 % restants :
  - 75 % en **train**,
  - 25 % en **validation**.

Les splits sont **stratifiés sur `diabetes`**.

---

## 5. Standardisation sélective

Séparation des colonnes :

- **binaires (non standardisées)** : `RIAGENDR`, `smoker`, dummies d’ethnicité.
- **numériques (standardisées)** : âge, BMI_log, waist, PAD680_log, SLD012.

Un `StandardScaler` est ajusté sur le train puis appliqué au val et au test.

---

## 6. Optimisation des hyperparamètres (RandomizedSearchCV)

Les hyperparamètres de LightGBM sont optimisés sur le train :

- espace de recherche : structure de l’arbre, régularisation, taux d’apprentissage, `n_estimators`, sous-échantillonnage ;
- 40 itérations de recherche aléatoire ;
- CV stratifiée à 5 folds ;
- score optimisé : ROC AUC ;
- `class_weight="balanced"`.

Les meilleurs paramètres et le meilleur AUC moyen sont affichés.

---

## 7. Refit final avec early stopping et sauvegarde

Train et validation sont fusionnés, puis re-découpés en :
- sous-ensemble apprentissage (90 %),
- sous-ensemble early stopping (10 %).

Le modèle final est entraîné avec :
- les meilleurs hyperparamètres,
- un `n_estimators` plus grand,
- un early stopping de 150 itérations.

Les artefacts sont sauvegardés :

- `artifacts_diab_no_bias/model_lightgbm_diab_no_bias.pkl`
- `artifacts_diab_no_bias/scaler_diab_no_bias.pkl`
- `artifacts_diab_no_bias/best_params.json`

Ce modèle devient la **référence “no-bias” pour le diabète**.

---

## 8. Évaluation sur le test (seuil 0,5)

Sur le jeu de test :

- prédiction des probabilités + classes (seuil 0,5),
- rapport de classification complet,
- calcul du ROC AUC,
- tracé de la courbe ROC,
- matrice de confusion.

Cela fournit la vision “standard” de la performance du modèle.

---

## 9. Seuil optimal (maximisation du F1-score)

À partir de `precision_recall_curve`, le notebook :

- calcule le F1-score pour chaque seuil,
- identifie le seuil qui maximise le F1,
- affiche la précision et le rappel correspondants,
- produit le rapport de classification et la matrice de confusion à ce seuil,
- trace la courbe F1 en fonction du seuil.

Ce bloc permet d’ajuster la stratégie de décision (par exemple privilégier le rappel en dépistage).

---

## Conclusion

Ce notebook fournit un **modèle de prédiction du diabète épuré des biais nutritionnels** :

- sans variables alimentaires auto-déclarées,
- basé sur l’âge, le sexe, le tabac, la morphologie, l’activité, le sommeil et l’ethnicité,
- optimisé par recherche d’hyperparamètres et early stopping,
- évalué de manière rigoureuse sur un jeu de test indépendant,
- sauvegardé avec tous les artefacts nécessaires au déploiement.

Il constitue le **modèle principal utilisé dans la branche “no-bias” du projet NHANES 2021–2023.**
