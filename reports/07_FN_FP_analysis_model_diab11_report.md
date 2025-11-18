# FN–FP Analysis for Diabetes Model (Notebook 17) — EN + FR  
_Source: 17-analyse-FN-FP-diab-11.ipynb_

---

# A. English Version

## Objective
This notebook analyzes **false negatives (FN)** and **false positives (FP)** produced by the diabetes model from Notebook 11 (LightGBM without nutrition bias, with threshold = 0.40).  
The goals are to:

- describe the **average profile of FN**,  
- describe the **average profile of FP**,  
- highlight that a sizeable share of FP falls into a **clinically meaningful “grey zone”**,  
- refine the **effective rate of truly unnecessary alerts**.

---

## 1. Model, Data, and Threshold

- Model: `model_lightgbm_diab_no_bias.pkl`  
- Scaler: `scaler_diab_no_bias.pkl`  
- Test set: `X_test_chol.csv`, `y_test_chol.csv`  
- Decision threshold: **0.40**

At this threshold, the confusion matrix yields:

- **FN rate ≈ 11.6%**  
- **FP rate ≈ 37.9%**

---

# 2. False Negatives (FN)

FN are **true diabetic individuals (y = 1) predicted as non‑diabetic (ŷ = 0)**.

The notebook creates a dedicated dataframe `df_FN` and compares FN to the overall test set using:

- descriptive statistics (`df_compare`),  
- boxplots for each numerical feature (FN vs non‑FN),  
- the distribution of predicted probabilities for FN.

### 2.1 Descriptive profile of FN

Overall, FN:

- do **not** show extreme values on age, BMI or waist circumference compared with the global test set,  
- have clinical variables that remain within ranges close to the population averages,  
- do not systematically differ on sitting time (PAD680_log) or sleep duration in a way that would define a clear “high‑risk” signature.

### 2.2 Predicted probabilities of FN

The distribution of predicted probabilities for FN is also analyzed. FN tend to have:

- predicted probabilities **close to the decision threshold (0.40)**,  
- values that lie in an overlapping zone with correctly classified negatives.

### Interpretation for FN

FN correspond mainly to:

- **borderline metabolic profiles**,  
- individuals whose features are **not markedly abnormal**,  
- cases located **very close to the model’s decision boundary** in terms of predicted probability.



---

# 3. False Positives (FP)

FP are **non‑diabetic individuals (y = 0) predicted as diabetic (ŷ = 1)**.

A dataframe `df_FP` is built, and:

- descriptive statistics are computed,  
- boxplots (FP vs non‑FP) are generated,  
- a specific high‑risk pattern is explored among FP.

Total number of FP in the test set: **≈ 464**.

Descriptive statistics and visual comparisons show that, on average, FP:

- are **older** than the overall test set,  
- have **higher BMI**,  
- have **higher waist circumference**,  
- tend to present **more sedentary behaviour** (higher sitting time, PAD680_log).

This already indicates that FP are **not random healthy subjects** but concentrate among individuals with a higher metabolic risk load.

---

## 3.1 High‑risk “grey‑zone” FP profile

The notebook then focuses on FP meeting **all** of the following criteria:

- **female**,  
- **age ≥ 60 years**,  
- **BMI above the mean / in the overweight–obese range**,  
- **waist circumference elevated** (threshold comparable to WHO high‑risk values in women).

These criteria are not chosen arbitrarily; they:

- are consistent with what the descriptive statistics show for FP,  
- match a **clinically recognized high‑risk pattern** (older, overweight/obese, central adiposity, sedentary).

From `df_FP`, the notebook identifies:

- **88 FP** matching this profile,  
- which corresponds to **≈ 20% of all FP**.

These individuals:

- do **not** look like clearly healthy, low‑risk profiles,  
- have a configuration compatible with **pre‑diabetes or early metabolic risk**,  
- are precisely the kind of profiles where a positive flag in a screening algorithm is clinically defensible.

---

# 4. Adjusted FP Burden

If one counts *all* FP as equally “wrong”, the raw FP rate is:

- **37.9%** (≈ 464 FP among 1223 healthy subjects).

However, a substantial part of FP corresponds to **metabolically high‑risk individuals** whose alert can be considered **clinically appropriate**, even if they are not labelled diabetic in NHANES.

By excluding only FP with the grey‑zone high‑risk profile from the count of *unjustified* alerts, the notebook arrives at:

- **Adjusted FP count: 376**  
- **Adjusted FP rate: ≈ 30.7% (376 / 1223)**

This adjusted rate is a more realistic indicator of **false positives that are both statistically and clinically undesirable**.

---

# 5. Conclusion (English)

The FN/FP analysis in Notebook 17 shows that:

- **False negatives** have a **borderline risk profile**, with values close to population averages and predicted probabilities near the threshold, rather than overtly high‑risk profiles being missed.  
- **False positives** are concentrated among individuals who are **older, heavier, with higher waist circumference and more sedentary behaviour**, which is consistent with known metabolic risk factors.  
- Within FP, **88 women (≈ 20% of FP) aged ≥ 60 with high BMI and large waist circumference** form a high‑risk “grey‑zone” profile where an alert is clinically legitimate.  
- Once these clinically plausible alerts are discounted, the **effective proportion of clearly unjustified alerts** is ≈ **30.7%**, rather than 37.9%.

This analysis supports the clinical relevance of the **0.40 threshold** chosen for the diabetes model in Notebook 11.

---

# B. Version Française

