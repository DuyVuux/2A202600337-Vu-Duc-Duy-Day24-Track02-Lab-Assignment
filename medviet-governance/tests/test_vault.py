import os
import json
import pandas as pd
import pytest
from src.encryption.vault import SimpleVault

@pytest.fixture
def vault(tmp_path):
    key_path = tmp_path / ".vault_key"
    return SimpleVault(master_key_path=str(key_path))

def test_encrypt_decrypt_data(vault):
    plaintext = "Đây là thông tin mật"
    encrypted = vault.encrypt_data(plaintext)
    
    assert "encrypted_dek" in encrypted
    assert "ciphertext" in encrypted
    assert encrypted["algorithm"] == "AES-256-GCM"
    
    decrypted = vault.decrypt_data(encrypted)
    assert decrypted == plaintext

def test_encrypt_column(vault):
    df = pd.DataFrame({
        "id": [1, 2],
        "secret_data": ["Secret 1", "Secret 2"]
    })
    
    encrypted_df = vault.encrypt_column(df, "secret_data")
    
    assert list(encrypted_df["id"]) == [1, 2]
    assert encrypted_df["secret_data"][0] != "Secret 1"
    
    payload1 = json.loads(encrypted_df["secret_data"][0])
    payload2 = json.loads(encrypted_df["secret_data"][1])
    
    assert vault.decrypt_data(payload1) == "Secret 1"
    assert vault.decrypt_data(payload2) == "Secret 2"
