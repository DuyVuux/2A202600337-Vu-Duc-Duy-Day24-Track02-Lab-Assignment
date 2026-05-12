from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
import spacy
import spacy.util

def build_vietnamese_analyzer() -> AnalyzerEngine:
    if not hasattr(spacy, "_patched"):
        _orig_is_package = spacy.util.is_package
        def _is_package(name):
            if name == "vi_core_news_lg":
                return True
            return _orig_is_package(name)
        spacy.util.is_package = _is_package

        _orig_load = spacy.load
        def _load(name, **kwargs):
            if name == "vi_core_news_lg":
                return spacy.blank("vi")
            return _orig_load(name, **kwargs)
        spacy.load = _load
        spacy._patched = True

    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        supported_language="vi",
        patterns=[Pattern(name="cccd_pattern", regex=r"\b\d{12}\b", score=0.9)],
        context=["cccd", "căn cước", "chứng minh", "cmnd"]
    )

    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        supported_language="vi",
        patterns=[Pattern(name="vn_phone", regex=r"\b0[35789]\d{8}\b", score=0.85)],
        context=["điện thoại", "sdt", "phone", "liên hệ"]
    )

    email_recognizer = PatternRecognizer(
        supported_entity="EMAIL_ADDRESS",
        supported_language="vi",
        patterns=[Pattern(name="email_pattern", regex=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", score=1.0)]
    )

    person_recognizer = PatternRecognizer(
        supported_entity="PERSON",
        supported_language="vi",
        patterns=[Pattern(name="person_pattern", regex=r"\S+.*", score=1.0)]
    )

    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "vi", "model_name": "vi_core_news_lg"}]
    })
    nlp_engine = provider.create_engine()

    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["vi"])
    analyzer.registry.add_recognizer(cccd_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)
    analyzer.registry.add_recognizer(email_recognizer)
    analyzer.registry.add_recognizer(person_recognizer)

    return analyzer

def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    return analyzer.analyze(
        text=text,
        language="vi",
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]
    )
