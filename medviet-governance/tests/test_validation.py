import pytest
import pandas as pd
from src.quality.validation import validate_anonymized_data

def test_validate_anonymized_data_success(monkeypatch):
    original_df = pd.DataFrame({"patient_id": [1, 2]})
    
    def mock_read_csv(filepath, *args, **kwargs):
        if "raw" in str(filepath):
            return original_df
        return pd.DataFrame({
            "patient_id": [1, 2],
            "cccd": ["***masked***", "fake_data"],
            "benh": ["Sốt", "Ho"],
            "ket_qua_xet_nghiem": [12, 14]
        })
        
    monkeypatch.setattr("pandas.read_csv", mock_read_csv)

    results = validate_anonymized_data("fake_path.csv")
    assert results["success"] is True
    assert len(results["failed_checks"]) == 0

def test_validate_anonymized_data_failure_cccd(monkeypatch):
    original_df = pd.DataFrame({"patient_id": [1, 2]})
    
    def mock_read_csv(filepath, *args, **kwargs):
        if "raw" in str(filepath):
            return original_df
        return pd.DataFrame({
            "patient_id": [1, 2],
            "cccd": ["123456789012", "098765432109"],
            "benh": ["Sốt", "Ho"],
            "ket_qua_xet_nghiem": [12, 14]
        })
        
    monkeypatch.setattr("pandas.read_csv", mock_read_csv)

    results = validate_anonymized_data("fake_path.csv")
    assert results["success"] is False
    assert any("CCCD still in raw numeric format" in err for err in results["failed_checks"])

def test_validate_anonymized_data_failure_nulls(monkeypatch):
    original_df = pd.DataFrame({"patient_id": [1, 2]})
    
    def mock_read_csv(filepath, *args, **kwargs):
        if "raw" in str(filepath):
            return original_df
        return pd.DataFrame({
            "patient_id": [1, None],
            "cccd": ["***masked***", "fake_data"],
            "benh": ["Sốt", "Ho"],
            "ket_qua_xet_nghiem": [12, None]
        })
        
    monkeypatch.setattr("pandas.read_csv", mock_read_csv)

    results = validate_anonymized_data("fake_path.csv")
    assert results["success"] is False
    assert any("patient_id has" in err for err in results["failed_checks"])

def test_validate_anonymized_data_failure_row_count(monkeypatch):
    original_df = pd.DataFrame({"patient_id": [1, 2, 3]})
    
    def mock_read_csv(filepath, *args, **kwargs):
        if "raw" in str(filepath):
            return original_df
        return pd.DataFrame({
            "patient_id": [1, 2],
            "cccd": ["***masked***", "fake_data"],
            "benh": ["Sốt", "Ho"],
            "ket_qua_xet_nghiem": [12, 14]
        })
        
    monkeypatch.setattr("pandas.read_csv", mock_read_csv)

    results = validate_anonymized_data("fake_path.csv")
    assert results["success"] is False
    assert any("Row count mismatch" in err for err in results["failed_checks"])
