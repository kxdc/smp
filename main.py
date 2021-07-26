import os
import re
import logging


def exists_file(filename):

    if not os.path.exists(filename):
        logger.critical('No such file "%s"', filename)
        return False
    else:
        logger.info('Processing file "%s"', filename)
        return True


def get_lines(filename):

    with open(filename, 'rt') as file:
        lines = file.read()

    return lines


def process_file(filename):

    if exists_file(filename):
        return get_lines(filename).split('.')
    else:
        return


def search_substr_in_line(line, substr):

    return (substr, [string.start() for string in re.finditer(substr, line)])


def search_word_in_line(line, word):

    return (word, [idx for idx, wd in enumerate(line.split()) if wd == word])


def search_words_in_context(context, target_words_list):

    results = []
    line_index = -1

    for one_line in context:
        line_index += 1
        oneline_result = []
        for target_word in target_words_list:
            oneline_result.append(search_word_in_line(one_line, target_word))
        results.append((line_index, oneline_result))

    return results


if __name__ == '__main__':

    file_path = "./sample.txt"
    logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatter, level=logging.INFO)
    logger = logging.getLogger(__name__)

    mail_context = process_file(file_path)

    noticed_list = ['very', 'just', 'really']
    context_results = search_words_in_context(mail_context, noticed_list)
