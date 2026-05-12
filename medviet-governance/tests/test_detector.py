from src.pii.detector import build_vietnamese_analyzer, detect_pii

def test_build_vietnamese_analyzer():
    analyzer = build_vietnamese_analyzer()
    assert analyzer is not None
    assert "vi" in analyzer.supported_languages

def test_detect_pii():
    analyzer = build_vietnamese_analyzer()
    text = "CCCD: 012345678901, liên hệ 0912345678"
    results = detect_pii(text, analyzer)
    entities = {res.entity_type for res in results}
    assert "VN_CCCD" in entities
    assert "VN_PHONE" in entities
