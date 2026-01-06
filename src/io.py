"""
I/O utilities for loading and saving data.
"""

import pandas as pd
from pathlib import Path
from typing import Union


def load_csv(filepath: Union[str, Path], encoding: str = "utf-8-sig") -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file.
    encoding : str, default "utf-8-sig"
        File encoding. Default handles BOM in UTF-8 files.

    Returns
    -------
    pd.DataFrame
        Loaded data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath, encoding=encoding)
    return df


def save_csv(df: pd.DataFrame, filepath: Union[str, Path], index: bool = False) -> None:
    """
    Save a DataFrame to CSV.

    Parameters
    ----------
    df : pd.DataFrame
        Data to save.
    filepath : str or Path
        Output path.
    index : bool, default False
        Whether to include row index.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=index)


def save_markdown(content: str, filepath: Union[str, Path]) -> None:
    """
    Save text content to a markdown file.

    Parameters
    ----------
    content : str
        Markdown content.
    filepath : str or Path
        Output path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
