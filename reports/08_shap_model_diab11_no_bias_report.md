# SHAP Analysis of Diabetes Model without Nutrition (EN + FR)

---

# A. English Version

## Objective

The notebook 20-shap-model-diab-no-bias.ipynb applies **SHAP explainability** to the diabetes prediction model trained in Notebook 11 (LightGBM without nutrition variables) with threshold = 0.40.  
The goal is to understand **which features the model actually uses** to make its predictions and how they contribute globally to diabetes risk.

---

## 1. Data, Model and Features

- Dataset: `nhanes_ready.csv`  
- Target: `diabetes` (binary 0/1)  
- Same feature set as the “no-bias” model:

**Core variables:**
- `RIDAGEYR` — age  
- `RIAGENDR` — sex (binary)  
- `smoker` — current smoker (0/1)

**Morphology:**
- `BMXBMI_log` — log-transformed BMI  
- `BMXWAIST` — waist circumference

**Lifestyle:**
- `PAD680_log` — log of **daily sitting time (minutes per day, excluding sleep)**  
- `SLD012` — sleep duration (hours per night)

**Ethnicity (one-hot encoded):**
- `ethnicity_MexicanAmerican`  
- `ethnicity_OtherHispanic`  
- `ethnicity_NonHispanicWhite`  
- `ethnicity_NonHispanicBlack`  
- `ethnicity_NonHispanicAsian`  
- `ethnicity_OtherRace`

No nutrition variables are included in this model.

The original train/validation/test split is recreated, and the numerical features are standardized with the saved scaler (`scaler_diab_no_bias.pkl`).

---

## 2. SHAP Setup

- Tuned LightGBM model loaded: `model_lightgbm_diab_no_bias.pkl`.  
- A **TreeExplainer** (`shap.TreeExplainer`) is computed.  
- Background data: the **training set**, representing the baseline population.  
- SHAP explanations are computed on the test set.

SHAP values quantify how much each feature pushes the prediction **towards** or **away from** diabetes.

---

## 3. Global Feature Importance (SHAP Bar Plot)

Using:

```python
shap.summary_plot(
    shap_values_pos,
    X_test_sample,
    plot_type="bar",
    max_display=10,
)
```

The global importance ranking highlights:

- **Age (`RIDAGEYR`)**  
- **Central adiposity and morphology:**  
  - `BMXWAIST`  
  - `BMXBMI_log`
- **Sedentary behaviour:**  
  - `PAD680_log`
- **Sleep duration (`SLD012`)**
- **Smoking, sex**
- **Ethnicity indicators**

These features drive most of the predictive signal.

---

## 4. Direction and Structure of Effects (SHAP Beeswarm)

```python
shap.summary_plot(
    shap_values_pos,
    X_test_sample,
    max_display=10,
)
```

This beeswarm plot shows:

- how each feature affects predictions (positive or negative SHAP values),  
- how this effect varies across the feature range.

### **Sleep duration (SLD012): a subtle and counter-intuitive pattern**

SHAP reveals that **higher sleep duration** can sometimes push the prediction *towards* diabetes (positive SHAP values).  
This is **clinically counter-intuitive**, since short sleep is generally associated with higher metabolic risk.

This pattern likely reflects:

- a **statistical association** within NHANES rather than causality,  
- the fact that individuals who sleep longer may also have **lower daytime activity**,  
- **health-condition confounding** (fatigue, chronic illness, medication),  
- the relatively **low global importance** of this feature compared with age or waist circumference.

Thus, the SHAP signal for sleep should be interpreted with **caution**.  
It does *not* imply that more sleep increases diabetes risk; it simply reflects how the model leverages correlations present in the dataset.

---

## 5. Key Takeaways (English)

- The diabetes model without nutrition variables relies on a **compact and clinically meaningful feature set**.  
- Age and central adiposity (waist, BMI) are the **dominant drivers** of predictions.  
- Sedentary time, smoking, sleep and ethnicity provide secondary but real contributions.  
- SHAP confirms the **direction of effects** for most features is coherent with known risk factors.  
- The sleep variable shows a **non-linear, counter-intuitive pattern** that must be interpreted carefully.

This notebook validates the interpretability and robustness of the “no-bias” feature set.

---

# B. Version Française

## Objectif

Le notebook 20-shap-model-diab-no-bias.ipynb applique **SHAP** au modèle de prédiction du diabète entraîné dans le notebook 11 (LightGBM sans variables nutritionnelles) avec un seuil de 0,40.  
L’objectif est d’identifier **les principales variables utilisées par le modèle** et de comprendre leur contribution globale au risque de diabète.

---

## 1. Données, Modèle et Variables

- Dataset : `nhanes_ready.csv`  
- Cible : `diabetes` (0/1)  
- Variables identiques au modèle “no-bias” :

**Cœur :**
- `RIDAGEYR` — âge  
- `RIAGENDR` — sexe  
- `smoker` — tabagisme (0/1)

**Morphologie :**
- `BMXBMI_log` — IMC (transformé en log)  
- `BMXWAIST` — tour de taille

**Mode de vie :**
- `PAD680_log` — log du **temps assis par jour (hors sommeil)**  
- `SLD012` — durée de sommeil en heures

**Ethnicité :**
six variables indicatrices (MexicanAmerican, OtherHispanic, White, Black, Asian, OtherRace)

Aucune variable nutritionnelle n’est utilisée.

---

## 2. Mise en place de SHAP

- Chargement du modèle LightGBM optimisé.  
- Construction d’un **TreeExplainer**.  
- **Background SHAP** : l’ensemble d’entraînement (population “de référence”).  
- Analyse sur l’ensemble de test.

Les valeurs SHAP mesurent comment chaque variable pousse la prédiction vers “diabète” ou vers “non diabète”.

---

## 3. Importance globale (barplot SHAP)

Le graphe classe les variables selon leur **importance moyenne absolue** :

- âge,  
- tour de taille, IMC,  
- temps assis,  
- sommeil,  
- tabac, sexe,  
- ethnicité.

Ces caractéristiques constituent le socle principal du modèle.

---

## 4. Direction et structure des effets (beeswarm SHAP)

Le beeswarm permet de visualiser l’impact (positif ou négatif) de chaque variable sur la prédiction.

### **Durée de sommeil (SLD012) : un motif subtil et contre-intuitif**

Les SHAP values montrent que **des durées de sommeil plus élevées** peuvent parfois **augmenter** la prédiction de diabète.  
Ce résultat est **contre-intuitif** car le manque de sommeil est habituellement considéré comme un facteur de risque.

Ce comportement peut refléter :

- une **association statistique** dans NHANES plutôt qu’un lien causal,  
- une **sédentarité accrue** chez les personnes dormant longtemps,  
- un **état de fatigue ou de pathologies sous-jacentes**,  
- la **faible importance globale** de cette variable.

Ainsi, ce signal doit être interprété avec **prudence** : il ne signifie pas que dormir davantage augmente le risque de diabète, mais reflète uniquement les corrélations apprises par le modèle.

---

## 5. Points clés (Français)

- Le modèle s’appuie sur un ensemble **cohérent et clinique** de variables (âge, adiposité centrale, sédentarité, tabac, sommeil, ethnicité).  
- L’âge et la graisse abdominale sont les **principaux déterminants**.  
- Le temps assis, le tabac et l’ethnicité jouent un rôle complémentaire.  
- Le sommeil présente un **effet non linéaire et contre-intuitif** qui doit être interprété avec précaution.  
- L’analyse SHAP confirme la fiabilité de l’approche sans variables nutritionnelles.

---

# End of Report
