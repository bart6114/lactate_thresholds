import logging

import pandas as pd

from lactate_thresholds.model import (
    determine_loglog,
    determine_ltp,
    determine_mod_dmax,
    interpolate,
)
from lactate_thresholds.types import LactateThresholdResults


def clean_data(
    df: pd.DataFrame,
    step_col: str = "step",
    length_col: str = "length",
    intensity_col: str = "intensity",
    lactate_col: str = "lactate",
    heart_rate_col: str = "heart_rate",
) -> pd.DataFrame:
    ## if df not a dataframe raise valueerror
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a DataFrame")

    df_clean = df.copy()
    df_clean = df_clean.rename(
        columns={
            step_col: "step",
            length_col: "length",
            intensity_col: "intensity",
            lactate_col: "lactate",
            heart_rate_col: "heart_rate",
        }
    )
    df_clean = df_clean[["step", "length", "intensity", "lactate", "heart_rate"]]

    ## iterate over columns and assert that all entries in the column are numeric
    for col in df_clean.columns:
        if not pd.api.types.is_numeric_dtype(df_clean[col]):
            raise ValueError(
                f"Column '{col}' is not numeric / contains nonnumeric values"
            )

    return df_clean


def determine(
    df: pd.DataFrame,
    step_col: str = "step",
    length_col: str = "length",
    intensity_col: str = "intensity",
    lactate_col: str = "lactate",
    heart_rate_col: str = "heart_rate",
    include_baseline=False,
) -> pd.DataFrame:
    dfc = clean_data(
        df, step_col, length_col, intensity_col, lactate_col, heart_rate_col
    )
    dfi = interpolate(dfc, include_baseline=include_baseline)

    res = LactateThresholdResults(clean_data=dfc, interpolated_data=dfi)
    res.ltp1, res.ltp2 = determine_ltp(dfc, dfi)
    res.mod_dmax = determine_mod_dmax(dfc, dfi)
    res.loglog = determine_loglog(dfc, dfi)

    return res
