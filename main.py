import os
import re
import logging
# from typing import List, Tuple
# 
# 
# Onelie_Results=Tuple[str, list[int]]
# Context_Results=List[Tuple[int, List[Onelie_Results]]]


def exists_file(filename:str) -> bool:

    if not os.path.exists(filename):
        logger.critical('No such file "%s"', filename)
        return False
    else:
        logger.info('Processing file "%s"', filename)
        return True


def get_lines(filename:str) -> str:

    with open(filename, "rt") as file:
        lines = file.read()

    return lines


def process_file(filename:str) -> list[str]:

    if exists_file(filename):
        return get_lines(filename).split(".")
    else:
        return []


def search_substr_in_line(line:str, substr:str) -> tuple[str, list[int]]:

    return (substr, [string.start() for string in re.finditer(substr, line)])


def search_word_in_line(line:str, word:str) -> tuple[str, list[int]]:

    return (word, [idx for idx, wd in enumerate(line.split()) if wd == word])


def search_words_in_context(context:list[str], target_words_list:list[str]) -> list[tuple[int, list[tuple[str, list[int]]]]]:

    results = []
    line_index = -1

    for oneline in context:
        line_index += 1
        oneline_result = []
        for target_word in target_words_list:
            oneline_result.append(search_word_in_line(oneline, target_word))
        results.append((line_index, oneline_result))

    return results


def process_words_to_remove(lines:list[str], results:list[int], word_list:list[str]) -> None:

    for oneline_result in results:
        found = False
        hint_line = ""
        for word_hit in oneline_result[1]:
            if len(word_hit[1]) > 0:
                found = True
                position_hit = ",".join(str(c) for c in word_hit[1])
                hint_line = word_hit[0] + ":" + position_hit

        print(lines[oneline_result[0]])
        if found:
            print(hint_line, end="")
        else:
            print(hint_line)


if __name__ == "__main__":

    file_path = "./sample.txt"
    logFormatter = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=logFormatter, level=logging.INFO)
    logger = logging.getLogger(__name__)

    mail_context = process_file(file_path)

    noticed_list = ["very", "just", "really"]
    context_results = search_words_in_context(mail_context, noticed_list)
    process_words_to_remove(mail_context, context_results, noticed_list)
