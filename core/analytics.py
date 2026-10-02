import pandas as pd


def calculate_variance(
    df: pd.DataFrame,
    budget_column: str,
    actual_column: str,
) -> pd.DataFrame:
    """
    Calculate row-level budget vs actual variance.

    Variance = Actual - Budget
    """

    if budget_column not in df.columns:
        raise ValueError(
            f"Budget column '{budget_column}' was not found."
        )

    if actual_column not in df.columns:
        raise ValueError(
            f"Actual column '{actual_column}' was not found."
        )

    result = df.copy()

    result["Variance"] = (
        result[actual_column] - result[budget_column]
    )

    result["Variance %"] = (
        result["Variance"]
        / result[budget_column].replace(0, pd.NA)
    ) * 100

    return result


def calculate_summary(
    df: pd.DataFrame,
    budget_column: str,
    actual_column: str,
) -> dict:
    """
    Calculate overall budget vs actual summary metrics.
    """

    total_budget = df[budget_column].sum()
    total_actual = df[actual_column].sum()

    total_variance = total_actual - total_budget

    if total_budget != 0:
        variance_percentage = (
            total_variance / total_budget
        ) * 100
    else:
        variance_percentage = None

    return {
        "total_budget": total_budget,
        "total_actual": total_actual,
        "total_variance": total_variance,
        "variance_percentage": variance_percentage,
    }
def identify_variance_status(variance: float) -> str:
    """
    Classify a variance based on its direction.
    """

    if variance > 0:
        return "unfavorable"

    if variance < 0:
        return "favorable"

    return "on_budget"


def generate_summary_insights(summary: dict) -> list:
    """
    Generate deterministic observations from summary metrics.

    These are factual observations only.
    AI commentary will be added later.
    """

    insights = []

    total_variance = summary["total_variance"]
    variance_percentage = summary["variance_percentage"]

    if total_variance > 0:

        insights.append(
            f"Actual spending is {abs(variance_percentage):.2f}% "
            "above the total budget."
        )

    elif total_variance < 0:

        insights.append(
            f"Actual spending is {abs(variance_percentage):.2f}% "
            "below the total budget."
        )

    else:

        insights.append(
            "Actual spending is exactly aligned with the total budget."
        )

    return insights
def calculate_category_analysis(
    df: pd.DataFrame,
    category_column: str,
    budget_column: str,
    actual_column: str,
) -> pd.DataFrame:
    """
    Calculate budget vs actual performance
    across any categorical dimension.
    """

    required_columns = [
        category_column,
        budget_column,
        actual_column,
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required column(s) not found: {missing_columns}"
        )

    grouped = (
        df.groupby(category_column, dropna=False)
        .agg(
            Budget=(budget_column, "sum"),
            Actual=(actual_column, "sum"),
        )
        .reset_index()
    )

    grouped["Variance"] = (
        grouped["Actual"] - grouped["Budget"]
    )

    grouped["Variance %"] = (
        grouped["Variance"]
        / grouped["Budget"].replace(0, pd.NA)
    ) * 100

    return grouped.sort_values(
        "Variance",
        ascending=False,
    ).reset_index(drop=True)
def calculate_trend_analysis(
    df: pd.DataFrame,
    date_column: str,
    budget_column: str,
    actual_column: str,
) -> pd.DataFrame:
    """
    Calculate budget vs actual trends over time.

    Dates are normalized to monthly periods.
    """

    required_columns = [
        date_column,
        budget_column,
        actual_column,
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required column(s) not found: {missing_columns}"
        )

    result = df.copy()

    result[date_column] = pd.to_datetime(
        result[date_column],
        errors="coerce",
    )

    result = result.dropna(subset=[date_column])

    if result.empty:
        return pd.DataFrame(
            columns=[
                "Period",
                "Budget",
                "Actual",
                "Variance",
                "Variance %",
            ]
        )

    result["Period"] = (
        result[date_column]
        .dt.to_period("M")
        .astype(str)
    )

    trend = (
        result.groupby("Period")
        .agg(
            Budget=(budget_column, "sum"),
            Actual=(actual_column, "sum"),
        )
        .reset_index()
    )

    trend["Variance"] = (
        trend["Actual"] - trend["Budget"]
    )

    trend["Variance %"] = (
        trend["Variance"]
        / trend["Budget"].replace(0, pd.NA)
    ) * 100

    return trend.sort_values(
        "Period"
    ).reset_index(drop=True)
