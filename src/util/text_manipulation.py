from typing import List

import nlpaug.augmenter.word as naw
from transformers import MarianMTModel, MarianTokenizer

from graph.data.models import Language


def get_translation_model_name(src_language: Language, target_language: Language) -> str:
    if src_language == Language.EN and target_language == Language.PT:
        return "Helsinki-NLP/opus-mt-tc-big-en-pt"

    return f'Helsinki-NLP/opus-mt-{src_language.iso_lower}-{target_language.iso_lower}'


def translate(texts: List[str], src_language: Language, target_language: Language):
    model_name = get_translation_model_name(src_language, target_language)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)

    translated = model.generate(**inputs)

    translated_texts = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

    return translated_texts


def back_translate(texts: list[str], src_language: Language) -> list[str]:
    target_language = Language.DE
    back_translation_aug = naw.BackTranslationAug(
        from_model_name=get_translation_model_name(src_language, target_language),
        to_model_name=get_translation_model_name(target_language, src_language),
    )
    return back_translation_aug.augment(texts)
