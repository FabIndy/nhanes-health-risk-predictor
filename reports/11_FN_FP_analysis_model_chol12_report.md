# Analysis of False Negatives and False Positives — Model 12, Threshold 0.35  
*Notebook analyzed: `19-analyse-FN-FP-chol-12.ipynb`* fileciteturn6file0

---

# PART 1 — English Report

## 1. Context and Objective

This notebook analyses the **errors of Model 12 (LightGBM cholesterol classifier, no-bias version)** on the **test set**, using the decision **threshold fixed at 0.35**.

The main objective is to **characterize the typical profiles of:**

- **False Negatives (FN)**: truly pathological patients (`chol_high = 1`) predicted as healthy (`0`)
- **False Positives (FP)**: truly non-pathological patients (`chol_high = 0`) predicted as pathological (`1`)

and to assess **how many “false alarms” are actually clinically plausible cases** (borderline cholesterol or high-risk profile), rather than clearly healthy individuals.

---

## 2. Setup and Data

- Source data: `nhanes_ready.csv`
- Target: `chol_high` (0/1)
- Features: identical to Model 12  
  - Core: age `RIDAGEYR`, sex `RIAGENDR`, smoker `smoker`  
  - Morphology: `BMXBMI_log`, `BMXWAIST`  
  - Lifestyle: `PAD680_log` (sitting time), `SLD012` (sleep duration)  
  - Ethnicity dummies (6 binary variables)

The exact same **train/val/test split** as in Model 12 is reproduced (stratified, 80/20 then 60/20/20).

The **saved scaler and model** from notebook 12 are reloaded and applied to the test set, then predictions are computed at **threshold = 0.35**.

---

## 3. Global FN/FP Counts at Threshold 0.35

On the test set:

- **False Negatives (FN)**: **17 individuals**
- **False Positives (FP)**: **707 individuals**

The model is intentionally tuned for **high recall** on the pathological class, which mechanically increases the number of FP.

---

## 4. Average Profile of False Negatives (FN)

Using descriptive statistics, the notebook compares FN with the **global test set mean**.

For the **17 FN**, the **average profile** is:

- **Age**: **younger than the test-set average**
- **Sex**: predominantly **female**
- **Smoking**: mostly **non-smokers**
- **BMI**: **around the global mean**
- **Waist circumference**: **below the global mean**
- **Sitting time (`PAD680_log`)**: **below the global mean**
- **Sleep duration (`SLD012`)**: **above the global mean**

**Interpretation**:  
These FN correspond to **relatively young, non-smoking women with no obvious morphological risk markers** (normal BMI and waist, rather less sedentary, slightly more sleep).  
They are **hard-to-detect pathological cases**, even for a model focused on recall.

---

## 5. Average Profile of False Positives (FP)

For the **707 FP**, the **average profile** (relative to the full test set) is:

- **Age**: around **55 years**, i.e. **older than the test-set average**
- **Sex**: predominantly **female**
- **Smoking**: mostly **non-smokers**
- **BMI**: **above the test-set mean** (elevated BMI)
- **Waist circumference**: **above the test-set mean** (abdominal obesity)
- **Sitting time and sleep**: **close to the test-set mean**

**Interpretation**:  
On average, FP are **not randomly healthy people**.  
They match a **high-risk cardiometabolic profile**: older women, non-smokers but with **elevated BMI and waist circumference**, which are strong risk factors for dyslipidemia and cardiovascular disease.

---

## 6. Zoom on “Clinically Plausible” False Positives

The notebook then refines the analysis among the 707 FP to identify those who are **clinically suspicious**, even if labeled as non-pathological in `chol_high`.

Two subgroups are considered:

1. **Grey-zone cholesterol**:  
   - `LBXTC` between **200 and 240 mg/dL**  
   - Biochemically borderline, even if not strictly “high” by the chosen label.

2. **High-risk profile** (from FP average profile):  
   - **Women ≥ 55 years**,  
   - **High BMI**,  
   - **High waist circumference**.

The union of these two groups yields:

- **126 FP** who are either:
  - in the **grey cholesterol zone** (200–240 mg/dL), **or**
  - match the **high-risk phenotype** of FP (older women, elevated BMI and waist).

These are **not reassuringly healthy** individuals; they represent **borderline or high-risk profiles**, for whom an alert is clinically defensible.

---

## 7. Truly Healthy False Positives

Among the **1255 truly negative individuals** in the test set, **415** are flagged as positive but:

- are **not** in the grey zone (cholesterol < 200 mg/dL),  
- **do not** match the high-risk profile definition.

These **415 people** can reasonably be considered **“truly healthy individuals flagged by mistake”**.

This corresponds to:

- **415 / 1255 ≈ 33%**

So, **about one third of truly healthy patients are incorrectly alerted**.

---

## 8. Conclusion — Is This Acceptable for Prevention?

This analysis shows that:

- The model at **threshold 0.35** produces many FP in absolute terms,  
- But a **large part of these FP (126 cases)** have **either borderline cholesterol or a high-risk cardiometabolic profile**,
- Only **~33% of truly healthy negatives** (415 out of 1255) are alerted without obvious risk factors.

In a **preventive screening** context, this trade-off is **acceptable and clinically meaningful**:

- **High recall on pathological cases** is preserved (as shown in notebook 18),
- Many FP correspond to **people who deserve closer monitoring**,
- The proportion of **“clearly healthy but alerted”** remains limited (~1 out of 3 negatives).

This notebook therefore **supports and refines the choice of threshold 0.35** for Model 12.

---

# PART 2 — Rapport en Français

## 1. Contexte et objectif

