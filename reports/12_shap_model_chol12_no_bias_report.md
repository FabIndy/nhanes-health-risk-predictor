# SHAP Interpretation — Model 12 (Cholesterol, No-Bias Version)  
*Notebook analyzed: `21-shap-model-chol-no-bias.ipynb`* fileciteturn8file0  

---

# PART 1 — English Report

## 1. Objective  
This notebook provides a **global SHAP interpretation** of **Model 12 (LightGBM, cholesterol high = 1, no-bias version)**.  
The aim is to understand **which features most strongly influence predictions** and **how they push the model toward or away from the class `chol_high = 1`**, using:

- a SHAP bar plot (mean absolute importance),  
- a SHAP beeswarm plot (direction + magnitude of effects),  
- a dependence plot for `BMXBMI_log`.  

This chapter complements the threshold-optimisation and FN/FP analyses for the NHANES 2021–2023 cholesterol model.

---

## 2. Data and Model  
- Dataset: `nhanes_ready.csv`, target `chol_high` (0/1).  
- Features: same as in Model 12 training:  
  - Age `RIDAGEYR`, sex `RIAGENDR`, smoking `smoker`  
  - Morphology: `BMXBMI_log`, `BMXWAIST`  
  - Lifestyle: sitting time `PAD680_log`, sleep duration `SLD012`  
  - Six ethnicity indicators.  
- All numerical features are standardised with the **saved scaler** from Model 12.  
- The **trained LightGBM model** is reloaded from  
  `artifacts_chol_no_bias/model_lightgbm_chol_no_bias.pkl`.  

SHAP is computed on the **full test set**, with the training set used as background.

---

## 3. Global Feature Importance (SHAP Bar Plot)

The SHAP bar plot shows the **mean absolute contribution** of each feature to the prediction *cholesterol high = 1*.  
The most influential predictors are:

1. **Age (RIDAGEYR)**  
2. **Waist circumference (BMXWAIST)**  
3. **Sex (RIAGENDR)**  
4. **BMI (log-transformed, BMXBMI_log)**  
5. **Smoking status (smoker)**  
6. **Sleep duration (SLD012)**  

Ethnicity variables have a smaller average impact, but still slightly modulate local predictions.

Overall, the ranking is medically coherent: **age and abdominal adiposity** are the dominant drivers of predicted dyslipidemia risk.

---

## 4. Direction of Effects (SHAP Beeswarm Plot)

The SHAP beeswarm plot (see screenshot) provides **two pieces of information at once**:

- horizontal position = **SHAP value** (effect on the prediction),  
- colour = **feature value** (blue = low, pink = high).

### Age (RIDAGEYR)  
- High ages (pink points) cluster on the **right** (positive SHAP values): they **push the model toward high cholesterol**.  
- Low ages (blue) are mainly on the **left**: they reduce the predicted risk.  

This is fully in line with clinical knowledge.

### Waist circumference (BMXWAIST)  
- High waist values are mostly associated with **positive SHAP values** → increased probability of `chol_high = 1`.  
- Low waist values tend to be protective.  

Again, this matches the link between abdominal obesity and dyslipidemia.

### Sex (RIAGENDR)  
- Depending on the encoding, one sex (here: women) tends to shift predictions slightly upward.  
- The effect size remains moderate but consistent across the test set.

### Smoking (smoker)  
- Being a smoker is associated with **positive SHAP values**, i.e. a higher predicted risk.

---

## 5. A More Nuanced View on BMI and Sleep

### 5.1 BMI (BMXBMI_log): a non-trivial pattern  

Unlike waist circumference, the beeswarm plot for **BMXBMI_log** does **not** show a simple “higher BMI → higher risk” pattern.  
In the current model:

- Many **high BMI values (pink)** appear on the **left side** (negative SHAP values),  
- while some **low BMI values (blue)** appear on the **right side** (positive SHAP values).

This means that, **in this dataset and for this model**, a high BMI can sometimes **pull the prediction downward**, and low BMI can occasionally **push it upward**.

We must therefore interpret this **very cautiously**. Two possible (non-exclusive) hypotheses can be mentioned:

1. **High BMI with high muscle mass**  
   - Some individuals with high BMI may be **strongly muscled rather than obese**,  
   - Their **waist circumference remains moderate**, and metabolic risk is lower,  
   - In such cases, the model may learn that “high BMI but moderate waist” is **less risky**.

