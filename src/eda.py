
import matplotlib.pyplot as plt
import pandas as pd

from src.config import figure_dir, target_column


class EDAAnalyzer:
    """Perform exploratory data analysis using Matplotlib."""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.figure_dir = figure_dir
        self.figure_dir.mkdir(parents=True, exist_ok=True)

    def summarize(self) -> None:
        """Print basic statistical information."""
        print("\nDataset shape:")
        print(self.data.shape)

        print("\nStatistical summary:")
        print(self.data.describe().T)

        print("\nTarget distribution:")
        print(self.data[target_column].value_counts().sort_index())

        print("\nTarget distribution (%):")
        print(
            self.data[target_column]
            .value_counts(normalize=True)
            .sort_index()
            .mul(100)
            .round(2)
        )

    def plot_target_distribution(self) -> None:
        """Plot the number of samples in each target class."""
        counts = self.data[target_column].value_counts().sort_index()

        plt.figure(figsize=(7, 5))
        plt.bar(
            counts.index.astype(str),
            counts.values,
            edgecolor="black",
        )

        plt.title("Target Class Distribution")
        plt.xlabel("Outcome (0 = No Diabetes, 1 = Diabetes)")
        plt.ylabel("Number of Samples")
        plt.tight_layout()

        self._save_figure("target_distribution.png")

    def plot_feature_distributions(self) -> None:
        """Plot histograms for numerical features."""
        features = self.data.drop(columns=[target_column])

        features.hist(
            figsize=(15, 12),
            bins=25,
            edgecolor="black",
        )

        plt.suptitle("Feature Distributions", fontsize=16)
        plt.tight_layout()

        self._save_figure("feature_distributions.png")

    def plot_correlation_matrix(self) -> None:
        """Plot correlations between numerical columns."""
        correlation = self.data.corr(numeric_only=True)
        columns = correlation.columns

        fig, ax = plt.subplots(figsize=(11, 8))

        image = ax.imshow(
            correlation,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            aspect="auto",
        )

        ax.set_xticks(range(len(columns)))
        ax.set_yticks(range(len(columns)))
        ax.set_xticklabels(columns, rotation=45, ha="right")
        ax.set_yticklabels(columns)

        for row in range(len(columns)):
            for col in range(len(columns)):
                ax.text(
                    col,
                    row,
                    f"{correlation.iloc[row, col]:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                )

        fig.colorbar(image, ax=ax, label="Correlation")
        ax.set_title("Feature Correlation Matrix")
        fig.tight_layout()

        self._save_figure("correlation_matrix.png")

    def plot_features_by_target(self) -> None:
        """Compare feature distributions across target classes."""
        features = self.data.drop(columns=[target_column]).columns

        for feature in features:
            group_0 = self.data.loc[
                self.data[target_column] == 0, feature
            ].dropna()

            group_1 = self.data.loc[
                self.data[target_column] == 1, feature
            ].dropna()

            fig, ax = plt.subplots(figsize=(7, 5))

            ax.boxplot(
                [group_0, group_1],
                tick_labels=["0 (No Diabetes)", "1 (Diabetes)"],
            )

            ax.set_title(f"{feature} by Outcome")
            ax.set_xlabel("Outcome")
            ax.set_ylabel(feature)
            fig.tight_layout()

            self._save_figure(f"{feature.lower()}_by_outcome.png")

    def _save_figure(self, filename: str) -> None:
        """Save the current plot and close its figure."""
        output_path = self.figure_dir / filename

        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"Saved figure: {output_path}")

    def run(self) -> None:
        """Run the complete exploratory analysis."""
        self.summarize()
        self.plot_target_distribution()
        self.plot_feature_distributions()
        self.plot_correlation_matrix()
        self.plot_features_by_target()

        print("\nEDA completed successfully.")
