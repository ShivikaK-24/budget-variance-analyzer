def summarize_transformations(transformation_log: list) -> dict:
    """
    Convert the raw transformation log into a UI-friendly summary.
    """

    if not transformation_log:
        return {
            "total_changes": 0,
            "summary": "No transformations were required.",
            "items": [],
        }

    items = []

    for entry in transformation_log:

        transformation_type = entry.get("type")
        description = entry.get("description", "")

        item = {
            "type": transformation_type,
            "description": description,
        }

        if "columns_affected" in entry:
            item["columns_affected"] = entry["columns_affected"]

        if "rows_affected" in entry:
            item["rows_affected"] = entry["rows_affected"]

        items.append(item)

    return {
        "total_changes": len(items),
        "summary": (
            f"{len(items)} transformation or data-quality "
            f"event(s) detected."
        ),
        "items": items,
    }
COLUMN_HINTS = {
    "budget": [
        "budget",
        "planned",
        "plan",
        "target",
        "forecast",
        "allocated",
    ],
    "actual": [
        "actual",
        "spent",
        "spend",
        "expense",
        "expenses",
        "cost",
        "actuals",
    ],
    "category": [
        "department",
        "category",
        "business unit",
        "business_unit",
        "cost center",
        "cost_center",
        "division",
        "region",
    ],
        "date": [
        "date",
        "transaction date",
        "invoice date",
        "posting date",
        "period",
        "month",
        "year",
        "fiscal year",
        "fiscal month",
    ],
}


def suggest_column_mappings(columns: list) -> dict:
    """
    Suggest possible business meanings for uploaded columns.

    Suggestions are NOT automatically applied.
    """

    suggestions = {}

    for column in columns:

        column_name = str(column).strip().lower()

        matched_concepts = []

        for concept, keywords in COLUMN_HINTS.items():

            if any(
                keyword in column_name
                for keyword in keywords
            ):
                matched_concepts.append(concept)

        suggestions[str(column)] = matched_concepts

    return suggestions
def resolve_column_mappings(columns: list) -> dict:
    """
    Resolve column meanings when there is exactly one
    unambiguous candidate.

    Ambiguous mappings are left unresolved.
    """

    suggestions = suggest_column_mappings(columns)

    resolved = {
        "budget": None,
        "actual": None,
        "category": None,
        "date": None,
        "ambiguous": {},
    }

    for column, concepts in suggestions.items():

        if len(concepts) == 1:

            concept = concepts[0]

            # Only assign if this concept has not already
            # been assigned to another column.
            if resolved[concept] is None:
                resolved[concept] = column
            else:
                resolved["ambiguous"][column] = concepts

        elif len(concepts) > 1:

            resolved["ambiguous"][column] = concepts

    return resolved