## Objectif
Ce notebook analyse les **faux négatifs (FN)** et les **faux positifs (FP)** générés par le modèle diabète du notebook 11 (LightGBM sans variables nutritionnelles, seuil = 0,40).  
Les objectifs sont de :

- décrire le **profil moyen des FN**,  
- décrire le **profil moyen des FP**,  
- montrer qu’une part importante des FP se situe dans une **véritable “zone grise” métabolique**,  
- recalculer le **taux d’alertes réellement injustifiées**.

---

## 1. Modèle, Données et Seuil

- Modèle : `model_lightgbm_diab_no_bias.pkl`  
- Scaler : `scaler_diab_no_bias.pkl`  
- Données test : `X_test_chol.csv`, `y_test_chol.csv`  
- Seuil de décision : **0,40**

La matrice de confusion donne :

- **taux de FN ≈ 11,6 %**,  
- **taux de FP ≈ 37,9 %**.

---

# 2. Faux Négatifs (FN)

Les FN sont des **patients réellement diabétiques (y = 1) mais prédits non diabétiques (ŷ = 0)**.

Le notebook construit un `df_FN` et compare FN et ensemble du test grâce :

- aux statistiques descriptives (`df_compare`),  
- à des boxplots (FN vs non‑FN),  
- à la distribution des probabilités prédites pour les FN.

### 2.1 Profil descriptif des FN

Globalement, les FN :

- **ne présentent pas de valeurs extrêmes** en âge, IMC ou tour de taille par rapport au test complet,  
- restent proches des **moyennes de la population** pour la plupart des variables,  
- ne se distinguent pas par un schéma très marqué sur le temps assis (PAD680_log) ou le sommeil.

### 2.2 Probabilités prédites des FN

L’étude des probabilités prédites montre que les FN :

- ont des probabilités **proches du seuil de 0,40**,  
- se situent dans une zone d’**enchevêtrement** avec les vrais négatifs correctement classés.

### Interprétation pour les FN

Les FN correspondent donc principalement à :

- des profils **intermédiaires**,  
- dont les marqueurs métaboliques ne sont **pas fortement perturbés**,  
- des cas positionnés **au voisinage direct de la frontière de décision du modèle**.



---

# 3. Faux Positifs (FP)

Les FP sont des **patients non diabétiques (y = 0) prédits diabétiques (ŷ = 1)**.

Un `df_FP` est construit et :

- des statistiques descriptives sont calculées,  
- des boxplots (FP vs non‑FP) sont tracés,  
- un motif de risque élevé est étudié au sein des FP.

Nombre total de FP dans le test : **≈ 464**.

Les comparaisons montrent qu’en moyenne, les FP :

- sont **plus âgés** que la moyenne du test,  
- ont un **IMC plus élevé**,  
- ont un **tour de taille plus important**,  
- présentent une **sédentarité accrue** (temps assis plus élevé).

Ils ne ressemblent donc pas à des sujets “complètement sains”, mais plutôt à des individus avec un **terrain métabolique à risque**.

---

## 3.1 Profil “zone grise” à haut risque parmi les FP

Le notebook se focalise ensuite sur les FP qui remplissent **simultanément** les critères suivants :

- **sexe féminin**,  
- **âge ≥ 60 ans**,  
- **IMC au‑dessus de la moyenne / en surpoids‑obésité**,  
- **tour de taille élevé** (valeurs proches ou au‑dessus des seuils OMS pour le risque cardio‑métabolique).

Ces critères reflètent directement ce que montrent les statistiques :  
ils décrivent un **profil moyen typique des FP**, et non un sous‑groupe artificiel.

Le filtre appliqué à `df_FP` met en évidence :

- **88 femmes** répondant à ce profil,  
- soit **environ 20 % des FP**.

Ces personnes ont :

- un **profil métabolique déjà défavorable**,  
- une configuration compatible avec **un état prédiabétique ou un risque cardio‑métabolique accru**,  
- un statut pour lequel un signal de dépistage est médicalement justifiable.

---

# 4. Nouveau taux de faux positifs réellement injustifiés

Si l’on considère tous les FP comme des erreurs équivalentes, le taux brut est :

- **37,9 %** (≈ 464 FP sur 1223 sujets réellement non diabétiques).

Mais une partie importante de ces FP correspond à des profils **objectivement à risque** pour lesquels le modèle “prévoit trop tôt” plutôt que “à tort”.

En ne comptant comme “fausses alertes réellement injustifiées” que les FP qui **ne** présentent pas ce profil de zone grise, le notebook obtient :

- **FP ajustés : 376**,  
- **taux de FP ajusté : ≈ 30,7 % (376 / 1223)**.

Ce taux ajusté est une estimation plus honnête de la part de prédictions **vraiment non souhaitables**.

---

# 5. Conclusion (Français)

L’analyse FN/FP du notebook 17 montre que :

- les **FN** ont un profil plutôt **modéré** et des probabilités proches du seuil, ce qui suggère qu’ils se situent dans une zone de décision difficile,  
- les **FP** se concentrent chez des personnes plus âgées, en surpoids, avec tour de taille élevé et forte sédentarité, ce qui correspond à un **profil métabolique à risque**,  
- parmi les FP, **88 femmes (≈ 20 % des FP) d’au moins 60 ans, IMC élevé, tour de taille élevé** incarnent ce profil de **zone grise**, où un signal de dépistage est médicalement défendable,  
- le taux réel d’alertes inutilement générées est donc plus proche de **30,7 %** que du taux brut de 37,9 %.

Ce travail valide la pertinence clinique du **seuil 0,40** pour le modèle diabète du notebook 11.

---

# End of Report
