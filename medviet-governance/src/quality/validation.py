import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

def build_patient_expectation_suite() -> ExpectationSuite:
    df = pd.read_csv("data/raw/patients_raw.csv")
    try:
        context = gx.get_context()
        suite = context.add_expectation_suite("patient_data_suite")
        validator = context.sources.pandas_default.read_dataframe(df)
    except AttributeError:
        context = gx.data_context.DataContext()
        suite = context.add_expectation_suite("patient_data_suite")
        validator = gx.from_pandas(df)

    validator.expect_column_values_to_not_be_null("patient_id")
    validator.expect_column_value_lengths_to_equal(column="cccd", value=12)
    validator.expect_column_values_to_be_between(column="ket_qua_xet_nghiem", min_value=0, max_value=50)
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(column="benh", value_set=valid_conditions)
    validator.expect_column_values_to_match_regex(column="email", regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    validator.expect_column_values_to_be_unique(column="patient_id")

    try:
        validator.save_expectation_suite()
    except Exception:
        pass

    return suite

def validate_anonymized_data(filepath: str) -> dict:
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    if df["cccd"].astype(str).str.match(r"^\d{12}$").all():
        results["failed_checks"].append("CCCD still in raw numeric format")
        results["success"] = False

    critical = ["patient_id", "benh", "ket_qua_xet_nghiem"]
    for col in critical:
        nulls = df[col].isnull().sum()
        if nulls > 0:
            results["failed_checks"].append(f"{col} has {nulls} null values")
            results["success"] = False

    original = pd.read_csv("data/raw/patients_raw.csv")
    if len(df) != len(original):
        results["failed_checks"].append(f"Row count mismatch: {len(df)} vs {len(original)}")
        results["success"] = False

    return results
