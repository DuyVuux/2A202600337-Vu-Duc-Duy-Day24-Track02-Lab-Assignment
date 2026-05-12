import pandas as pd
import pytest
from src.pii.anonymizer import MedVietAnonymizer

def test_anonymize_text_replace():
    anonymizer = MedVietAnonymizer()
    text = "Bệnh nhân có CCCD là 123456789012 và SĐT là 0912345678."
    anon_text = anonymizer.anonymize_text(text, strategy="replace")
    
    assert "123456789012" not in anon_text
    assert "0912345678" not in anon_text

def test_anonymize_dataframe():
    anonymizer = MedVietAnonymizer()
    df = pd.DataFrame({
        "patient_id": ["P001", "P002"],
        "ho_ten": ["Nguyễn Văn A", "Trần Thị B"],
        "email": ["a@example.com", "b@example.com"],
        "dia_chi": ["Hà Nội", "Hồ Chí Minh"],
        "cccd": ["001090123456", "079190123456"],
        "so_dien_thoai": ["0912345678", "0987654321"],
        "bac_si_phu_trach": ["Bác sĩ C", "Bác sĩ D"],
        "benh": ["Sốt", "Ho"],
        "ket_qua_xet_nghiem": ["Bình thường", "Âm tính"]
    })
    
    df_anon = anonymizer.anonymize_dataframe(df)
    
    assert list(df_anon["patient_id"]) == ["P001", "P002"]
    assert list(df_anon["benh"]) == ["Sốt", "Ho"]
    assert list(df_anon["ket_qua_xet_nghiem"]) == ["Bình thường", "Âm tính"]
    
    assert list(df_anon["ho_ten"]) != ["Nguyễn Văn A", "Trần Thị B"]
    assert list(df_anon["email"]) != ["a@example.com", "b@example.com"]
    assert list(df_anon["dia_chi"]) != ["Hà Nội", "Hồ Chí Minh"]
    assert list(df_anon["cccd"]) != ["001090123456", "079190123456"]
    assert list(df_anon["so_dien_thoai"]) != ["0912345678", "0987654321"]
    assert list(df_anon["bac_si_phu_trach"]) != ["Bác sĩ C", "Bác sĩ D"]

def test_calculate_detection_rate():
    anonymizer = MedVietAnonymizer()
    df = pd.DataFrame({
        "ho_ten": ["Nguyễn Văn A", "Không xác định"],
        "cccd": ["123456789012", ""]
    })
    rate = anonymizer.calculate_detection_rate(df, ["ho_ten", "cccd"])
    assert 0.0 <= rate <= 1.0
