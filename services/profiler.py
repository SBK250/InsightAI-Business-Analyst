"""Dataset profiling utilities.

This module exposes a small profiling API that can be used from Python code and
from the command line. It supports both DataFrame objects and CSV/Excel files.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Union

import pandas as pd


def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """Return a compact summary of a pandas DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame")

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "numeric_columns": int(len(df.select_dtypes(include="number").columns)),
        "categorical_columns": int(len(df.select_dtypes(include="object").columns)),
        "memory_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
        "column_names": list(df.columns),
    }


class DataProfiler:
    """Backward-compatible wrapper around the profiling helper."""

    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate a basic data profile for a DataFrame."""
        return profile_dataframe(df)


def profile(data: Union[pd.DataFrame, str, Path]) -> Dict[str, Any]:
    """Load data from a file path or profile an existing DataFrame."""
    if isinstance(data, (str, Path)):
        path = Path(data)
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")

        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        elif path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(path)
        else:
            raise ValueError("Only CSV and Excel files are supported")
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise TypeError("Expected a pandas DataFrame or a file path")

    return profile_dataframe(df)


def main() -> int:
    """CLI entry point for profiling a CSV or Excel file."""
    parser = argparse.ArgumentParser(description="Profile a CSV or Excel dataset")
    parser.add_argument("path", nargs="?", help="Path to the CSV or Excel file")
    args = parser.parse_args()

    if not args.path:
        parser.print_help()
        return 1

    result = profile(args.path)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())