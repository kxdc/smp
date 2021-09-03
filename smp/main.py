# -*- coding: UTF-8 -*-
import os
import re
import logging
import difflib
from typing import List, Tuple, Generator


Oneline_Results = Tuple[str, List[int]]
Content_Results = List[Tuple[int, List[Oneline_Results]]]
logFormatter = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=logFormatter, level=logging.INFO)


class SimpleMailHelper:
    def __init__(self) -> None:
        self.target_word_list: List[str] = []
        self.content: List[str] = []
        self.outputs: List[str] = []
        self.logger = logging.getLogger(__name__)
        self.replace_char = " "

    def set_target_word_list(self, word_list: List[str]) -> None:

        self.target_word_list = word_list

    def exists_file(self, filename: str) -> bool:

        if not os.path.exists(filename):
            self.logger.critical('No such file "%s"', filename)
            return False
        else:
            self.logger.info('Processing file "%s"', filename)
            return True

    def get_lines(self, filename: str) -> str:

        with open(filename, "rt") as file:
            lines = file.read()

        return lines

    def process_file(self, filename: str) -> None:

        if self.exists_file(filename):
            for oneline in self.get_lines(filename).split("."):
                self.content.append(oneline.lstrip())

    def search_substr_in_line(self, line: str, sstr: str) -> Oneline_Results:

        return (sstr, [string.start() for string in re.finditer(sstr, line)])

    def search_word_in_line(self, line: str, word: str) -> Oneline_Results:

        return (word, [i for i, w in enumerate(line.split()) if w == word])

    def search_words_in_content(self) -> Content_Results:

        results = []
        line_index = -1

        for oneline in self.content:
            line_index += 1
            oneline_result = []
            for word in self.target_word_list:
                oneline_result.append(self.search_word_in_line(oneline, word))
            results.append((line_index, oneline_result))

        return results

    def word_matches(
            self, word: str, target: List[str], threshold: int
    ) -> Generator[str, None, None]:

        s = difflib.SequenceMatcher(None, word, target)
        w = ''.join(word[i:i+n] for i, j, n in s.get_matching_blocks() if n)
        if len(w) / float(len(target)) >= threshold:
            yield w

    def replace_except_target(self, line: str, target: Oneline_Results) -> str:

        tmp = line.split(" ")
        for idx in range(len(tmp)):
            if not tmp[idx] == target[0]:
                tmp[idx] = self.replace_char * len(tmp[idx])

        return self.replace_char.join(tmp)

    def process_words_to_remove(self, results: Content_Results) -> None:

        for oneline_result in results:
            hint_line = ""
            for word_hit in oneline_result[1]:
                if len(word_hit[1]) > 0:
                    hint_line = self.replace_except_target(
                        self.content[oneline_result[0]], word_hit[0]
                    )

            self.outputs.append(hint_line)

    def display_outputs(self) -> None:

        for i in range(len(self.content)):
            print(self.content[i])
            print(self.outputs[i])


if __name__ == "__main__":

    file_path = "../sample.txt"

    mail_helper = SimpleMailHelper()
    mail_helper.process_file(file_path)

    noticed_list = ["very", "just", "really"]
    mail_helper.set_target_word_list(noticed_list)
    content_results = mail_helper.search_words_in_content()
    mail_helper.process_words_to_remove(content_results)
    mail_helper.display_outputs()
