import os

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd


class VisualizationGenerator:

    def generate(
        self,
        file_path: str
    ):

        df = pd.read_csv(
            file_path
        )

        output_dir = (
            "uploads/reports/charts"
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        charts = []

        numeric_df = (
            df.select_dtypes(
                include="number"
            )
        )

        # ==================
        # Correlation Heatmap
        # ==================

        if len(
            numeric_df.columns
        ) > 1:

            plt.figure(
                figsize=(10, 8)
            )

            sns.heatmap(
                numeric_df.corr(),
                annot=True
            )

            heatmap_path = (
                f"{output_dir}/heatmap.png"
            )

            plt.savefig(
                heatmap_path
            )

            plt.close()

            charts.append(
                heatmap_path
            )

        # ==================
        # Histograms
        # ==================

        for col in (
            numeric_df.columns
        ):

            plt.figure()

            numeric_df[col].hist()

            chart_path = (
                f"{output_dir}/hist_{col}.png"
            )

            plt.title(
                col
            )

            plt.savefig(
                chart_path
            )

            plt.close()

            charts.append(
                chart_path
            )

        # ==================
        # Boxplots
        # ==================

        for col in numeric_df.columns:

            plt.figure()

            sns.boxplot(
                y=numeric_df[col]
            )

            chart_path = (
                f"{output_dir}/box_{col}.png"
            )

            plt.title(
                f"Boxplot - {col}"
            )

            plt.savefig(
                chart_path
            )

            plt.close()

            charts.append(
                chart_path
            )

        # ==================
        # Scatterplots
        # ==================

        cols = list(
            numeric_df.columns
        )

        for i in range(
            len(cols)
        ):

            for j in range(
                i + 1,
                len(cols)
            ):

                plt.figure(
                    figsize=(6, 4)
                )

                sns.scatterplot(
                    x=numeric_df[
                        cols[i]
                    ],
                    y=numeric_df[
                        cols[j]
                    ]
                )

                chart_path = (
                    f"{output_dir}/scatter_{cols[i]}_{cols[j]}.png"
                )

                plt.savefig(
                    chart_path
                )

                plt.close()

                charts.append(
                    chart_path
                )

        
        # ==================
        # Barplots
        # ==================

        cat_cols = (
            df.select_dtypes(
                include=[
                    "object",
                    "category"
                ]
            ).columns
        )

        for col in cat_cols:

            plt.figure(
                figsize=(8, 5)
            )

            df[col] \
                .value_counts() \
                .head(10) \
                .plot(
                    kind="bar"
                )

            chart_path = (
                f"{output_dir}/bar_{col}.png"
            )

            plt.savefig(
                chart_path
            )

            plt.close()

            charts.append(
                chart_path
            )

        # ==================
        # Pairplot
        # ==================

        if len(
            numeric_df.columns
        ) >= 2:

            pairplot = (
                sns.pairplot(
                    numeric_df.head(
                        1000
                    )
                )
            )

            chart_path = (
                f"{output_dir}/pairplot.png"
            )

            pairplot.savefig(
                chart_path
            )

            plt.close()

            charts.append(
                chart_path
            )

        return charts