2. **Low or “normal” BMI but high fat percentage**  
   - Some individuals may have a **relatively low BMI** but **unfavourable fat distribution** (e.g. visceral fat, “TOFI” profiles),  
   - Combined with a high waist circumference or other risk factors, this can lead to **positive SHAP values** for low BMI values.

These hypotheses **cannot be proven** with SHAP alone, but they help explain why BMI behaves differently from waist circumference and why the model seems to “trust” **waist** more than **BMI** as a cardiometabolic marker.

### 5.2 Sleep duration (SLD012): high values and higher risk  

The beeswarm plot also shows that:

- **Higher sleep duration (pink points)** tends to be associated with **positive SHAP values**,  
- whereas shorter sleep (blue) more often appears with **negative SHAP values**.

This goes against the naive idea that “more sleep = always better”.  
A reasonable, cautious hypothesis is that:

- Very long sleep duration may reflect **underlying severe illness, fatigue or frailty**,  
- In the NHANES sample, some people who sleep a lot might be those with **poor overall health**, which correlates with abnormal lipid profiles.

Again, this is **exploratory, not causal**: SHAP only describes the behaviour of the model given the data; it does not prove that long sleep *causes* high cholesterol.

---

## 6. SHAP Dependence Plot for `BMXBMI_log`

The dependence plot for `BMXBMI_log` confirms that the relationship between BMI and predicted risk is **not perfectly monotonic**:

- For some ranges of BMI, SHAP values increase,  
- for others, they flatten or even decrease.

This reinforces the idea that **BMI alone is an imperfect proxy** for cardiometabolic risk, and that the model relies more heavily on **waist circumference** and other covariates to refine its predictions.

---

## 7. Conclusion — What This SHAP Study Adds  

- Model 12 relies strongly on **age and waist circumference**, which is medically consistent.  
- **BMI and sleep duration show more complex, non-linear patterns** that require nuanced interpretation.  
- SHAP highlights situations where **high BMI can be protective in the model** (possibly muscular or “fit” profiles) and where **long sleep may correlate with severe illness**, but these interpretations must remain **hypotheses**, not causal claims.  
- Ethnicity and lifestyle variables adjust the risk but remain secondary compared to age and morphology.

Overall, the SHAP analysis shows that Model 12 behaves in a way that is **clinically interpretable but not simplistic**, capturing both expected effects (age, waist, smoking) and subtler patterns (BMI, sleep) that deserve further investigation.

---

# PART 2 — Rapport en Français

## 1. Objectif  
Ce notebook propose une **interprétation globale SHAP** du **Modèle 12 (LightGBM, cholestérol élevé = 1, version no-bias)**.  
L’objectif est de comprendre **quelles variables influencent le plus les prédictions** et **dans quel sens elles poussent le modèle vers la classe `chol_high = 1` ou vers la classe 0**, grâce à :

- un *bar plot* SHAP (importance moyenne absolue),  
- un *beeswarm plot* (direction + intensité des effets),  
- un graphique de dépendance pour `BMXBMI_log`.  

Cette analyse complète l’optimisation du seuil et l’étude FN/FP du projet NHANES 2021–2023.

---

## 2. Données et Modèle  
- Données : `nhanes_ready.csv`, cible `chol_high` (0/1).  
- Variables explicatives : âge, sexe, tabac, IMC log, tour de taille, temps assis, sommeil, indicateurs d’ethnicité.  
- Standardisation : mêmes scalers que pour l’entraînement du Modèle 12.  
- Modèle : `model_lightgbm_chol_no_bias.pkl`, chargé depuis les artefacts.  
- SHAP calculé sur le **jeu de test**, avec le **jeu d’entraînement comme background**.

---

## 3. Importance Globale (Bar Plot SHAP)

Le *bar plot* SHAP donne l’importance moyenne absolue de chaque variable dans la prédiction *cholesterol high = 1*.  
Les variables les plus influentes sont :

1. **RIDAGEYR (âge)**  
2. **BMXWAIST (tour de taille)**  
3. **RIAGENDR (sexe)**  
4. **BMXBMI_log (IMC log)**  
5. **smoker (tabac)**  
6. **SLD012 (durée de sommeil)**  

Les variables d’ethnicité jouent un rôle secondaire.  
Globalement, la hiérarchie est cohérente : **âge et adiposité abdominale** dominent le risque estimé.

---

## 4. Direction des Effets (Beeswarm SHAP)

Le *beeswarm plot* combine :

- la position horizontale (valeur SHAP = effet sur la prédiction),  
- la couleur (valeur de la variable : bleu = bas, rose = élevé).

