# NHANES Health Predictor — Hugging Face version (no API)

import gradio as gr
import joblib
import numpy as np
import pandas as pd

# ====== THEME ======
theme = gr.themes.Monochrome(
    primary_hue="blue",
    font=["Roboto", "Arial", "sans-serif"]
)

# ====== LOAD MODELS AND SCALERS ======
# They must be present in the Space repo
model_diab = joblib.load("artifacts_diab_no_bias/model_lightgbm_diab_no_bias.pkl")
scaler_diab = joblib.load("artifacts_diab_no_bias/scaler_diab_no_bias.pkl")

model_chol = joblib.load("artifacts_chol_no_bias/model_lightgbm_chol_no_bias.pkl")
scaler_chol = joblib.load("artifacts_chol_no_bias/scaler_chol_no_bias.pkl")

# ====== FEATURE ORDER (must match notebooks 11 & 12) ======
# Common feature set used for both models
feature_cols = [
    "RIDAGEYR",
    "RIAGENDR",
    "smoker",
    "BMXBMI_log",
    "BMXWAIST",
    "PAD680_log",
    "SLD012",
    "ethnicity_MexicanAmerican",
    "ethnicity_OtherHispanic",
    "ethnicity_NonHispanicWhite",
    "ethnicity_NonHispanicBlack",
    "ethnicity_NonHispanicAsian",
    "ethnicity_OtherRace",
]

# Columns considered binary during training (not standardized)
binary_cols = [
    "RIAGENDR",
    "smoker",
    "ethnicity_MexicanAmerican",
    "ethnicity_OtherHispanic",
    "ethnicity_NonHispanicWhite",
    "ethnicity_NonHispanicBlack",
    "ethnicity_NonHispanicAsian",
    "ethnicity_OtherRace",
]

# Numerical columns standardized by the scalers
num_cols = [c for c in feature_cols if c not in binary_cols]


# ====== PREDICTION FUNCTION (NO API) ======
def predict_risk(
    age, sex, smoker,
    weight_kg, height_m, waist_cm,
    sleep_hours_per_day,
    sitting_time_min_per_day,
    ethnicity,
):
    # --- Basic sanity checks to avoid crashes ---
    if height_m is None or height_m <= 0:
        return [("Invalid height — must be > 0", None)], [("Invalid height — must be > 0", None)], {
            "error": "height_m must be positive"
        }
    if weight_kg is None or weight_kg <= 0:
        return [("Invalid weight — must be > 0", None)], [("Invalid weight — must be > 0", None)], {
            "error": "weight_kg must be positive"
        }
    if age is None or age <= 0:
        return [("Invalid age — must be > 0", None)], [("Invalid age — must be > 0", None)], {
            "error": "age must be positive"
        }

    # Sex encoding (NHANES: 1 = male, 2 = female)
    sex_num = 1 if sex == "male" else 2

    # One-hot encoding ethnicity (same labels as in the notebooks)
    eth = {
        "ethnicity_MexicanAmerican": 1 if ethnicity == "MexicanAmerican" else 0,
        "ethnicity_OtherHispanic": 1 if ethnicity == "OtherHispanic" else 0,
        "ethnicity_NonHispanicWhite": 1 if ethnicity == "NonHispanicWhite" else 0,
        "ethnicity_NonHispanicBlack": 1 if ethnicity == "NonHispanicBlack" else 0,
        "ethnicity_NonHispanicAsian": 1 if ethnicity == "NonHispanicAsian" else 0,
        "ethnicity_OtherRace": 1 if ethnicity == "OtherRace" else 0,
    }

    # --- Derived features to match training preprocessing ---
    # BMI (kg/m²) then log-transform (noted *_log in the notebooks)
    bmi = weight_kg / (height_m ** 2)
    # log1p is safe if we ever hit 0; it is a very close proxy to log for positive values
    bmi_log = float(np.log1p(bmi))

    # Sitting time: minutes per day -> log1p, as in the feature PAD680_log
    sitting_time = max(float(sitting_time_min_per_day), 0.0)
    pad680_log = float(np.log1p(sitting_time))

    # Build feature row with EXACT same feature names as during training
    row = pd.DataFrame([{
        "RIDAGEYR": float(age),
        "RIAGENDR": float(sex_num),
        "smoker": int(bool(smoker)),
        "BMXBMI_log": bmi_log,
        "BMXWAIST": float(waist_cm),
        "PAD680_log": pad680_log,
        "SLD012": float(sleep_hours_per_day),
        **eth,
    }])

    # Ensure correct column order
    row = row[feature_cols].copy()

    # Apply model-specific scalers only on numerical columns
    row_diab = row.copy()
    row_diab[num_cols] = scaler_diab.transform(row_diab[num_cols])

    row_chol = row.copy()
    row_chol[num_cols] = scaler_chol.transform(row_chol[num_cols])

    # Predictions (probabilities of the positive class)
    diab_prob = float(model_diab.predict_proba(row_diab[feature_cols])[0][1])
    chol_prob = float(model_chol.predict_proba(row_chol[feature_cols])[0][1])

    # Hard classification using threshold 0.40 for diab, 0.35 for chol
    diab_class = int(diab_prob >= 0.40)
    chol_class = int(chol_prob >= 0.35)

    # Gradio HighlightedText needs a list of (text, label/color)
    diab_text = f"Diabetes risk: {diab_prob * 100:.1f}% — Class {diab_class}"
    chol_text = f"High cholesterol risk: {chol_prob * 100:.1f}% — Class {chol_class}"

    raw_json = {
        "diabetes": {
            "probability": diab_prob,
            "prediction": diab_class,
        },
        "chol_high": {
            "probability": chol_prob,
            "prediction": chol_class,
        },
    }

    return [(diab_text, None)], [(chol_text, None)], raw_json


