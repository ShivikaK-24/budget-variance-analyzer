import pandas as pd


def clean_dataframe(df: pd.DataFrame):
    """
    Apply safe, deterministic cleaning transformations.

    Returns:
        cleaned_df: transformed dataframe
        transformation_log: list of changes performed
    """

    if df is None:
        raise ValueError("Dataframe cannot be None.")

    cleaned_df = df.copy()
    transformation_log = []

    # ========================================================
    # 1. CLEAN COLUMN NAMES
    # ========================================================

    original_columns = list(cleaned_df.columns)

    cleaned_columns = [
        str(column).strip()
        for column in cleaned_df.columns
    ]

    if cleaned_columns != original_columns:

        transformation_log.append({
            "type": "column_name_cleanup",
            "description": "Removed leading/trailing spaces from column names.",
            "columns_affected": [
                original
                for original, cleaned in zip(
                    original_columns,
                    cleaned_columns
                )
                if original != cleaned
            ],
        })

        cleaned_df.columns = cleaned_columns

    # ========================================================
    # 2. TRIM TEXT VALUES
    # ========================================================

    text_columns = cleaned_df.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    trimmed_columns = []

    for column in text_columns:

        before = cleaned_df[column].copy()

        cleaned_df[column] = cleaned_df[column].apply(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

        if not before.equals(cleaned_df[column]):
            trimmed_columns.append(column)

    if trimmed_columns:

        transformation_log.append({
            "type": "text_cleanup",
            "description": "Removed leading/trailing spaces from text values.",
            "columns_affected": trimmed_columns,
        })

    # ========================================================
    # 3. NUMERIC CONVERSION
    # ========================================================

    for column in cleaned_df.columns:

        if cleaned_df[column].dtype not in [
            "object",
            "string",
        ]:
            continue

        converted = pd.to_numeric(
            cleaned_df[column],
            errors="coerce",
        )

        original_non_null = cleaned_df[column].notna().sum()
        converted_non_null = converted.notna().sum()

        if (
            original_non_null > 0
            and converted_non_null == original_non_null
        ):

            cleaned_df[column] = converted

            transformation_log.append({
                "type": "numeric_conversion",
                "description": (
                    "Converted a text column to numeric "
                    "because all non-empty values were numeric."
                ),
                "columns_affected": [column],
            })

    # ========================================================
    # 4. DUPLICATE DETECTION
    # ========================================================

    duplicate_count = int(cleaned_df.duplicated().sum())

    if duplicate_count > 0:

        transformation_log.append({
            "type": "duplicate_detection",
            "description": (
                f"Detected {duplicate_count} duplicate row(s). "
                "No rows were automatically deleted."
            ),
            "rows_affected": duplicate_count,
        })

    return cleaned_df, transformation_log
