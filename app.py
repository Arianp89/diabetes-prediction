
from flask import Flask, render_template, request
from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static")

MODEL_PATH = "diabetes_model.pkl"
model = joblib.load(MODEL_PATH)

FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    try:
        values = {
            feature: float(request.form[feature])
            for feature in FEATURES
        }

        input_data = pd.DataFrame(
            [values],
            columns=FEATURES
        )

        prediction = int(model.predict(input_data)[0])

        if prediction == 1:
            result_title = "Higher Predicted Likelihood"
            result_message = (
                "The model predicts the positive class "
                "for the provided data."
            )
            result_status = "positive"
            result_icon = "!"
        else:
            result_title = "Lower Predicted Likelihood"
            result_message = (
                "The model predicts the negative class "
                "for the provided data."
            )
            result_status = "negative"
            result_icon = "✓"

        return render_template(
            "result.html",
            result_title=result_title,
            result_message=result_message,
            result_status=result_status,
            result_icon=result_icon
        )

    except (ValueError, KeyError):
        return "Invalid input. Please check all fields.", 400
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