# ====== INTERFACE ======
with gr.Blocks(theme=theme, title="NHANES Health Risk Predictor") as demo:
    gr.Markdown(
        "# NHANES Health Risk Predictor\n"
        "### Two ML models trained on 5,000+ NHANES participants (2021–2023)\n"
        "---"
    )

    gr.Markdown("## Patient information")

    with gr.Row():
        with gr.Column():
            age = gr.Number(label="Age (years)", value=45)
            sex = gr.Radio(["male", "female"], label="Sex", value="male")
            smoker = gr.Checkbox(label="Current smoker", value=False)

            weight_kg = gr.Number(label="Weight (kg)", value=80)
            height_m = gr.Number(label="Height (m)", value=1.75)
            waist_cm = gr.Number(label="Waist circumference (cm)", value=100)

            sleep_hours_per_day = gr.Number(label="Sleep (hours per day)", value=7)
            sitting_time_min_per_day = gr.Number(label="Sitting time (min per day)", value=420)

            ethnicity = gr.Radio(
                [
                    "MexicanAmerican",
                    "NonHispanicWhite",
                    "NonHispanicBlack",
                    "NonHispanicAsian",
                    "OtherHispanic",
                    "OtherRace",
                ],
                label="Ethnicity",
                value="NonHispanicWhite",
            )

    predict_btn = gr.Button("Predict risk", variant="primary")

    diab_out = gr.HighlightedText(label="Diabetes prediction")
    chol_out = gr.HighlightedText(label="Cholesterol prediction")
    raw_out = gr.JSON(label="Raw model outputs")

    predict_btn.click(
        predict_risk,
        [
            age,
            sex,
            smoker,
            weight_kg,
            height_m,
            waist_cm,
            sleep_hours_per_day,
            sitting_time_min_per_day,
            ethnicity,
        ],
        [diab_out, chol_out, raw_out],
    )

if __name__ == "__main__":
    demo.launch()
