import json
import random
import re

#aug = naw.SynonymAug(aug_src='ppdb', model_path=r"C:\Users\bueck\Downloads\ppdb-1.0-xl-lexical\ppdb-1.0-xl-lexical")
#aug = naw.ContextualWordEmbsAug(
#    model_path='google-bert/bert-base-german-cased', action="substitute")

REMOVE_WORDS_PROB = {
    "dringend": 0.9,
    "Dringend": 0.9,
    "dringende": 0.9,
    "dringendes": 0.9

}


def remove_words(text):
    splitted = re.findall(r'[A-Za-z]+|[^A-Za-z]', text)
    print(splitted)
    new_words = []
    for word in splitted:
        word_prob = REMOVE_WORDS_PROB.get(word)
        if word_prob is None or random.random() > word_prob:
            new_words.append(word)
    return "".join(new_words)


if __name__ == '__main__':
    json.load(open("../../dataset-generator/data/training/gpt4/gpt-4-5k-23-5.json", "r", encoding="utf-8"))
    #test_text = "Hallo ich habe ein dringendes Problem. Bitte schnell eine Lösung finden. Libe Grüße. Ich liebe den Strand und Häuser"
    #print(aug.augment(test_text))