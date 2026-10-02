import pandas as pd

from services.ai_service import ask_groq


def _find_column(df, candidates):
    for candidate in candidates:
        for column in df.columns:
            if str(column).strip().lower() == candidate:
                return column

    for candidate in candidates:
        for column in df.columns:
            if candidate in str(column).strip().lower():
                return column

    return None


def _calculate_financial_answer(df, question):
    q = question.lower().strip()

    budget_col = _find_column(
        df,
        ["budget", "planned", "plan", "allocated"]
    )

    actual_col = _find_column(
        df,
        ["actual", "spent", "spending", "expense", "expenses"]
    )

    category_col = _find_column(
        df,
        ["department", "category", "business unit", "business_unit",
         "cost center", "cost_center", "division", "region"]
    )

    if not budget_col or not actual_col:
        return None

    working = df.copy()

    working[budget_col] = pd.to_numeric(
        working[budget_col],
        errors="coerce"
    )

    working[actual_col] = pd.to_numeric(
        working[actual_col],
        errors="coerce"
    )

    working = working.dropna(
        subset=[budget_col, actual_col]
    )

    if working.empty:
        return None

    working["_variance"] = (
        working[actual_col] - working[budget_col]
    )

    # Total actual spending
    if (
        "total actual" in q
        or "total spending" in q
        or "total spend" in q
        or "actual spending" in q
    ):
        total_actual = working[actual_col].sum()

        return (
            f"Total actual spending is "
            f"{total_actual:,.2f}."
        )

    # Total budget
    if "total budget" in q:
        total_budget = working[budget_col].sum()

        return (
            f"Total budget is "
            f"{total_budget:,.2f}."
        )

    # Overall / total variance
    if (
        "overall variance" in q
        or "total variance" in q
        or "overall budget variance" in q
    ):
        total_budget = working[budget_col].sum()
        total_actual = working[actual_col].sum()
        variance = total_actual - total_budget

        if total_budget != 0:
            variance_pct = (variance / total_budget) * 100
            return (
                f"Overall budget variance is "
                f"{variance:,.2f}, which is "
                f"{variance_pct:.2f}% "
                f"(Actual minus Budget)."
            )

        return (
            f"Overall budget variance is "
            f"{variance:,.2f} "
            f"(Actual minus Budget)."
        )

    # Highest variance by department/category
    if (
        category_col
        and (
            "highest variance" in q
            or "largest variance" in q
            or "highest budget variance" in q
        )
    ):
        grouped = (
            working
            .groupby(category_col, dropna=False)
            .agg(
                Budget=(budget_col, "sum"),
                Actual=(actual_col, "sum"),
            )
        )

        grouped["Variance"] = (
            grouped["Actual"] - grouped["Budget"]
        )

        highest = grouped["Variance"].idxmax()
        value = grouped.loc[highest, "Variance"]

        return (
            f"{highest} has the highest budget variance "
            f"at {value:,.2f} "
            f"(Actual minus Budget)."
        )

    # Largest overspend
    if (
        category_col
        and (
            "highest overspend" in q
            or "largest overspend" in q
            or "most overspent" in q
        )
    ):
        grouped = (
            working
            .groupby(category_col, dropna=False)
            .agg(
                Budget=(budget_col, "sum"),
                Actual=(actual_col, "sum"),
            )
        )

        grouped["Variance"] = (
            grouped["Actual"] - grouped["Budget"]
        )

        overspending = grouped[
            grouped["Variance"] > 0
        ]

        if overspending.empty:
            return "No department or category is currently over budget."

        highest = overspending["Variance"].idxmax()
        value = overspending.loc[highest, "Variance"]

        return (
            f"{highest} has the largest overspend at "
            f"{value:,.2f}."
        )

    # Which departments/categories are over budget
    if (
        category_col
        and (
            "over budget" in q
            or "overbudget" in q
            or "overspending" in q
        )
    ):
        grouped = (
            working
            .groupby(category_col, dropna=False)
            .agg(
                Budget=(budget_col, "sum"),
                Actual=(actual_col, "sum"),
            )
        )

        grouped["Variance"] = (
            grouped["Actual"] - grouped["Budget"]
        )

        over_budget = grouped[
            grouped["Variance"] > 0
        ]

        if over_budget.empty:
            return "No department or category is over budget."

        results = []

        for name, row in over_budget.iterrows():
            results.append(
                f"{name}: {row['Variance']:,.2f}"
            )

        return (
            "The following departments/categories are over budget: "
            + "; ".join(results)
        )

    return None


def answer_question(
    df: pd.DataFrame,
    question: str,
) -> str:

    if df is None or df.empty:
        return "There is no data available to analyze."

    if not question.strip():
        return "Please enter a question."

    # First try deterministic financial reasoning.
    deterministic_answer = _calculate_financial_answer(
        df,
        question
    )

    if deterministic_answer:
        return deterministic_answer

    # Use Groq for questions that require natural-language interpretation.
    data_context = df.to_string(
        index=False,
        max_rows=200,
    )

    prompt = f"""
You are an FP&A financial data analyst.

Answer the user's question using ONLY the dataset provided below.

IMPORTANT RULES:
1. Do not invent numbers, companies, years, or facts.
2. If the dataset does not contain enough information, say so.
3. Perform calculations directly from the data when possible.
4. Keep the answer concise and business-focused.
5. Mention the relevant numbers supporting your answer.
6. Do not assume meanings that are not supported by the dataset.
7. For budget variance, use:
   Variance = Actual - Budget

USER QUESTION:
{question}

DATASET:
{data_context}

Answer the question directly.
"""

    return ask_groq(prompt)
