from keybert import KeyBERT
import pandas as pd


class KeywordGenerator():
    def __init__(self):
        self.kw_model = KeyBERT()

    def create_keywords_for_doc(self, doc):
        keywords = self.kw_model.extract_keywords(doc)

        return keywords
