from tools.ds_tools.dataset_analyzer import (
    DatasetAnalyzer
)

from tools.ds_tools.visualization_generator import (
    VisualizationGenerator
)

from tools.ml_tools.automl_engine import (
    AutoMLEngine
)

from tools.ml_tools.model_visualizer import (
    ModelVisualizer
)

from tools.report_tools.pdf_report_generator import (
    PDFReportGenerator
)


class DataScienceService:

    def analyze_dataset(
        self,
        file_path
    ):

        analyzer = DatasetAnalyzer()

        dataset_report = (
            analyzer.analyze(
                file_path
            )
        )

        visualizer = (
            VisualizationGenerator()
        )

        eda_charts = (
            visualizer.generate(
                file_path
            )
        )

        automl = (
            AutoMLEngine()
        )

        automl_result = (
            automl.run(
                file_path
            )
        )

        model_visualizer = (
            ModelVisualizer()
        )

        model_charts = {}

        if (

            "results" in automl_result

            and

            "feature_scores" in automl_result

        ):

            model_charts = (

                model_visualizer.generate_all(

                    automl_result.get(
                        "results",
                        {}
                    ),

                    automl_result.get(
                        "feature_scores",
                        {}
                    ),

                    automl_result.get(
                        "model_importance",
                        {}
                    ),

                    automl_result.get(
                        "problem_type",
                        "classification"
                    )

                )

            )
        pdf_generator = (
            PDFReportGenerator()
        )

        pdf_path = (

            pdf_generator.generate(

                dataset_report,

                automl_result,

                eda_charts,

                model_charts

            )

        )

        print("\n========== AUTOML RESULT ==========")

        print(
            automl_result.keys()
        )

        print(
            automl_result
        )

        print("===================================")

        return {

            "dataset_report":
                dataset_report,

            "automl":
                automl_result,

            "pdf_report":
                pdf_path
        }