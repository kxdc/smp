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
        """
        initialize function for the class

        :param self: instance of the class
        :return: None
        """
        self.target_word_list: List[str] = []
        self.content: List[str] = []
        self.outputs: List[str] = []
        self.logger = logging.getLogger(__name__)
        self.replace_char = " "

    def set_target_word_list(self, word_list: List[str]) -> None:
        """
        Set value of member 'target_word_list'

        :param self: instance of the class
        :param word_list: list of words to be set
        :return: None
        """
        self.target_word_list = word_list

    def exists_file(self, filename: str) -> bool:
        """
        Check whether the file exists

        :param self: instance of the class
        :param filename: path to the target file
        :return: file exists or not
        """
        if not os.path.exists(filename):
            self.logger.critical('No such file "%s"', filename)
            return False
        else:
            self.logger.info('Processing file "%s"', filename)
            return True

    def get_lines(self, filename: str) -> str:
        """
        Get lines from target file

        :param self: instance of the class
        :param filename: path to the target file
        :return: content of lines
        """
        with open(filename, "rt") as file:
            lines = file.read()

        return lines

    def process_file(self, filename: str) -> None:
        """
        Whole process of target file

        :param self: instance of the class
        :param filename: path to the target file
        :return: None
        """
        if self.exists_file(filename):
            for oneline in self.get_lines(filename).split("."):
                self.content.append(oneline.lstrip())

    def search_substr_in_line(self, line: str, sstr: str) -> Oneline_Results:
        """
        Search target sub string in target line

        :param self: instance of the class
        :param line: line to be processed
        :param sstr: sub string to be searched
        :return: results of this search
        """
        return (sstr, [string.start() for string in re.finditer(sstr, line)])

    def search_word_in_line(self, line: str, word: str) -> Oneline_Results:
        """
        Search target word in target line

        :param self: instance of the class
        :param line: line to be processed
        :param word: word to be searched
        :return: results of this search
        """
        return (word, [i for i, w in enumerate(line.split()) if w == word])

    def search_words_in_content(self) -> Content_Results:
        """
        Search target word in self member 'content'

        :param self: instance of the class
        :return: results of this search
        """
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
        """
        Get the match result of target word

        :param self: instance of the class
        :param word: target word to match
        :param list: line to match with the target word
        :param threshold: define the similarity
        :return: results of this match
        """
        s = difflib.SequenceMatcher(None, word, target)
        w = "".join(word[i:i + n] for i, j, n in s.get_matching_blocks() if n)
        if len(w) / float(len(target)) >= threshold:
            yield w

    def replace_except_target(self, line: str, target: Oneline_Results) -> str:
        """
        Get a new line only with target word

        :param self: instance of the class
        :param line: source line
        :param target: target word and it's position
        :return: new line after process
        """
        tmp = line.split(" ")
        for idx in range(len(tmp)):
            if not tmp[idx] == target[0]:
                tmp[idx] = self.replace_char * len(tmp[idx])

        return self.replace_char.join(tmp)

    def process_words_to_remove(self, results: Content_Results) -> None:
        """
        Generate the lines to show words to be removed

        :param self: instance of the class
        :param results: word hit results
        :return: None
        """
        for oneline_result in results:
            hint_line = ""
            orig_line = self.content[oneline_result[0]]
            for word_hit in oneline_result[1]:
                if len(word_hit[1]) > 0:
                    hint_line = self.replace_except_target(orig_line, word_hit)

            if len(hint_line) == 0:
                for line in orig_line.split("\n"):
                    hint_line += self.replace_char * len(line) + "\n"
                hint_line = hint_line.rstrip("\n")
            self.outputs.append(hint_line)

    def splitted_display(self, size) -> None:
        """
        Display the lines with characters limit

        :param self: instance of the class
        :param size: limit of char length
        :return: None
        """
        squiz_content = "# ".join(self.content)
        squiz_outputs = " ".join(self.outputs)
        words = squiz_content.split(" ")
        total_length = 0

        while total_length < len(squiz_content) and len(words) > 0:
            line = []
            next_word = words[0]
            line_len = len(next_word) + 1

            while (line_len < size) and len(words) > 0:
                words.pop(0)
                line.append(next_word)

                if len(words) > 0:
                    next_word = words[0]
                    line_len += len(next_word) + 1

            line = " ".join(line)
            print(line)
            print(squiz_outputs[total_length:total_length + len(line)])
            total_length += len(line)

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
    # mail_helper.display_outputs()
    mail_helper.splitted_display(80)
