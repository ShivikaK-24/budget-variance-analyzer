import pandas as pd


def classify_column(series: pd.Series) -> str:
    """
    Classify a column into a broad data type.
    """

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    return "categorical"


def profile_dataframe(df: pd.DataFrame) -> dict:
    """
    Profile an uploaded dataframe.

    This function performs NO cleaning or transformation.
    It only describes the existing data.
    """

    if df is None:
        raise ValueError("Dataframe cannot be None.")

    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": [],
        "duplicate_rows": int(df.duplicated().sum()),
        "total_missing_values": int(df.isna().sum().sum()),
    }

    for column in df.columns:

        series = df[column]

        column_info = {
            "name": str(column),
            "data_type": classify_column(series),
            "pandas_dtype": str(series.dtype),
            "missing_values": int(series.isna().sum()),
            "missing_percentage": round(
                float(series.isna().mean() * 100),
                2,
            ),
            "unique_values": int(series.nunique(dropna=True)),
        }

        profile["columns"].append(column_info)

    return profile
