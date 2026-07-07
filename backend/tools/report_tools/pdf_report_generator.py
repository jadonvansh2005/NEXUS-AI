import os

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Image,

    PageBreak

)

from reportlab.lib.styles import (

    getSampleStyleSheet
)


class PDFReportGenerator:

    def generate(

        self,

        dataset_report,

        automl_result,

        eda_charts,

        model_charts,

        output_path="uploads/reports/report.pdf"

    ):

        os.makedirs(

            os.path.dirname(
                output_path
            ),

            exist_ok=True

        )

        doc = SimpleDocTemplate(
            output_path
        )

        styles = (
            getSampleStyleSheet()
        )

        story = []

        # =====================
        # TITLE
        # =====================

        story.append(

            Paragraph(

                "UPSS AutoML Report",

                styles["Title"]

            )

        )

        story.append(
            Spacer(1, 20)
        )

        # =====================
        # DATASET INFO
        # =====================

        story.append(

            Paragraph(

                "Dataset Summary",

                styles["Heading1"]

            )

        )

        story.append(

            Paragraph(

                f"Rows: {dataset_report['rows']}",

                styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"Columns: {dataset_report['columns']}",

                styles["BodyText"]

            )

        )

        story.append(
            Spacer(1, 10)
        )

        # =====================
        # AUTOML INFO
        # =====================

        story.append(

            Paragraph(

                "AutoML Results",

                styles["Heading1"]

            )

        )

        story.append(

            Paragraph(

                f"Problem Type: {automl_result['problem_type']}",

                styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"Target Column: {automl_result['target']}",

                styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"Best Model: {automl_result['best_model']}",

                styles["BodyText"]

            )

        )

        story.append(
            Spacer(1, 20)
        )

        # =====================
        # FEATURE IMPORTANCE
        # =====================

        if automl_result.get("pipeline_type") == "nlp":

            story.append(

                Paragraph(

                    "NLP Classification Results",

                    styles["Heading1"]

                )

            )

            story.append(

                Paragraph(

                    f"Best Model: {automl_result['best_model']}",

                    styles["BodyText"]

                )

            )

            story.append(

                Paragraph(

                    f"Accuracy: {automl_result['accuracy']:.4f}",

                    styles["BodyText"]

                )

            )

            story.append(

                Paragraph(

                    f"F1 Score: {automl_result['f1']:.4f}",

                    styles["BodyText"]

                )

            )

            story.append(
                Spacer(1, 20)
            )

        else:

            story.append(

                Paragraph(

                    "Top Features",

                    styles["Heading1"]

                )

            )

            for feature, score in list(

                automl_result.get(
                    "feature_scores",
                    {}
                ).items()

            )[:10]:

                story.append(

                    Paragraph(

                        f"{feature}: {score}",

                        styles["BodyText"]

                    )

                )

            story.append(
                Spacer(1, 20)
            )
        # =====================
        # EDA CHARTS
        # =====================

        story.append(

            PageBreak()
        )

        story.append(

            Paragraph(

                "EDA Charts",

                styles["Heading1"]

            )

        )

        for chart in eda_charts[:5]:

            if os.path.exists(
                chart
            ):

                story.append(

                    Image(

                        chart,

                        width=400,

                        height=250

                    )

                )

                story.append(
                    Spacer(1, 10)
                )

        # =====================
        # MODEL CHARTS
        # =====================

        story.append(

            PageBreak()
        )

        story.append(

            Paragraph(

                "Model Visualizations",

                styles["Heading1"]

            )

        )

        for chart in model_charts.values():

            if chart and os.path.exists(
                chart
            ):

                story.append(

                    Image(

                        chart,

                        width=400,

                        height=250

                    )

                )

                story.append(
                    Spacer(1, 10)
                )

        # =====================
        # BUILD PDF
        # =====================

        doc.build(
            story
        )

        return output_path