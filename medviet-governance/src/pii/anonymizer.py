import pandas as pd
import random
import hashlib
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from faker import Faker
from .detector import build_vietnamese_analyzer, detect_pii

fake = Faker("vi_VN")

class MedVietAnonymizer:
    def __init__(self):
        self.analyzer = build_vietnamese_analyzer()
        self.anonymizer = AnonymizerEngine()

    def anonymize_text(self, text: str, strategy: str = "replace") -> str:
        results = detect_pii(text, self.analyzer)
        if not results:
            return text
        
        operators = {}
        if strategy == "replace":
            operators = {
                "PERSON": OperatorConfig("replace", {"new_value": fake.name()}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": fake.email()}),
                "VN_CCCD": OperatorConfig("replace", {"new_value": "".join([str(random.randint(0, 9)) for _ in range(12)])}),
                "VN_PHONE": OperatorConfig("replace", {"new_value": f"0{random.choice([3, 5, 7, 8, 9])}" + "".join([str(random.randint(0, 9)) for _ in range(8)])})
            }
        elif strategy == "mask":
            operators = {
                "DEFAULT": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 6, "from_end": False})
            }
        elif strategy == "hash":
            operators = {
                "DEFAULT": OperatorConfig("hash", {"hash_type": "sha256"})
            }
            
        return self.anonymizer.anonymize(text=text, analyzer_results=results, operators=operators).text

    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df_anon = df.copy()
        df_anon["ho_ten"] = [fake.name() for _ in range(len(df))]
        df_anon["email"] = [fake.email() for _ in range(len(df))]
        df_anon["dia_chi"] = [fake.address() for _ in range(len(df))]
        df_anon["cccd"] = ["".join([str(random.randint(0, 9)) for _ in range(12)]) for _ in range(len(df))]
        df_anon["so_dien_thoai"] = [f"0{random.choice([3, 5, 7, 8, 9])}" + "".join([str(random.randint(0, 9)) for _ in range(8)]) for _ in range(len(df))]
        df_anon["bac_si_phu_trach"] = [fake.name() for _ in range(len(df))]
        return df_anon

    def calculate_detection_rate(self, original_df: pd.DataFrame, pii_columns: list) -> float:
        total = 0
        detected = 0
        for col in pii_columns:
            for value in original_df[col].astype(str):
                total += 1
                results = detect_pii(value, self.analyzer)
                if len(results) > 0:
                    detected += 1
        return detected / total if total > 0 else 0.0
