from src.service.utils import replacement
import json
import os
import inspect

class MatRemover:
    def __init__(self):
        mat = open(f"{os.getcwd()}/src/service/bad_words.json", "r")
        self.data = json.load(mat)
        self.words = list(self.data.keys())
        mat.close()

    def replace_letters(self, text):
        phrase = text.lower().replace(" ", "")

        for key, value in replacement.items():
            for letter in value:
                for phr in phrase:
                    if letter == phr:
                        phrase = phrase.replace(phr, key)
        return phrase

    def make_fragments(self, phrase):
        fragments = []
        for word in self.words:
            for part in range(len(phrase)):
                fragment = phrase[part: part+len(word)]
                fragments.append(fragment)
        return fragments

    def search_mat(self, fragments):
        for word in self.words:
            for fragment in fragments:
                if word == fragment:
                    return self.data[word]
        return False

    def search(self, text):
        proc_text = self.replace_letters(text)
        fragments = self.make_fragments(proc_text)
        mat = self.search_mat(fragments)
        if mat:
            return mat
        else:
            return text

