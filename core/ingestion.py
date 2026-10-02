from io import BytesIO

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
}


class IngestionError(Exception):
    """Raised when a source file cannot be ingested."""


def get_file_extension(filename: str) -> str:
    """
    Return the lowercase file extension.
    """
    if not filename or "." not in filename:
        raise IngestionError(
            "The uploaded file does not have a valid extension."
        )

    return "." + filename.rsplit(".", 1)[-1].lower()


def validate_file_type(filename: str) -> str:
    """
    Validate that the uploaded file is a supported format.
    """
    extension = get_file_extension(filename)

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))

        raise IngestionError(
            f"Unsupported file type '{extension}'. "
            f"Supported formats: {supported}."
        )

    return extension


def read_uploaded_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """
    Read an uploaded CSV or Excel file into a pandas DataFrame.

    This function intentionally performs NO:
    - cleaning
    - transformation
    - column mapping
    - analysis
    - AI processing

    Those responsibilities belong to later pipeline stages.
    """

    extension = validate_file_type(filename)

    try:

        if extension == ".csv":
            return pd.read_csv(BytesIO(file_bytes))

        if extension in {".xlsx", ".xls"}:
            return pd.read_excel(BytesIO(file_bytes))

    except Exception as exc:
        raise IngestionError(
            f"Unable to read '{filename}'. "
            "The file may be corrupted, password-protected, "
            "or contain an unsupported structure."
        ) from exc

    raise IngestionError(
        f"No ingestion handler exists for '{extension}'."
    )
