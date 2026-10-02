import pandas as pd

from services.ai_service import ask_groq


def answer_question(
    df: pd.DataFrame,
    question: str,
) -> str:
    """
    Answer a user question using the uploaded dataframe.

    The dataframe is provided to the LLM as context.
    The model is instructed to stay grounded in the data.
    """

    if df is None or df.empty:
        return "There is no data available to analyze."

    if not question.strip():
        return "Please enter a question."

    # Keep the context compact enough for the local model.
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
3. Perform comparisons and calculations when they can be derived
   directly from the data.
4. Keep the answer concise and business-focused.
5. Mention the relevant numbers supporting your answer.
6. Do not assume that a column has a meaning unless the data
   clearly supports it.

USER QUESTION:
{question}

DATASET:
{data_context}

Answer the question directly.
"""

    return ask_groq(prompt)