Ce notebook analyse les **erreurs du Modèle 12 (classifieur LightGBM cholestérol, version no-bias)** sur le **jeu de test**, avec un **seuil de décision fixé à 0,35**.

L’objectif est de **caractériser les profils typiques** :

- des **Faux Négatifs (FN)** : patients réellement pathologiques (`chol_high = 1`) prédits sains (`0`),  
- des **Faux Positifs (FP)** : patients réellement non pathologiques (`chol_high = 0`) prédits malades (`1`),

et de déterminer **dans quelle mesure les FP sont réellement “sains” ou cliniquement plausibles** (profil à risque ou cholestérol borderline).

---

## 2. Mise en place

- Données : `nhanes_ready.csv`
- Cible : `chol_high` (0/1)
- Features : identiques au Modèle 12  
  - Cœur : âge `RIDAGEYR`, sexe `RIAGENDR`, tabac `smoker`  
  - Morphologie : `BMXBMI_log`, `BMXWAIST`  
  - Mode de vie : `PAD680_log` (temps assis), `SLD012` (sommeil)  
  - Ethnicité : 6 variables indicatrices

Le même **split train/val/test** que dans le modèle 12 est reproduit (80/20 puis 60/20/20, stratifié).  
Le **scaler** et le **modèle entraîné** sont rechargés, puis évalués au **seuil 0,35**.

---

## 3. Nombre global de FN et FP (seuil 0,35)

Sur le jeu de test :

- **Faux négatifs (FN)** : **17 personnes**
- **Faux positifs (FP)** : **707 personnes**

Le modèle est volontairement paramétré pour **maximiser le rappel** sur la classe pathologique, ce qui augmente mécaniquement le nombre de FP.

---

## 4. Profil moyen des Faux Négatifs (FN)

En comparant les FN à la **moyenne du jeu de test**, on obtient le profil moyen suivant pour les **17 FN** :

- **Âge** : **plus jeunes que la moyenne** du test
- **Sexe** : majoritairement **femmes**
- **Tabac** : plutôt **non-fumeuses**
- **IMC (BMI)** : **proche de la moyenne**
- **Tour de taille** : **inférieur à la moyenne**
- **Temps assis (`PAD680_log`)** : **inférieur à la moyenne**
- **Sommeil (`SLD012`)** : **supérieur à la moyenne**

**Interprétation :**  
Ces FN correspondent à des **profils apparemment peu à risque** (jeunes, femmes, non-fumeuses, morphologie peu inquiétante, moins sédentaires, sommeil plus long).  
Ce sont des **cas pathologiques difficiles à repérer**, même avec un modèle orienté vers le recall.

---

## 5. Profil moyen des Faux Positifs (FP)

Pour les **707 FP**, le profil moyen (par rapport à la moyenne du test) est :

- **Âge** : environ **55 ans**, donc **supérieur à la moyenne**
- **Sexe** : majoritairement **femmes**
- **Tabac** : essentiellement **non-fumeuses**
- **IMC** : **supérieur à la moyenne** (IMC élevé)
- **Tour de taille** : **supérieur à la moyenne** (obésité abdominale)
- **Temps assis et sommeil** : **proches de la moyenne** du test

**Interprétation :**  
En moyenne, les FP **ne sont pas des individus “parfaitement sains” tirés au hasard**.  
Ils présentent un **profil cardiométabolique à risque** : femmes d’environ 55 ans, avec **IMC et tour de taille élevés**, même si leur cholestérol total ne dépasse pas le seuil de la variable `chol_high`.

---

## 6. Zoom sur les FP à risque ou borderline

Le notebook examine ensuite, parmi les **707 FP**, ceux qui :

1. **Ont un cholestérol en zone grise** :  
   - `LBXTC` entre **200 et 240 mg/dL** (valeur borderline),

**ou**

2. **Correspondent au profil moyen à risque observé chez les FP** :  
   - **Femmes d’au moins 55 ans**,  
   - **IMC élevé**,  
   - **Tour de taille élevé**.

L’union de ces deux groupes représente :

- **126 faux positifs** au total.

Ces 126 FP ne sont **pas des profils rassurants** :  
ils sont soit **biochimiquement borderline**, soit **clairement à risque** sur le plan morphologique et démographique.

---

## 7. Faux positifs vraiment “sains”

Parmi les **1255 vrais négatifs** du test, **415** sont prédits positifs mais :

- ne sont **ni** en zone grise (cholestérol < 200 mg/dL),  
- **ni** dans le profil à risque (femmes ≥ 55 ans avec IMC et tour de taille élevés).

On peut donc considérer ces **415 personnes** comme des **individus réellement sains alertés à tort**.

Cela correspond à :

- **415 / 1255 ≈ 33 %**

Autrement dit, **environ un tiers des vrais négatifs** sont alertés alors qu’ils ne présentent pas de risque évident.

---

## 8. Conclusion — Pertinence clinique du seuil 0,35

Cette analyse montre que, au seuil **0,35** :

- Le modèle génère beaucoup de FP en valeur absolue,  
- Mais une part importante (**126 FP**) concerne des **profils soit borderline, soit à haut risque**,  
- Seuls **environ 33 % des vrais négatifs** (415 sur 1255) sont **de vrais “faux positifs cliniquement rassurants”**.

Dans une optique de **dépistage préventif**, ce compromis est **cohérent** :

- On maintient un **rappel élevé** sur les cas pathologiques,  
- Une large fraction des FP correspond malgré tout à des profils **justifiant une vigilance accrue**,  
- Le nombre de patients réellement sains inutilement inquiétés reste **limité**.

Ce notebook **confirme et renforce la pertinence du seuil 0,35** choisi pour le Modèle 12.

---

*Fin du rapport.*
