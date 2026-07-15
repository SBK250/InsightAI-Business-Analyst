"""
Data Loader Service

Responsible for loading CSV and Excel files.
"""

from typing import Optional

import pandas as pd


class DataLoader:
    """Handles loading datasets into pandas DataFrames."""

    @staticmethod
    def load_file(uploaded_file) -> Optional[pd.DataFrame]:
        """
        Load CSV or Excel file.

        Parameters
        ----------
        uploaded_file
            Streamlit uploaded file object.

        Returns
        -------
        pd.DataFrame | None
        """

        if uploaded_file is None:
            return None

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):
            return pd.read_csv(uploaded_file)

        if file_name.endswith(".xlsx"):
            return pd.read_excel(uploaded_file)

        raise ValueError("Unsupported file format.")