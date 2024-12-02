import pandas as pd
import pytest

from lactate_thresholds import process

test_instances = {
    "simple": [
        {"step": 0, "length": 0, "intensity": 0, "lactate": 1.0, "heart_rate": 80},
        {"step": 1, "length": 4, "intensity": 8.5, "lactate": 2.2, "heart_rate": 122},
        {"step": 2, "length": 4, "intensity": 10.0, "lactate": 1.3, "heart_rate": 131},
        {"step": 3, "length": 4, "intensity": 11.5, "lactate": 1.0, "heart_rate": 145},
        {"step": 4, "length": 4, "intensity": 13.0, "lactate": 0.8, "heart_rate": 155},
        {"step": 5, "length": 4, "intensity": 14.5, "lactate": 1.1, "heart_rate": 162},
        {"step": 6, "length": 4, "intensity": 16.0, "lactate": 1.8, "heart_rate": 171},
        {"step": 7, "length": 4, "intensity": 17.5, "lactate": 2.9, "heart_rate": 180},
        {"step": 8, "length": 4, "intensity": 19.0, "lactate": 5.3, "heart_rate": 186},
    ],
    "differently_named_cols": [
        {"step": 0, "step_length": 0, "intensity": 0, "lactate": 1.0, "heartrate": 80},
        {
            "step": 1,
            "step_length": 4,
            "intensity": 8.5,
            "lactate": 2.2,
            "heartrate": 122,
        },
        {
            "step": 2,
            "step_length": 4,
            "intensity": 10.0,
            "lactate": 1.3,
            "heartrate": 131,
        },
        {
            "step": 3,
            "step_length": 4,
            "intensity": 11.5,
            "lactate": 1.0,
            "heartrate": 145,
        },
        {
            "step": 4,
            "step_length": 4,
            "intensity": 13.0,
            "lactate": 0.8,
            "heartrate": 155,
        },
        {
            "step": 5,
            "step_length": 4,
            "intensity": 14.5,
            "lactate": 1.1,
            "heartrate": 162,
        },
        {
            "step": 6,
            "step_length": 4,
            "intensity": 16.0,
            "lactate": 1.8,
            "heartrate": 171,
        },
        {
            "step": 7,
            "step_length": 4,
            "intensity": 17.5,
            "lactate": 2.9,
            "heartrate": 180,
        },
        {
            "step": 8,
            "step_length": 4,
            "intensity": 19.0,
            "lactate": 5.3,
            "heartrate": 186,
        },
    ],
    "non_numeric_vals": [
        {"step": 0, "length": 0, "intensity": 0, "lactate": 1.0, "heartrate": 80},
        {"step": 1, "length": 4, "intensity": 8.5, "lactate": 2.2, "heartrate": 122},
        {"step": 2, "length": 4, "intensity": "a", "lactate": 1.3, "heartrate": 131},
        {"step": 3, "length": 4, "intensity": 11.5, "lactate": 1.0, "heartrate": 145},
        {"step": 4, "length": 4, "intensity": 13.0, "lactate": 0.8, "heartrate": 155},
        {"step": 5, "length": 4, "intensity": 14.5, "lactate": 1.1, "heartrate": 162},
        {"step": 6, "length": 4, "intensity": 16.0, "lactate": 1.8, "heartrate": 171},
        {"step": 7, "length": 4, "intensity": 17.5, "lactate": 2.9, "heartrate": 180},
        {"step": 8, "length": 4, "intensity": 19.0, "lactate": 5.3, "heartrate": 186},
    ],
}


def test_lactate_data_ingestion_simple():
    df = pd.DataFrame.from_dict(test_instances["simple"])
    df2 = process.lactate_data(df)
    assert set(df2.columns) == set(
        ["step", "length", "intensity", "lactate", "heart_rate"]
    )


def test_lactate_data_ingestion_rename():
    df = pd.DataFrame.from_dict(test_instances["differently_named_cols"])
    df2 = process.lactate_data(df, heart_rate_col="heartrate", length_col="step_length")
    assert set(df2.columns) == set(
        ["step", "length", "intensity", "lactate", "heart_rate"]
    )


def test_lactate_data_ingestion_non_numeric():
    df = pd.DataFrame.from_dict(test_instances["non_numeric_vals"])
    with pytest.raises(ValueError):
        process.lactate_data(df, heart_rate_col="heartrate")
