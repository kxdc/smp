# -*- coding: UTF-8 -*-
import os
import re
import logging
from typing import List, Tuple


Oneline_Results = Tuple[str, List[int]]
Content_Results = List[Tuple[int, List[Oneline_Results]]]


class SimpleMailHelper:
    target_word_list=[]
    content=[]

    def set_target_word_list(self, word_list: List[str]) -> None:

        self.target_words_list=word_list

    def exists_file(self, filename: str) -> bool:
    
        if not os.path.exists(filename):
            logger.critical('No such file "%s"', filename)
            return False
        else:
            logger.info('Processing file "%s"', filename)
            return True
    
    
    def get_lines(self, filename: str) -> str:
    
        with open(filename, "rt") as file:
            lines = file.read()
    
        return lines
    
    
    def process_file(self, filename: str) -> None:
    
        if self.exists_file(filename):
            for oneline in self.get_lines(filename).split("."):
                self.content.append(oneline.lstrip())
    
    def search_substr_in_line(self, line: str, substr: str) -> Oneline_Results:
    
        return (substr, [string.start() for string in re.finditer(substr, line)])
    
    
    def search_word_in_line(self, line: str, word: str) -> Oneline_Results:
    
        return (word, [idx for idx, wd in enumerate(line.split()) if wd == word])
    
    
    def search_words_in_content(self) -> Content_Results:
    
        results = []
        line_index = -1
    
        for oneline in self.content:
            line_index += 1
            oneline_result = []
            for target_word in self.target_word_list:
                oneline_result.append(self.search_word_in_line(oneline, target_word))
            results.append((line_index, oneline_result))
    
        return results
    
    
    def process_words_to_remove(self, results: Content_Results) -> None:
    
        for oneline_result in results:
            found = False
            hint_line = ""
            for word_hit in oneline_result[1]:
                if len(word_hit[1]) > 0:
                    found = True
                    position_hit = ",".join(str(c) for c in word_hit[1])
                    hint_line = word_hit[0] + ":" + position_hit
    
            print(self.content[oneline_result[0]])
            if found:
                print(hint_line, end="")
            else:
                print(hint_line)


if __name__ == "__main__":

    file_path = "../sample.txt"
    logFormatter = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=logFormatter, level=logging.INFO)
    logger = logging.getLogger(__name__)

    smp = SimpleMailHelper()
    smp.process_file(file_path)

    noticed_list = ["very", "just", "really"]
    smp.set_target_word_list(noticed_list)
    content_results = smp.search_words_in_content()
    smp.process_words_to_remove(content_results)
