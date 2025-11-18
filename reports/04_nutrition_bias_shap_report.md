# SHAP Analysis Report — Nutrition Bias & Decision Justification (EN + FR)

This report summarizes findings from four notebooks:
- **07_model_diab_opt.ipynb** fileciteturn3file3  
- **08_model_chol_opt.ipynb** fileciteturn3file2  
- **09_shap-model-diab.ipynb** fileciteturn3file1  
- **10_shap-model-chol.ipynb** fileciteturn3file0  

---

# A. English Version

## Objective
The purpose of these analyses was to evaluate whether nutritional variables from NHANES 2021–2023 were reliable predictors of **diabetes** and **high cholesterol**, and whether they should remain in the modeling pipeline.

SHAP explainability revealed systematic issues suggesting **declaration bias** and **reverse causality**: nutritional variables behaved more like *consequences* of the diseases rather than *causal predictors*.  
This led to their complete removal.

---

## Key Findings

## 1. Strong predictors were *not* nutrition-related
In both optimized models (diabetes and cholesterol), top predictors were:
- Age  
- Waist circumference  
- BMI (log)  
- Sex  
- Ethnicity  
- Physical activity  
- Sleep  

These showed stable, coherent SHAP patterns aligned with medical knowledge.

---

## 2. Nutrition variables showed unreliable SHAP behavior

### A. Declaration bias (self-reported dietary intake is systematically distorted)
NHANES dietary recall is known to suffer from **under-reporting**, especially:
- among individuals with obesity,  
- among patients already diagnosed with diabetes or dyslipidemia,  
- among participants who feel judged for “unhealthy” behaviors.

**SHAP results reflect exactly these distortions.**  
Common patterns observed:
- High sugar intake → *lower* predicted diabetes risk  
- Higher alcohol intake → *lower* cholesterol risk  
- High calorie intake → *protective* signal

These patterns are not physiologically plausible.  
They are consistent, however, with **patients with known disease reporting their diet differently**, often minimizing or modifying their declarations.

This indicates that nutrition features were capturing **how people report** food—not what they actually eat.

---

### B. Reverse causality (diet adapts *after* disease diagnosis)
A major issue revealed by SHAP is that nutrition variables often reflect **post-diagnosis behavioral changes**:
- People diagnosed with diabetes reduce sugars, carbs, and total calories.
- Individuals with high cholesterol may reduce fats and alcohol.
- Many start “corrective diets”, leading to an inverse association between intake and disease.

Thus, nutritional variables act as **effects of the disease**, not causes.

**SHAP detects these behavioral adjustments, not biological pathways.**

This creates misleading importance patterns and undermines the medical credibility of the model.

---

## 3. Instability and inconsistency across models
SHAP beeswarm plots show:
- Direction of effects flipping between diabetes and cholesterol models.
- Nutrition variables appearing important only in small, contradictory clusters.
- High variance and lack of repeatable structure.

This inconsistency confirms that the model is not learning a meaningful dietary signal.

---

## 4. Decision: Remove all nutrition variables

### All 8 nutrition variables were permanently removed from the modeling pipeline.

#### Reasons:
1. **Declaration bias** distorted associations.  
   People underreport unhealthy food, especially when sick.

2. **Reverse causality**: diet reflects the disease rather than causing it.  
   SHAP shows correlations driven by dietary *restrictions* after diagnosis.

3. **Clinical implausibility**:  
   The model was learning “noise” instead of physiological mechanisms.

4. **Model robustness** improves without them.  
   Predictive performance remains stable or slightly better.

5. **Interpretability and ethics**:  
   Using self-reported diet as a predictor could unfairly penalize honest respondents and mislead clinical interpretation.

These arguments justify the full removal of nutrition features.

---

# B. Version Française

## Objectif
L’objectif était d’évaluer la fiabilité des variables nutritionnelles de NHANES 2021–2023 dans la prédiction du **diabète** et du **cholestérol élevé**.

L’analyse SHAP a révélé deux problèmes majeurs :
- un **biais de déclaration** important (les personnes malades déclarent différemment ce qu’elles mangent),  
- un phénomène de **causalité inversée** (l’alimentation change *à cause* de la maladie).

Ces résultats ont conduit à la suppression totale des variables nutritionnelles.

---

## Résultats principaux

## 1. Les prédicteurs dominants n’étaient pas nutritionnels
Pour les deux modèles (diabète et cholestérol), les variables les plus informatives étaient :
- âge  
- tour de taille  
- IMC (log)  
- sexe  
- ethnicité  
- activité physique  
- sommeil  

Des résultats stables et cohérents avec les connaissances médicales.

---

## 2. Les variables nutritionnelles ont montré un comportement non fiable

### A. Biais de déclaration (auto-déclaration très imparfaite)
Les rappels alimentaires NHANES sont connus pour sous-estimer :
- les sucres,  
- les graisses,  
- l’alcool,  
- les calories totales.

De plus, **les personnes déjà malades sous-déclarent encore plus**.  
SHAP reflète ce biais :

- plus de sucres → *moins* de risque prédit de diabète  
- plus d’alcool → *moins* de risque de cholestérol  
- plus de calories → effet protecteur

Ces effets n’ont **aucun sens médical**, mais s’expliquent parfaitement par la **sous-déclaration volontaire ou involontaire**.

---

### B. Causalité inversée (les malades changent leur alimentation)
Les analyses montrent que :
- les patients diabétiques réduisent réellement sucres et calories,
- les personnes ayant du cholestérol diminuent graisses et alcool.

Le modèle détecte alors un signal inversé :  
**manger moins → être malade**,  
car les malades adaptent déjà leur alimentation.

Autrement dit :  
> Le contenu d’une assiette n’est pas la cause observée par le modèle, mais la *conséquence* du diagnostic et des recommandations médicales.

---

## 3. Instabilité des effets nutritionnels
Les effets SHAP :
- changent de direction entre les modèles diabète/cholestérol,
- varient fortement selon les sous-échantillons,
- ne forment jamais une structure cohérente.

Cette instabilité confirme l’absence de signal fiable.

---

## 4. Décision : Retirer toutes les variables nutritionnelles

### Les 8 variables nutritionnelles ont été supprimées du pipeline.

#### Motifs :
1. **Biais de déclaration massif** dans NHANES.  
2. **Causalité inversée** : l’alimentation reflète la maladie plutôt que de la prédire.  
3. **Non-pertinence clinique** des signaux détectés.  
4. **Robustesse accrue** sans ces variables.  
5. **Modèle plus explicable et plus éthique**.

Cette décision améliore la crédibilité scientifique du modèle, sa stabilité, et la confiance dans ses résultats.

---

# End of Report
