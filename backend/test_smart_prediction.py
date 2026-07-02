from tools.ml_tools.prediction_engine import (
    PredictionEngine
)

engine = PredictionEngine()

sample = [

    {

        "project_type":
            "reforestation",

        "location":
            "Maharashtra",

        "area_hectares":
            500,

        "duration_years":
            10,

        "baseline_emissions":
            25000,

        "expected_emission_reduction":
            12000,

        "emission_factor":
            0.85
    }

]

result = engine.predict(

    "GradientBoosting",

    sample

)

print(result)