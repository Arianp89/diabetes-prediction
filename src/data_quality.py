
import pandas as pd


SUSPICIOUS_ZERO_COLUMNS = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
]


def check_missing_values(data: pd.DataFrame) -> pd.Series:
    """Return the number of missing values in each column."""
    return data.isnull().sum()


def check_duplicates(data: pd.DataFrame) -> int:
    """Return the number of duplicated rows."""
    return int(data.duplicated().sum())


def check_suspicious_zeros(data: pd.DataFrame) -> pd.Series:
    """Count suspicious zero values in selected medical features."""
    return data[SUSPICIOUS_ZERO_COLUMNS].eq(0).sum()


def check_data_types(data: pd.DataFrame) -> pd.Series:
    """Return the data type of each column."""
    return data.dtypes


def check_outliers(data: pd.DataFrame) -> pd.Series:
    """Count potential outliers using the IQR method."""
    numeric_data = data.select_dtypes(include="number")
    q1 = numeric_data.quantile(0.25)
    q3 = numeric_data.quantile(0.75)

    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = (
        (numeric_data.lt(lower_bound))
        | (numeric_data.gt(upper_bound))
    )

    return outliers.sum()


def generate_quality_report(data: pd.DataFrame) -> dict:
    """Generate a basic data quality report."""
    return {
        "missing_values": check_missing_values(data),
        "duplicate_rows": check_duplicates(data),
        "suspicious_zeros": check_suspicious_zeros(data),
        "data_types": check_data_types(data),
        "potential_outliers": check_outliers(data),
    }