### Âge  
- Âge élevé (points roses) → SHAP positif → **augmentation du risque prédit**.  
- Âge faible (bleu) → SHAP négatif → **réduction du risque**.

### Tour de taille  
- Tour de taille élevé → SHAP plutôt positif → **risque accru**.  
- Tour de taille faible → effet protecteur.

### Sexe  
- Selon l’encodage, un des deux sexes (ici les femmes) présente en moyenne un SHAP légèrement plus positif.  
- L’effet reste modéré.

### Tabac  
- Être fumeur est associé à des valeurs SHAP positives, donc à une **augmentation du risque estimé**.

---

## 5. Une lecture plus fine de l’IMC et du sommeil

### 5.1 IMC (BMXBMI_log) : un motif non trivial  

Contrairement au tour de taille, le *beeswarm* de **BMXBMI_log** ne montre pas un simple schéma “IMC élevé = risque plus élevé”.  
On observe :

- de nombreux **IMC élevés (points roses)** du côté **négatif** de l’axe SHAP,  
- et des **IMC bas (bleus)** parfois du côté **positif**.

Autrement dit, dans ce modèle et sur ce jeu de données :

- un IMC élevé peut **tirer la prédiction vers le bas**,  
- un IMC bas peut, dans certains contextes, **tirer la prédiction vers le haut**.

Il faut donc rester prudent et avancer uniquement des **hypothèses** :

1. **IMC élevé mais masse musculaire importante**  
   - Certains individus ont un IMC élevé car ils sont **très musclés**,  
   - Leur tour de taille reste modéré et leurs autres facteurs sont favorables,  
   - Le modèle apprend alors que ce profil n’est pas particulièrement à risque, d’où des SHAP négatifs pour des IMC élevés.

2. **IMC bas mais composition corporelle défavorable**  
   - D’autres personnes peuvent avoir un IMC apparemment “normal” mais une **répartition de graisse défavorable** (viscérale, “TOFI”),  
   - Combiné à un tour de taille élevé ou à d’autres facteurs, cela peut entraîner des SHAP positifs malgré un IMC bas.

Ces interprétations restent **exploratoires** : SHAP décrit le comportement du modèle, pas un lien causal direct.

### 5.2 Durée de sommeil (SLD012) : valeurs élevées et risque accru  

Le *beeswarm* met aussi en évidence que :

- une **durée de sommeil élevée (points roses)** est souvent associée à des **valeurs SHAP positives**,  
- alors qu’une durée plus courte (bleu) est plus fréquemment liée à des SHAP négatifs.

Ce résultat va à l’encontre de l’intuition “plus de sommeil = toujours mieux”.  
Une hypothèse raisonnable est que :

- des durées de sommeil très élevées peuvent refléter un **état de santé très altéré**, une fatigue importante, voire une forme de fragilité,  
- ces profils peuvent cumuler plusieurs facteurs de risque (âge, comorbidités) et présenter des anomalies lipidiques.

Là encore, il ne s’agit **pas de dire que le sommeil long cause le cholestérol**, mais que, dans ce jeu de données, **les personnes qui dorment beaucoup sont souvent des patients plus malades**, et le modèle intègre cette information.

---

## 6. Graphique de dépendance SHAP pour `BMXBMI_log`

Le graphique de dépendance confirme que la relation entre IMC et risque prédit est **non linéaire** :

- dans certaines plages d’IMC, les valeurs SHAP augmentent,  
- dans d’autres, elles se stabilisent ou diminuent.

Cela illustre le fait que **l’IMC seul n’est pas un indicateur suffisant**, et que le modèle s’appuie beaucoup sur le **tour de taille** et les autres covariables pour affiner la prédiction.

---

## 7. Conclusion — Apport de l’analyse SHAP  

- Le Modèle 12 utilise surtout **l’âge et le tour de taille**, ce qui est attendu sur le plan clinique.  
- Les comportements plus complexes de **l’IMC** et de la **durée de sommeil** montrent que le modèle capture des motifs plus subtils, qu’il faut interpréter avec prudence.  
- SHAP suggère que certains IMC élevés peuvent correspondre à des profils musclés peu à risque, et que certains IMC bas peuvent malgré tout être associés à des profils à risque.  
- Les durées de sommeil très élevées pourraient refléter des états de santé fragiles plutôt que des habitudes favorables.

Cette analyse renforce la **transparence** du modèle : elle confirme des effets attendus (âge, tour de taille, tabac) tout en mettant en lumière des patterns plus nuancés qui méritent une exploration clinique supplémentaire.

---

*End of report.*