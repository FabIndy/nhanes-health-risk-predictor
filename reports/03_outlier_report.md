# Outlier Management — Justification Report
## (English first, French version below)

# 🇬🇧 1. Outlier Management Rationale (English)

## Overview
As part of the predictive modeling for diabetes risk and high-cholesterol risk using NHANES 2021–2023 data, a thorough analysis of extreme values was conducted on all numerical variables included in the models (anthropometric, clinical, demographic, and behavioral variables).

All nutritional variables (calories, sugars, fats, carbs, alcohol, water, etc.) were **excluded** from both final models.

The outlier assessment therefore concerns only the variables that actually feed the machine-learning algorithms.

## Findings
The analysis shows:

- Most extreme values are present only in nutrition variables — which are **not used** in the models.
- Variables used in the models show **very few extreme values**, all of which are clinically plausible:

| Variable                   | Extreme Outliers | Comment                         |
|----------------------------|------------------|---------------------------------|
| LBXTC (total cholesterol)  | 8                | expected in severe dyslipidemia |
| BMXBMI (BMI)               | 23               | severe obesity cases            |
| BMXWT (weight)             | 9                | consistent with BMI outliers    |
| BMXWAIST (waist)           | 1                | high-risk profile               |
| PAD680 (physical activity) | 36               | heterogeneous behavior          |
| RIDAGEYR (age)             | 0                | perfectly clean                 |

No impossible or erroneous values were detected.

## Why No Outliers Were Removed

### 1. Outliers represent high-risk patients
Extreme BMI, waist circumference or cholesterol values correspond to individuals who are genuinely at elevated risk. Removing them would eliminate the most clinically relevant profiles and bias the model toward “healthy” observations.

### 2. NHANES clinical measures are reliable
Anthropometric and laboratory data are collected by trained professionals following standardized procedures. Extreme values in these variables are **real**, not measurement errors.

### 3. LightGBM is robust to extreme values
The models use LightGBM, an algorithm based on decision trees:
- insensitive to outliers,
- not relying on distance metrics,
- not requiring normally distributed variables.

Thus, no technical justification exists for trimming or filtering out extreme observations.

## Conclusion
The extreme values observed in the features used by the models are:
- rare,
- clinically meaningful,
- representative of real high-risk profiles,
- and fully compatible with LightGBM.

**Final decision: no outlier removal was applied to diabetes and cholesterol models.**
**Keeping extreme values preserves predictive accuracy and avoids clinical bias.**

---

# 🇫🇷 2. Justification de la gestion des valeurs extrêmes (Français)

## Résumé
Dans le cadre des modèles prédictifs du risque de diabète et du risque de cholestérol élevé basés sur les données NHANES 2021–2023, une analyse détaillée des valeurs extrêmes a été réalisée sur toutes les variables utilisées (anthropométrie, clinique, démographie, comportement).

Toutes les variables nutritionnelles ont été **exclues** des modèles finaux.

L’analyse des valeurs extrêmes concerne donc uniquement les variables réellement intégrées dans les modèles.

## Constats
Les résultats montrent :
- La majorité des valeurs extrêmes se trouvent dans les données nutritionnelles — **non utilisées** dans les modèles.
- Les variables du modèle ne présentent que très peu de valeurs extrêmes, toutes **cliniquement cohérentes** :

| Variable                   | Valeurs extrêmes | Commentaire                       |
|----------------------------|------------------|-----------------------------------|
| LBXTC (cholestérol total)  | 8                | cohérent avec des cas sévères     |
| BMXBMI (IMC)               | 23               | obésité morbide                   |
| BMXWT (poids)              | 9                | cohérent avec l’IMC               |
| BMXWAIST (tour de taille)  | 1                | profil cardiométabolique à risque |
| PAD680 (activité physique) | 36               | variabilité importante            |
| RIDAGEYR (âge)             | 0                | aucune anomalie                   |

Aucune valeur aberrante ou impossible n’a été identifiée.

## Pourquoi aucune suppression n’a été appliquée

### 1. Les valeurs extrêmes correspondent à des patients réellement à risque
Les IMC très élevés, tours de taille importants ou valeurs de cholestérol extrêmes reflètent des situations cliniques réelles. Supprimer ces observations reviendrait à effacer les profils les plus pertinents pour la prévention.

### 2. Les mesures NHANES sont fiables
Les variables cliniques et anthropométriques sont mesurées par des professionnels selon des protocoles standardisés. Les valeurs extrêmes sont donc des données valides.

### 3. LightGBM gère très bien les valeurs extrêmes
Le modèle reposant sur des arbres de décision, il n’est pas sensible aux outliers et ne nécessite pas de distributions normales.

Il n’y a donc **aucune justification technique** à la suppression des valeurs extrêmes.

## Conclusion
Les valeurs extrêmes présentes dans les variables utilisées par les modèles sont :
- rares,
- plausibles,
- représentatives de profils à risque,
- et sans impact négatif sur LightGBM.

**Décision finale : aucune suppression d’outliers n’a été réalisée pour les modèles diabète et cholestérol.**
**Conserver ces valeurs garantit une meilleure sensibilité clinique et évite tout biais.**
