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

    with open (filename, 'rt') as file:
        lines = file.read()

    return lines


def process_file(filename):

    if exists_file(filename):
        return get_lines(filename).split('.')
    else:
        return


if __name__ == '__main__':

    file_path = "./sample.txt"
    logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatter, level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    mail_context = process_file(file_path)

    noticed_list = [ 'with', 'the' ]
    search_words_in_context(mail_context, noticed_list)
