import os
import logging

def exists_file(filename):

    if not os.path.exists(filename):
        logger.critical('No such file "%s"', filename)
        return False
    else:
        logger.info('Processing file "%s"', filename)
        return True


def process_file(filename):

    if exists_file(filename):
        logger.info('Do somthing with "%s"', filename)
    else:
        return


if __name__ == '__main__':

    file_path = "./sample.txt"
    logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatter, level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    process_file(file_path)

