import sys
import os
import re
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))
from generate_data import generate_patients

def test_generate_patients():
    df = generate_patients(n=10)
    assert len(df) == 10
    expected_columns = [
        "patient_id", "ho_ten", "cccd", "ngay_sinh", "so_dien_thoai",
        "email", "dia_chi", "benh", "ket_qua_xet_nghiem",
        "bac_si_phu_trach", "ngay_kham"
    ]
    assert list(df.columns) == expected_columns
    assert all(isinstance(x, str) and len(x) == 12 and x.isdigit() for x in df["cccd"])
    assert all(isinstance(x, str) and re.match(r"^0[35789]\d{8}$", x) for x in df["so_dien_thoai"])
    assert all(3.5 <= x <= 12.0 for x in df["ket_qua_xet_nghiem"])
